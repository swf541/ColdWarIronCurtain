# -*- coding: utf-8 -*-
"""Resolve deposits.csv (country,resource,deposit,state_hint,weight,confidence,note)
   to state IDs by name match, then distribute each country's existing endowment
   total across its deposits by weight. Unresolved hints are reported, never guessed."""
import re,glob,csv,sys,collections,unicodedata
MOD='/sessions/sweet-quirky-curie/mnt/Cold War Iron Curtain'
def norm(s):
    s=unicodedata.normalize('NFKD',s).encode('ascii','ignore').decode().lower()
    return re.sub(r'[^a-z0-9]','',s)
def bb(s,i0):
    i=i0;d=1
    while d>0:
        if s[i]=='{':d+=1
        elif s[i]=='}':d-=1
        i+=1
    return s[i0:i-1],i
def lr(total,weights):
    if total<=0 or not weights: return [0]*len(weights)
    sw=sum(weights) or 1.0
    raw=[total*w/sw for w in weights]; base=[int(x) for x in raw]
    for i in sorted(range(len(raw)),key=lambda i:-(raw[i]-base[i]))[:total-sum(base)]: base[i]+=1
    return base
sname={}
for l in open(f'{MOD}/localisation/english/state_names_l_english.yml',encoding='utf-8-sig',errors='replace'):
    m=re.match(r'\s*STATE_(\d+):\d*\s*"(.*)"',l)
    if m: sname.setdefault(int(m.group(1)),m.group(2))
files={}; owner={}; cur=collections.defaultdict(collections.Counter); bycountry=collections.defaultdict(list)
for f in glob.glob(f'{MOD}/history/states/*.txt'):
    t=re.sub(r'#[^\n]*','',open(f,encoding='utf-8-sig',errors='replace').read())
    o=re.search(r'^\s*owner\s*=\s*(\w+)',t,re.M)
    if not o: continue
    sid=int(re.search(r'\bid\s*=\s*(\d+)',t).group(1))
    files[sid]=f; owner[sid]=o.group(1); bycountry[o.group(1)].append(sid)
    m=re.search(r'resources\s*=\s*\{([^}]*)\}',t)
    if m:
        for k,v in re.findall(r'(\w+)\s*=\s*([\d.]+)',m.group(1)): cur[o.group(1)][k]+=float(v)
def resolve(tag,hint):
    if hint.strip().isdigit():
        sid=int(hint)
        return sid if owner.get(sid)==tag else None
    h=norm(hint); cands=bycountry.get(tag,[])
    exact=[s for s in cands if norm(sname.get(s,''))==h]
    if exact: return exact[0]
    sub=[s for s in cands if h and h in norm(sname.get(s,''))]
    if len(sub)==1: return sub[0]
    sub2=[s for s in cands if h and norm(sname.get(s,'')) and norm(sname.get(s,'')) in h]
    if len(sub2)==1: return sub2[0]
    return sub[0] if sub else None
rows=list(csv.DictReader(open(sys.argv[1],encoding='utf-8-sig')))
plan=collections.defaultdict(list); unresolved=[]
for r in rows:
    tag=r['country'].strip(); res=r['resource'].strip()
    sid=resolve(tag,r['state_hint'])
    if sid is None: unresolved.append((tag,res,r['deposit'],r['state_hint'])); continue
    plan[(tag,res)].append((sid,float(r['weight']),r['deposit'],r['confidence']))
print('deposit rows: %d   resolved: %d   UNRESOLVED: %d'%(len(rows),len(rows)-len(unresolved),len(unresolved)))
for u in unresolved: print('   !! %s %s "%s" -> hint "%s" matched nothing'%u)
if unresolved and '--force' not in sys.argv:
    print('\naborting - fix the hints or pass --force'); sys.exit(1)
newres=collections.defaultdict(dict); touched=set()
for (tag,res),lst in plan.items():
    total=int(round(cur[tag][res]))
    if total<=0: print('   (skip %s %s: country holds none)'%(tag,res)); continue
    for (sid,w,dep,conf),v in zip(lst,lr(total,[x[1] for x in lst])):
        if v>0: newres[sid][res]=newres[sid].get(res,0)+v
    touched.add((tag,res))
n=0
for tag,res in touched:
    for sid in bycountry[tag]:
        f=files[sid]; raw=open(f,encoding='utf-8',errors='replace').read()
        m=re.search(r'([ \t]*)resources\s*=\s*\{',raw)
        keep=dict(newres.get(sid,{}))
        if m:
            inner,e=bb(raw,m.end())
            for k,v in re.findall(r'(\w+)\s*=\s*([\d.]+)',inner):
                if (tag,k) not in touched: keep.setdefault(k,int(round(float(v))))
        if keep:
            body='\n'+'\n'.join('\t\t%s = %d.000'%(k,v) for k,v in sorted(keep.items()))+'\n\t'
            if m: raw=raw[:m.end()]+body+raw[e-1:]
            else:
                nm=re.search(r'(name\s*=\s*"[^"]*"[^\n]*\n)',raw)
                raw=raw[:nm.end()]+'\tresources = {'+body+'}\n'+raw[nm.end():]
        elif m:
            _,e=bb(raw,m.end()); ls=raw.rfind('\n',0,m.start())+1
            raw=raw[:ls]+raw[e:].lstrip('\n')
        else: continue
        open(f,'w',encoding='utf-8').write(raw); n+=1
print('\ncountry/resource pairs placed: %d   state files rewritten: %d'%(len(touched),n))
