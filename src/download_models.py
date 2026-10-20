"""Fetch exact author snapshots into this workspace, without using shared caches."""
import json, concurrent.futures, requests, os, time
from pathlib import Path

def fetch(task):
    slug,rev,name=task
    p=Path('models')/slug.split('/')[-1]/name
    p.parent.mkdir(parents=True,exist_ok=True)
    if p.exists(): return
    headers={}
    if os.getenv('HF_TOKEN'): headers['Authorization']='Bearer '+os.environ['HF_TOKEN']
    for attempt in range(3):
      try:
        with requests.get(f'https://huggingface.co/{slug}/resolve/{rev}/{name}',headers=headers,stream=True,timeout=(30,180)) as r:
          r.raise_for_status()
          with p.with_suffix(p.suffix+'.part').open('wb') as f:
            for chunk in r.iter_content(8*1024*1024): f.write(chunk)
        p.with_suffix(p.suffix+'.part').rename(p)
        print('downloaded',slug,name,p.stat().st_size,flush=True);return
      except Exception as e:
        print(type(e).__name__,slug,name,'attempt',attempt,flush=True)
        if attempt==2: raise
        time.sleep(2)
if __name__=='__main__':
 tasks=[]
 for p in Path('results/manifests').glob('*8B.json'):
  d=json.loads(p.read_text())
  tasks += [(d['id'],d['sha'],s['rfilename']) for s in d['siblings'] if '/' not in s['rfilename'] and not s['rfilename'].startswith('.')]
 with concurrent.futures.ThreadPoolExecutor(max_workers=6) as ex: list(ex.map(fetch,tasks))
