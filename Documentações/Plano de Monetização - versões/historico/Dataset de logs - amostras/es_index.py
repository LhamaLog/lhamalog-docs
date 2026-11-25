import json, urllib.request, hashlib, os, glob, random
from measure import sev
ES="http://localhost:9200"
def req(m,p,b=None,ct="application/json"):
    r=urllib.request.Request(ES+p,data=b,method=m,headers={"Content-Type":ct})
    try: return json.loads(urllib.request.urlopen(r).read())
    except urllib.error.HTTPError as e: return json.loads(e.read())
props={"@timestamp":{"type":"date_nanos"},"tenant_id":{"type":"keyword"},"service.name":{"type":"keyword"},"host.name":{"type":"keyword"},
 "severity_text":{"type":"keyword"},"severity_number":{"type":"byte"},"body":{"type":"match_only_text"},"trace_id":{"type":"keyword"},"span_id":{"type":"keyword"},"log.file.name":{"type":"keyword"}}
idx={
 "logs-dynamic":{"settings":{"number_of_shards":1,"number_of_replicas":0}},
 "logs-opt":{"settings":{"number_of_shards":1,"number_of_replicas":0,"codec":"best_compression"},"mappings":{"dynamic":"strict","properties":props}},
 "logs-logsdb":{"settings":{"number_of_shards":1,"number_of_replicas":0,"index.mode":"logsdb"},"mappings":{"properties":dict(props,**{"host.name":{"type":"keyword"}})}},
}
for k,v in idx.items():
    req("DELETE","/"+k); print(k, req("PUT","/"+k, json.dumps(v).encode()))
N=20000; rawtot=0; docs=0; t0=1760000000000000000
for f in sorted(glob.glob("data/*.log")):
    name=os.path.basename(f)[:-4]; lines=[]
    with open(f,"rb") as fh:
        for i,l in enumerate(fh):
            if i>=N: break
            l=l.decode("utf-8","replace").rstrip("\n")
            if l.strip(): lines.append(l)
    for k in idx:
        buf=[]
        for j,l in enumerate(lines):
            ts=t0+(docs+j)*1000000; st,sn=sev(l); h=hashlib.md5(str(ts).encode()).hexdigest()
            from datetime import datetime,timezone
            iso=datetime.fromtimestamp(ts//10**9,timezone.utc).strftime("%Y-%m-%dT%H:%M:%S")+".%09dZ"%(ts%10**9)
            d={"@timestamp":iso,"tenant_id":"tenant-%04d"%random.randint(1,20),"service.name":name.lower(),"host.name":"node-%02d"%random.randint(1,5),
               "severity_text":st,"severity_number":sn,"body":l,"trace_id":h,"span_id":h[:16],"log.file.name":name+".log"}
            buf.append('{"index":{}}'); buf.append(json.dumps(d))
            if len(buf)>=10000:
                r=req("POST","/%s/_bulk"%k,("\n".join(buf)+"\n").encode(),"application/x-ndjson"); assert not r.get("errors"),str(r)[:500]; buf=[]
        if buf: r=req("POST","/%s/_bulk"%k,("\n".join(buf)+"\n").encode(),"application/x-ndjson"); assert not r.get("errors"),str(r)[:500]
    rawtot+=sum(len(l.encode())+1 for l in lines); docs+=len(lines)
for k in idx:
    req("POST","/%s/_refresh"%k); req("POST","/%s/_forcemerge?max_num_segments=1"%k)
res={"docs":docs,"raw_bytes":rawtot}
for k in idx:
    s=req("GET","/%s/_stats/store,docs"%k)["indices"][k]["primaries"]
    res[k]={"count":s["docs"]["count"],"store_bytes":s["store"]["size_in_bytes"],"ratio_vs_raw":s["store"]["size_in_bytes"]/rawtot,"bytes_per_doc":s["store"]["size_in_bytes"]/s["docs"]["count"]}
print(json.dumps(res,indent=1)); json.dump(res,open("es_measure.json","w"),indent=1)
