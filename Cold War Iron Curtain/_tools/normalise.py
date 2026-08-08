# -*- coding: utf-8 -*-
"""After geological placement, scale each country's endowment per resource so that
   EFFECTIVE OUTPUT (endowment x state-category extraction rate) hits the 1950 target."""
import re,glob,collections,importlib.util
MOD='/sessions/sweet-quirky-curie/mnt/Cold War Iron Curtain'
s=importlib.util.spec_from_file_location('t','/tmp/work/targets.py');T=importlib.util.module_from_spec(s);s.loader.exec_module(T)
for c in T.TARGETS:
    for g in ('MLA','RHO'): T.TARGETS[c].pop(g,None)
def bb(s2,i0):
    i=i0;d=1
    while d>0:
        if s2[i]=='{':d+=1
        elif s2[i]=='}':d-=1
        i+=1
    return s2[i0:i-1],i
cats={}
for f in glob.glob(f'{MOD}/common/state_category/*.txt'):
    t=re.sub(r'#[^\n]*','',open(f,encoding='utf-8-sig',errors='replace').read())
    for m in re.finditer(r'\n\t(\w+) = \{',t):
        b,_=bb(t,m.end())
        lr=re.search(r'local_resources_factor\s*=\s*(-?[\d.]+)',b)
        if lr: cats[m.group(1)]=1.0+float(lr.group(1))
st=[]
for f in glob.glob(f'{MOD}/history/states/*.txt'):
    raw=open(f,encoding='utf-8',errors='replace').read(); t=re.sub(r'#[^\n]*','',raw)
    o=re.search(r'^\s*owner\s*=\s*(\w+)',t,re.M); c=re.search(r'^\s*state_category\s*=\s*(\w+)',t,re.M)
    m=re.search(r'([ \t]*)resources\s*=\s*\{',raw)
    if not o or not m: continue
    inner,e=bb(raw,m.end())
    vals={k:float(v) for k,v in re.findall(r'(\w+)\s*=\s*([\d.]+)',inner)}
    st.append([f,o.group(1),cats.get(c.group(1)) if c else None,vals])
COLS=['oil','steel','aluminium','tungsten','chromium']
for it in range(6):
    out=collections.Counter(); byc=collections.defaultdict(collections.Counter)
    for f,tg,r,v in st:
        if not r: continue
        for k,val in v.items():
            if k in COLS: out[k]+=val*r; byc[tg][k]+=val*r
    worst=0
    fac=collections.defaultdict(dict)
    for c in COLS:
        named=T.TARGETS[c]; tail_t=1.0-sum(named.values())
        tail_cur=sum(byc[tg][c] for tg in byc if tg not in named)
        for tg in byc:
            have=byc[tg][c]
            if have<=0: continue
            want=(named[tg]*out[c]) if tg in named else (have/tail_cur*tail_t*out[c] if tail_cur>0 else 0)
            fac[tg][c]=want/have
            worst=max(worst,abs(100*want/out[c]-100*have/out[c]))
    if worst<0.25: break
    for row in st:
        f,tg,r,v=row
        for k in list(v):
            if k in COLS and k in fac.get(tg,{}): v[k]=v[k]*fac[tg][k]
print('converged after %d iteration(s), worst residual %.2f pp'%(it+1,worst))
n=0
for f,tg,r,v in st:
    raw=open(f,encoding='utf-8',errors='replace').read()
    m=re.search(r'([ \t]*)resources\s*=\s*\{',raw); inner,e=bb(raw,m.end())
    keep={k:int(round(val)) for k,val in v.items() if round(val)>0}
    if keep: body='\n'+'\n'.join('\t\t%s = %d.000'%(k,x) for k,x in sorted(keep.items()))+'\n\t'
    else:
        ls=raw.rfind('\n',0,m.start())+1
        open(f,'w',encoding='utf-8').write(raw[:ls]+raw[e:].lstrip('\n')); n+=1; continue
    open(f,'w',encoding='utf-8').write(raw[:m.end()]+body+raw[e-1:]); n+=1
print('state files rewritten:',n)
