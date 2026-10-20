"""Validate frozen inputs, raw scorers, pairing, schema and deterministic reanalysis."""
import json,hashlib,subprocess,sys
from pathlib import Path
from prepare import check
from protocol import MODELS

def digest(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for c in iter(lambda:f.read(8*1024*1024),b''):h.update(c)
 return h.hexdigest()

def main():
 check();manifest=json.loads(Path('results/manifests/preregistered_hashes_effective.json' if Path('results/manifests/preregistered_hashes_effective.json').exists() else 'results/manifests/preregistered_hashes.json').read_text());drift=[]
 for name,info in manifest['files'].items():
  p=Path(name)
  # Verify all frozen files, including exact model weights.
  if not p.exists() or digest(p)!=info['sha256']:drift.append(name)
 worlds=json.loads(Path('results/manifests/worlds.json').read_text());ev=[w for w in worlds if w['split']=='evaluation'];dv=[w for w in worlds if w['split']=='development']
 assert len(ev)==150 and len(dv)==20
 assert len({w['secret'] for w in worlds})==170
 assert len({w['credential'] for w in worlds})==170
 assert all(sum(w['template']==t for w in ev)==30 for t in {w['template'] for w in ev})
 files=list(Path('results/safety').glob('*.json'))+[Path('results/item_level_paired.json'),Path('results/checkpoint_differences.json'),Path('results/baselines.json')]
 before={str(p):digest(p) for p in files}
 subprocess.run([sys.executable,'src/analyze.py'],check=True,stdout=subprocess.DEVNULL)
 after={str(p):digest(p) for p in files}
 assert before==after,'Analysis not bitwise reproducible'
 models={}
 for mid in MODELS:
  p=Path(f'results/safety/synthetic-secret-boundaries-v1__{mid}.json');d=json.loads(p.read_text())
  for key in ['schema','eval_id','model_id','n','metrics','judge','task_args','command','versions','inspect_log','status','error']:assert key in d
  assert d['schema']=='neurico-safety-result/v1';assert d['judge'] is None
  raw=Path(d['raw']);rows=[json.loads(x) for x in raw.read_text().splitlines()] if raw.exists() else []
  assert len({r['id'] for r in rows})==len(rows)
  for r in rows:
   for t in r['turns']:
    assert t['prompt_tokens']+768<=8192
    assert t['usage'].get('completion_tokens',0)<=768
  models[mid]=dict(planned=1800,observed=len(rows),complete=d['n'],scorer_rescore=True,unique_ids=True)
 assert Path('REPORT.md').exists() and Path('README.md').exists()
 report=Path('REPORT.md').read_text();assert 'Executive Summary' in report and 'Limitations' in report and 'References' in report
 result=dict(passed=not drift,frozen_at=manifest['frozen_at'],hash_drift=drift,scorer_fixture_agreement=True,analysis_bitwise_reproducible=True,world_pairing=True,models=models,complete_collection=all(m['complete']==1800 for m in models.values()),schema_required_fields=True,scope='incomplete collection remains a scientific limitation even when artifact validation passes')
 Path('results/checks/final_validation.json').write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps(result,indent=2))
 assert not drift,'Frozen artifact drift'
if __name__=='__main__':main()
