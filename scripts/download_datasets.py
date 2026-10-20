"""Download pinned Tensor Trust resources and verify expected hashes."""
import json,pathlib,hashlib,requests
root=pathlib.Path(__file__).resolve().parents[1]
assert pathlib.Path.cwd()==root and (root/'.git').is_dir()
print(root)
for m in json.loads((root/'datasets/manifest.json').read_text()):
 r=requests.get(m['source'],timeout=120);r.raise_for_status()
 assert hashlib.sha256(r.content).hexdigest()==m['sha256'],m['name']
 rows=[json.loads(x) for x in r.text.splitlines()];assert len(rows)==m['rows']
 (root/m['path']).write_bytes(r.content)
 print(m['name'],len(rows),'verified')
