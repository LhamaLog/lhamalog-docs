// Core (Java 25 / Spring Boot) — DTOs e lógica de recomendação
// Ilustrativo: em produção, cada tipo público vai em seu próprio arquivo .java.
package com.lhamalog.core.storage.latency;

import java.time.Instant;
import java.util.*;
import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.index.Indexed;
import org.springframework.data.mongodb.core.mapping.Document;
import org.springframework.stereotype.Service;

public enum ProviderId { magalu, oci, aws }

public record ProbeResult(ProviderId provider, String region, String url, List<Double> samplesMs, int failures,
                          Double p50Ms, Double p90Ms, Double minMs, Double jitterMs, String timingSource) {}

public record LatencyTestPayload(String source, Instant startedAt, Instant finishedAt, int samplesPerTarget,
                                 Map<String, String> client, List<ProbeResult> results) {}

@Document("storage_latency_tests")
public record LatencyTest(@Id String id, @Indexed String tenantId, String userId, String source,
                          @Indexed(expireAfter = "90d") Instant createdAt, List<ProbeResult> results) {}

public record RankedOption(ProviderId provider, String region, double p50Ms, double p90Ms, double successRate,
                           double storagePricePerGbMonthBrl, boolean tiedWithBest) {}

public record StorageRecommendation(String testId, RankedOption recommended, List<RankedOption> ranking,
                                    String criterion, boolean advisory, String measuredFrom) {}

/** Tabela de preços vem de configuração (application.yml / Mongo), alinhada à planilha v3 (aba Preços por Uso). */
public interface StoragePriceCatalog { double storagePricePerGbMonthBrl(ProviderId p, String region); }

@Service
public class StorageRecommendationService {
    static final int MIN_SAMPLES = 5;
    static final double TIE_PCT = 0.10;   // empate técnico: ≤ 10% ...
    static final double TIE_ABS_MS = 15;  // ... ou ≤ 15 ms

    private final StoragePriceCatalog prices;
    public StorageRecommendationService(StoragePriceCatalog prices) { this.prices = prices; }

    /** Recalcula p50/p90 no servidor (não confia nos agregados do cliente) e aplica o critério. */
    public StorageRecommendation recommend(LatencyTest test) {
        List<RankedOption> valid = new ArrayList<>();
        for (ProbeResult r : test.results()) {
            List<Double> s = r.samplesMs().stream().filter(x -> x != null && x >= 0 && x < 10_000).sorted().toList();
            if (s.size() < MIN_SAMPLES) continue;
            double success = s.size() / (double) (s.size() + r.failures());
            if (success < 0.8) continue; // região instável para este cliente
            valid.add(new RankedOption(r.provider(), r.region(), pct(s, 50), pct(s, 90), success,
                    prices.storagePricePerGbMonthBrl(r.provider(), r.region()), false));
        }
        if (valid.isEmpty()) throw new IllegalStateException("nenhuma região com amostras suficientes");
        double best = valid.stream().mapToDouble(RankedOption::p50Ms).min().orElseThrow();
        List<RankedOption> ranked = valid.stream()
            .map(o -> new RankedOption(o.provider(), o.region(), o.p50Ms(), o.p90Ms(), o.successRate(),
                    o.storagePricePerGbMonthBrl(),
                    o.p50Ms() - best <= Math.max(TIE_ABS_MS, best * TIE_PCT)))
            // empatados primeiro, ordenados por preço; depois os demais por latência
            .sorted(Comparator.comparing((RankedOption o) -> !o.tiedWithBest())
                    .thenComparing(o -> o.tiedWithBest() ? o.storagePricePerGbMonthBrl() : o.p50Ms())
                    .thenComparingDouble(RankedOption::p90Ms))
            .toList();
        return new StorageRecommendation(test.id(), ranked.get(0), ranked,
                "menor p50; empate (≤10% ou ≤15 ms) desempatado pelo menor R$/GB-mês", true, test.source());
    }

    static double pct(List<Double> sorted, double p) {
        int i = (int) Math.ceil(p / 100.0 * sorted.size()) - 1;
        return sorted.get(Math.max(0, Math.min(sorted.size() - 1, i)));
    }
}
