import requests,json,pathlib,re,html,hashlib,concurrent.futures
R=pathlib.Path(__file__).resolve().parents[1]
assert pathlib.Path.cwd()==R and (R/'.git').is_dir()
ids={'2311.01011':'tensor_trust','2404.01833':'crescendo','2404.13208':'instruction_hierarchy','2501.12948':'deepseek_r1','2307.06865':'prompt_extraction'}
def paper(kv):
 aid,slug=kv
 h=requests.get('https://arxiv.org/abs/'+aid,timeout=60);h.raise_for_status()
 meta={k: [html.unescape(v) for v in re.findall('<meta name="citation_'+k+'" content="(.*?)"',h.text)] for k in ['title','author','date','abstract','pdf_url']}
 p=R/f'papers/{aid}_{slug}.pdf';r=requests.get(meta['pdf_url'][0],timeout=120);r.raise_for_status();assert r.content.startswith(b'%PDF');p.write_bytes(r.content)
 meta.update(id=aid,file=str(p.relative_to(R)),sha256=hashlib.sha256(r.content).hexdigest());(R/f'notes/{slug}_metadata.json').write_text(json.dumps(meta,indent=2));return meta
if __name__ == '__main__':
 for m in concurrent.futures.ThreadPoolExecutor(4).map(paper,ids.items()):print(m['id'],m['title'][0])
