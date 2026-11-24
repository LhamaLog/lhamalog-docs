// LhamaLog — teste de latência do provedor de bucket (roda no NAVEGADOR do cliente)
// Uso: onboarding/configurações, quando o cliente escolhe onde guardar os logs.
// Mede RTT HTTP até um objeto público pequeno (~1 KB) em cada região candidata e envia ao Core.

export type ProviderId = "magalu" | "oci" | "aws";

export interface ProbeTarget {
  provider: ProviderId;
  region: string;        // ex.: "br-se1", "sa-saopaulo-1", "sa-east-1"
  url: string;           // objeto público de teste, ex.: https://br-se1.magaluobjects.com/lhamalog-probe-br-se1/probe-1k.bin
}

export interface ProbeResult {
  provider: ProviderId;
  region: string;
  url: string;
  samplesMs: number[];   // só amostras bem-sucedidas, em ms
  failures: number;
  p50Ms: number | null;
  p90Ms: number | null;
  minMs: number | null;
  jitterMs: number | null;   // desvio-padrão
  timingSource: "resource-timing" | "performance-now";
}

export interface LatencyTestPayload {
  source: "browser" | "collector";
  startedAt: string;     // ISO 8601
  finishedAt: string;
  samplesPerTarget: number;
  client: { userAgent: string; connection?: string; timezone: string };
  results: ProbeResult[];
}

const sleep = (ms: number) => new Promise((r) => setTimeout(r, ms));

function percentile(sorted: number[], p: number): number | null {
  if (sorted.length === 0) return null;
  const idx = Math.min(sorted.length - 1, Math.max(0, Math.ceil((p / 100) * sorted.length) - 1));
  return sorted[idx];
}

function stddev(xs: number[]): number | null {
  if (xs.length < 2) return null;
  const m = xs.reduce((a, b) => a + b, 0) / xs.length;
  return Math.sqrt(xs.reduce((a, b) => a + (b - m) ** 2, 0) / (xs.length - 1));
}

function shuffle<T>(arr: T[]): T[] {
  const a = [...arr];
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [a[i], a[j]] = [a[j], a[i]];
  }
  return a;
}

/**
 * Uma amostra. Prioriza Resource Timing (responseStart - requestStart = ~1 RTT + tempo de servidor,
 * sem DNS/TLS) quando o bucket envia Timing-Allow-Origin. Sem esse header, os campos detalhados vêm zerados
 * e usamos performance.now() em volta do fetch (inclui fila do navegador; ainda serve para comparar).
 * mode "cors" exige CORS no bucket; se falhar, tentamos "no-cors" (resposta opaca, mas o tempo é medido).
 */
async function sampleOnce(url: string, timeoutMs: number): Promise<{ ms: number; src: ProbeResult["timingSource"] }> {
  const u = `${url}${url.includes("?") ? "&" : "?"}lhm=${Date.now()}-${Math.random().toString(36).slice(2)}`;
  const ctrl = new AbortController();
  const timer = setTimeout(() => ctrl.abort(), timeoutMs);
  const t0 = performance.now();
  try {
    try {
      const resp = await fetch(u, { method: "GET", mode: "cors", cache: "no-store", credentials: "omit", signal: ctrl.signal });
      await resp.arrayBuffer(); // garante resposta completa (objeto ~1 KB)
    } catch (e) {
      if ((e as Error).name === "AbortError") throw e;
      await fetch(u, { method: "GET", mode: "no-cors", cache: "no-store", credentials: "omit", signal: ctrl.signal });
    }
    const t1 = performance.now();
    const entries = performance.getEntriesByName(u) as PerformanceResourceTiming[];
    const rt = entries[entries.length - 1];
    if (rt && rt.requestStart > 0 && rt.responseStart > 0) {
      return { ms: rt.responseStart - rt.requestStart, src: "resource-timing" };
    }
    return { ms: t1 - t0, src: "performance-now" };
  } finally {
    clearTimeout(timer);
  }
}

/**
 * Executa o teste: 1 aquecimento descartado por alvo (abre DNS+TCP+TLS), depois N rodadas intercaladas
 * em ordem aleatória (evita favorecer quem vai primeiro).
 */
export async function runLatencyTest(
  targets: ProbeTarget[],
  opts: { samples?: number; timeoutMs?: number; pauseMs?: number } = {}
): Promise<LatencyTestPayload> {
  const samples = Math.min(10, Math.max(5, opts.samples ?? 7));
  const timeoutMs = opts.timeoutMs ?? 3000;
  const pauseMs = opts.pauseMs ?? 100;
  const startedAt = new Date().toISOString();
  const acc = new Map<string, { s: number[]; fail: number; src: ProbeResult["timingSource"] }>();
  targets.forEach((t) => acc.set(t.url, { s: [], fail: 0, src: "performance-now" }));

  // aquecimento (não entra na estatística)
  await Promise.allSettled(targets.map((t) => sampleOnce(t.url, timeoutMs)));

  for (let round = 0; round < samples; round++) {
    for (const t of shuffle(targets)) {
      const a = acc.get(t.url)!;
      try {
        const r = await sampleOnce(t.url, timeoutMs);
        a.s.push(Math.round(r.ms * 10) / 10);
        a.src = r.src;
      } catch {
        a.fail++;
      }
      await sleep(pauseMs);
    }
  }
  performance.clearResourceTimings();

  const results: ProbeResult[] = targets.map((t) => {
    const a = acc.get(t.url)!;
    const sorted = [...a.s].sort((x, y) => x - y);
    return {
      provider: t.provider, region: t.region, url: t.url,
      samplesMs: a.s, failures: a.fail,
      p50Ms: percentile(sorted, 50), p90Ms: percentile(sorted, 90),
      minMs: sorted[0] ?? null, jitterMs: stddev(a.s), timingSource: a.src,
    };
  });

  const nav = navigator as Navigator & { connection?: { effectiveType?: string } };
  return {
    source: "browser", startedAt, finishedAt: new Date().toISOString(), samplesPerTarget: samples,
    client: { userAgent: navigator.userAgent, connection: nav.connection?.effectiveType,
              timezone: Intl.DateTimeFormat().resolvedOptions().timeZone },
    results,
  };
}

/** Envia ao Core e devolve a recomendação calculada no servidor. */
export async function submitLatencyTest(apiBase: string, tenantId: string, token: string, payload: LatencyTestPayload) {
  const headers = { "Content-Type": "application/json", Authorization: `Bearer ${token}` };
  const post = await fetch(`${apiBase}/api/v1/tenants/${encodeURIComponent(tenantId)}/storage/latency-tests`,
    { method: "POST", headers, body: JSON.stringify(payload) });
  if (!post.ok) throw new Error(`latency-test POST falhou: ${post.status}`);
  const rec = await fetch(`${apiBase}/api/v1/tenants/${encodeURIComponent(tenantId)}/storage/recommendation`, { headers });
  if (!rec.ok) throw new Error(`recommendation GET falhou: ${rec.status}`);
  return rec.json(); // StorageRecommendation
}

// Exemplo (alvos vêm do Core: GET /api/v1/storage/probe-targets, para trocar URLs sem novo deploy do front)
export const DEFAULT_TARGETS: ProbeTarget[] = [
  { provider: "magalu", region: "br-se1", url: "https://br-se1.magaluobjects.com/lhamalog-probe-br-se1/probe-1k.bin" },
  { provider: "magalu", region: "br-ne1", url: "https://br-ne1.magaluobjects.com/lhamalog-probe-br-ne1/probe-1k.bin" },
  { provider: "oci", region: "sa-saopaulo-1", url: "https://objectstorage.sa-saopaulo-1.oraclecloud.com/n/<namespace>/b/lhamalog-probe/o/probe-1k.bin" },
  { provider: "oci", region: "sa-vinhedo-1", url: "https://objectstorage.sa-vinhedo-1.oraclecloud.com/n/<namespace>/b/lhamalog-probe/o/probe-1k.bin" },
  { provider: "aws", region: "sa-east-1", url: "https://lhamalog-probe-sa-east-1.s3.sa-east-1.amazonaws.com/probe-1k.bin" },
];
