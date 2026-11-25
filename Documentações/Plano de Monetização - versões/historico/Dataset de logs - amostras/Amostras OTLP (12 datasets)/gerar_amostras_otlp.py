"""Gera amostras OTLP/JSON (200 linhas) para os 12 datasets Loghub do LhamaLog.
Usa EXATAMENTE a mesma conversão do measure.py (função otlp(): lotes de 100 logs,
1 ExportLogsServiceRequest por linha, JSON compacto).
Entrada: <Dataset>_amostra_200.log (lido em modo texto: CRLF -> LF, igual às amostras
HDFS/SSH_amostra_100_otlp.json já existentes).
Uso: python3 gerar_amostras_otlp.py <pasta_com_amostras_200_e_measure.py> <pasta_saida>
"""
import sys, os, glob, json, gzip, csv
src, out = sys.argv[1], sys.argv[2]
sys.path.insert(0, src)
from measure import otlp
import zstandard
os.makedirs(out, exist_ok=True)
rows = []
for f in sorted(glob.glob(os.path.join(src, "*_amostra_200.log"))):
    name = os.path.basename(f).split("_amostra_")[0]
    with open(f, encoding="utf-8", errors="replace") as fh:
        lines = [l for l in fh.read().split("\n") if l.strip()][:200]
    o = otlp(name, lines)  # bytes, NDJSON (2 linhas = 2 lotes de 100)
    open(os.path.join(out, f"{name}_amostra_200_otlp.ndjson"), "wb").write(o + b"\n")
    raw = sum(len(l.encode()) + 1 for l in lines)
    rows.append(dict(dataset=name, linhas=len(lines), bytes_brutos=raw, bytes_por_log_bruto=round(raw/len(lines), 2),
        otlp_json_bytes=len(o), otlp_bytes_por_log=round(len(o)/len(lines), 2), otlp_overhead_x=round(len(o)/raw, 3),
        otlp_gzip6_bytes=len(gzip.compress(o, 6)), otlp_zstd3_bytes=len(zstandard.ZstdCompressor(level=3).compress(o)),
        otlp_zstd_vs_bruto_x=round(len(zstandard.ZstdCompressor(level=3).compress(o))/raw, 3)))
with open(os.path.join(out, "medicoes_amostras_otlp_200.csv"), "w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
for r in rows: print(r)
