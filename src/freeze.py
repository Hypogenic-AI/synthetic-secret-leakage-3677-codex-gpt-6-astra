"""Record immutable pre-inference hashes for protocol, code, data and snapshots."""
from pathlib import Path
import hashlib,json,datetime

def main():
 target=Path('results/manifests/preregistered_hashes.json')
 assert not target.exists(),'Do not overwrite preregistration'
 paths=[Path('preregistration.md'),Path('planning.md'),Path('pyproject.toml'),Path('uv.lock'),Path('results/manifests/worlds.json'),Path('results/manifests/environment.json'),Path('results/checks/fixtures.json'),Path('results/checks/scorer_checks.json')]
 paths+=list(Path('src').rglob('*.py'))+list(Path('src/runtime').glob('*.json'))
 paths+=list(Path('models').glob('*/*'))
 hashes={}
 for p in paths:
  if p.is_file() and not p.name.endswith('.part'):
   h=hashlib.sha256()
   with p.open('rb') as f:
    for chunk in iter(lambda:f.read(8*1024*1024),b''):h.update(chunk)
   hashes[str(p)]=dict(sha256=h.hexdigest(),bytes=p.stat().st_size)
 target.write_text(json.dumps(dict(frozen_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),files=hashes),indent=2)+'\n')
 print('Frozen',len(hashes),'files')
if __name__=='__main__':main()
