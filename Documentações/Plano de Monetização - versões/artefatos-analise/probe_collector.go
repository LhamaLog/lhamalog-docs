// Alternativa: medição a partir do collector/agente do cliente (Go), para quem ingere via OTLP
// (o collector roda na rede do cliente, mais perto de onde os logs nascem do que o navegador).
package probe

import (
	"bytes"
	"context"
	"crypto/tls"
	"encoding/json"
	"fmt"
	"io"
	"math/rand"
	"net/http"
	"net/http/httptrace"
	"sort"
	"time"
)

type Target struct {
	Provider string `json:"provider"`
	Region   string `json:"region"`
	URL      string `json:"url"`
}

type Result struct {
	Provider     string    `json:"provider"`
	Region       string    `json:"region"`
	URL          string    `json:"url"`
	SamplesMs    []float64 `json:"samplesMs"`
	Failures     int       `json:"failures"`
	P50Ms        *float64  `json:"p50Ms"`
	P90Ms        *float64  `json:"p90Ms"`
	MinMs        *float64  `json:"minMs"`
	TimingSource string    `json:"timingSource"`
}

// sample mede do envio da requisição ao primeiro byte da resposta (≈ RTT + servidor) com conexão reutilizada.
func sample(ctx context.Context, c *http.Client, url string) (float64, error) {
	var wrote, first time.Time
	tr := &httptrace.ClientTrace{
		WroteRequest:         func(httptrace.WroteRequestInfo) { wrote = time.Now() },
		GotFirstResponseByte: func() { first = time.Now() },
	}
	req, _ := http.NewRequestWithContext(httptrace.WithClientTrace(ctx, tr), http.MethodGet,
		fmt.Sprintf("%s?lhm=%d", url, rand.Int63()), nil)
	req.Header.Set("Cache-Control", "no-cache")
	resp, err := c.Do(req)
	if err != nil {
		return 0, err
	}
	io.Copy(io.Discard, resp.Body)
	resp.Body.Close()
	return float64(first.Sub(wrote).Microseconds()) / 1000, nil
}

func pct(s []float64, p float64) *float64 {
	if len(s) == 0 {
		return nil
	}
	i := int(float64(len(s))*p/100+0.999999) - 1
	if i < 0 {
		i = 0
	}
	v := s[i]
	return &v
}

func Run(ctx context.Context, targets []Target, n int) []Result {
	c := &http.Client{Timeout: 3 * time.Second, Transport: &http.Transport{TLSClientConfig: &tls.Config{}, MaxIdleConnsPerHost: 1}}
	acc := make(map[string]*Result)
	for _, t := range targets {
		acc[t.URL] = &Result{Provider: t.Provider, Region: t.Region, URL: t.URL, TimingSource: "collector-httptrace"}
		sample(ctx, c, t.URL) // aquecimento: abre TCP+TLS
	}
	for i := 0; i < n; i++ {
		order := rand.Perm(len(targets))
		for _, j := range order {
			r := acc[targets[j].URL]
			if ms, err := sample(ctx, c, targets[j].URL); err == nil {
				r.SamplesMs = append(r.SamplesMs, ms)
			} else {
				r.Failures++
			}
			time.Sleep(100 * time.Millisecond)
		}
	}
	out := make([]Result, 0, len(targets))
	for _, t := range targets {
		r := acc[t.URL]
		s := append([]float64(nil), r.SamplesMs...)
		sort.Float64s(s)
		r.P50Ms, r.P90Ms, r.MinMs = pct(s, 50), pct(s, 90), pct(s, 0.0001)
		out = append(out, *r)
	}
	return out
}

// Report envia ao mesmo endpoint do Core, com source="collector". token = chave de ingestão do tenant (escopo storage:latency).
func Report(ctx context.Context, apiBase, tenantID, token, collectorID string, started time.Time, n int, res []Result) error {
	body, _ := json.Marshal(map[string]any{
		"source": "collector", "startedAt": started.UTC().Format(time.RFC3339), "finishedAt": time.Now().UTC().Format(time.RFC3339),
		"samplesPerTarget": n, "client": map[string]string{"collectorId": collectorID}, "results": res,
	})
	req, _ := http.NewRequestWithContext(ctx, http.MethodPost,
		fmt.Sprintf("%s/api/v1/tenants/%s/storage/latency-tests", apiBase, tenantID), bytes.NewReader(body))
	req.Header.Set("Content-Type", "application/json")
	req.Header.Set("Authorization", "Bearer "+token)
	resp, err := http.DefaultClient.Do(req)
	if err != nil {
		return err
	}
	defer resp.Body.Close()
	if resp.StatusCode != http.StatusCreated {
		return fmt.Errorf("latency-test POST: %d", resp.StatusCode)
	}
	return nil
}
