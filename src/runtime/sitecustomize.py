"""Avoid repeated full-filesystem package metadata scans on the shared filesystem.

This caches only the package-to-distribution name mapping. It does not change
model code, tensors, sampling, tokenization or package version lookup.
"""
import importlib.metadata,json
from pathlib import Path
p=Path(__file__).with_name('package_distributions.json')
if p.exists():
    mapping=json.loads(p.read_text())
    importlib.metadata.packages_distributions=lambda: {k:list(v) for k,v in mapping.items()}

# Transformers' lazy import index is derived solely from installed source files.
# Persist the computed index so each GPU worker does not rescan thousands of files.
import importlib.machinery,hashlib,pickle,os
_original_exec=importlib.machinery.SourceFileLoader.exec_module

def _exec_module(self,module):
    _original_exec(self,module)
    if module.__name__=='transformers.utils.import_utils':
        original=module.define_import_structure
        def cached_structure(module_path,prefix=None):
            cache=Path(__file__).parent/'import_structure_cache'
            cache.mkdir(exist_ok=True)
            key=hashlib.sha256((str(module_path)+'|'+str(prefix)).encode()).hexdigest()
            dest=cache/(key+'.pickle')
            if dest.exists():
                with dest.open('rb') as f:return pickle.load(f)
            result=original(module_path,prefix)
            temp=cache/(key+f'.{os.getpid()}.tmp')
            with temp.open('wb') as f:pickle.dump(result,f)
            temp.replace(dest)
            return result
        module.define_import_structure=cached_structure
importlib.machinery.SourceFileLoader.exec_module=_exec_module
