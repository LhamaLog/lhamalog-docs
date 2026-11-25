import sys, os, gzip, json, zlib, zstandard, re, time, hashlib
from multiprocessing import Pool
SEV = [("FATAL",21),("CRITICAL",21),("ERROR",17),("SEVERE",17),("WARN",13),("WARNING",13),("INFO",9),("DEBUG",5),("TRACE",1)]
def sev(line):
    u=line[:200].upper()
    for k,n in SEV:
        if k in u: return k if k not in("WARNING","SEVERE","CRITICAL") else {"WARNING":"WARN","SEVERE":"ERROR","CRITICAL":"FATAL"}[k], n
    return "INFO",9
def otlp(name, lines, batch=100):
    out=[]
    t0=1760000000000000000
    for i in range(0,len(lines),batch):
        recs=[]
        for j,l in enumerate(lines[i:i+batch]):
            st,sn=sev(l); ts=str(t0+(i+j)*1000000)
            recs.append({"timeUnixNano":ts,"observedTimeUnixNano":ts,"severityNumber":sn,"severityText":st,
              "body":{"stringValue":l},
              "attributes":[{"key":"log.file.name","value":{"stringValue":name+".log"}}],
              "traceId":hashlib.md5(ts.encode()).hexdigest(),"spanId":hashlib.md5(ts.encode()).hexdigest()[:16]})
        out.append({"resourceLogs":[{"resource":{"attributes":[
            {"key":"service.name","value":{"stringValue":name.lower()}},
            {"key":"host.name","value":{"stringValue":"node-01"}},
            {"key":"lhamalog.tenant.id","value":{"stringValue":"tenant-0001"}}]},
            "scopeLogs":[{"scope":{"name":"lhamalog.filelog"},"logRecords":recs}]}]})
    return "\n".join(json.dumps(o,separators=(",",":")) for o in out).encode()
def run(path):
    name=os.path.basename(path).split(".")[0]
    raw=0; n=0
    gz=zlib.compressobj(6, zlib.DEFLATED, 31); gzs=0
    zc=zstandard.ZstdCompressor(level=3).compressobj(); zs=0
    first=[]
    with open(path,"rb") as f:
        while True:
            chunk=f.read(8<<20)
            if not chunk: break
            raw+=len(chunk); n+=chunk.count(b"\n")
            gzs+=len(gz.compress(chunk)); zs+=len(zc.compress(chunk))
            if len(first)<1000:
                first+= chunk.decode("utf-8","replace").split("\n")[:1000-len(first)]
    gzs+=len(gz.flush()); zs+=len(zc.flush())
    first=[l for l in first if l.strip()][:1000]
    rawsample=sum(len(l.encode())+1 for l in first)
    o=otlp(name, first)
    og=len(gzip.compress(o,6)); oz=len(zstandard.ZstdCompressor(level=3).compress(o))
    return dict(dataset=name, lines=n, raw_bytes=raw, avg_bytes=raw/n, gzip_bytes=gzs, gzip_ratio=raw/gzs, zstd_bytes=zs, zstd_ratio=raw/zs,
      sample_lines=len(first), sample_raw=rawsample, otlp_json=len(o), otlp_per_log=len(o)/len(first), otlp_overhead=len(o)/rawsample,
      otlp_gzip=og, otlp_zstd=oz)
if __name__=="__main__":
    files=sorted(sys.argv[1:], key=lambda p:-os.path.getsize(p))
    with Pool(6) as p: res=p.map(run, files)
    json.dump(res, open("/workspace/logs-dataset/measurements.json","w"), indent=1)
    for r in sorted(res,key=lambda r:r["dataset"]): print(r)
