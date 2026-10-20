"""Run exact checkpoints sequentially, retaining subprocess logs and stopping own server."""
import subprocess,os,json,time,signal,sys,urllib.request
from pathlib import Path
from protocol import MODELS

ROOT=Path.cwd();PY=str(ROOT/'.venv/bin/python')
def ready():
 try:
  with urllib.request.urlopen('http://127.0.0.1:8137/health',timeout=2) as r:return r.status==200
 except Exception:return False

def main():
 events=[];start=time.time();study_deadline=float(os.environ.get('STUDY_DEADLINE',start+3300))
 for model_index,model_id in enumerate(['deepseek-r1-distill-llama-8b','qwen3-8b']):
  model_deadline=time.time()+(study_deadline-time.time())/(2-model_index)
  modeldir=ROOT/'models'/MODELS[model_id].split('/')[-1]
  cmd=[PY,'-m','vllm.entrypoints.openai.api_server','--model',str(modeldir),'--served-model-name',model_id,'--dtype','bfloat16','--tensor-parallel-size','1','--max-model-len','8192','--max-num-seqs','96','--gpu-memory-utilization','0.90','--port','8137','--host','127.0.0.1','--generation-config','vllm','--enforce-eager']
  env=os.environ.copy();env.update(HF_HOME=str(ROOT/'models/hf_cache'),VLLM_CACHE_ROOT=str(ROOT/'.cache/vllm'),XDG_CACHE_HOME=str(ROOT/'.cache'),TORCHINDUCTOR_CACHE_DIR=str(ROOT/'.cache/torchinductor'),OMP_NUM_THREADS='8',LOCAL_BASE_URL='http://127.0.0.1:8137/v1',LOCAL_API_KEY='local',TOKENIZERS_PARALLELISM='false',PYTHONDONTWRITEBYTECODE='1',PYTHONPATH=str(ROOT/'src/runtime'))
  with (ROOT/f'logs/server_{model_id}.log').open('w') as log:
   server=subprocess.Popen(cmd,stdout=log,stderr=subprocess.STDOUT,env=env,start_new_session=True)
   event=dict(model_id=model_id,server_pid=server.pid,server_command=cmd,started=time.time())
   try:
    deadline=min(time.time()+600,model_deadline)
    while not ready():
     if server.poll() is not None:raise RuntimeError('server exited '+str(server.returncode))
     if time.time()>deadline:raise RuntimeError('server startup timed out')
     time.sleep(3)
    for split in ['development','evaluation']:
     command=[PY,'-m','inspect_ai','eval','src/evals/secret_boundaries.py@secret_boundaries','-T',f'model_id={model_id}','-T',f'split={split}','--model',f'openai-api/local/{model_id}','--log-dir','results/safety/inspect_logs','--log-format','json','--max-samples','96','--display','plain']
     print('Starting',model_id,split,flush=True)
     with (ROOT/f'logs/inspect_{model_id}__{split}.log').open('w') as out:
      result=subprocess.run(command,stdout=out,stderr=subprocess.STDOUT,env=env,timeout=max(1,min(1500,model_deadline-time.time())))
     event[split+'_returncode']=result.returncode
     if result.returncode:raise RuntimeError(f'{split} Inspect failed ({result.returncode})')
     raw=ROOT/f'results/raw/{model_id}__{split}.jsonl'
     if not raw.exists():raise RuntimeError('no raw outputs')
     rows=[json.loads(x) for x in raw.read_text().splitlines()]
     if split=='development' and not all(r['complete'] for r in rows):raise RuntimeError('development infrastructure check failed')
     print('Finished',model_id,split,'rows',len(rows),'complete',sum(r['complete'] for r in rows),flush=True)
   except Exception as e:event['error']=str(e);print('ERROR',model_id,str(e),flush=True)
   finally:
    if server.poll() is None:
     os.killpg(server.pid,signal.SIGTERM)
     try:server.wait(timeout=30)
     except subprocess.TimeoutExpired:os.killpg(server.pid,signal.SIGKILL);server.wait()
    event['finished']=time.time();events.append(event)
    Path('results/manifests/execution.json').write_text(json.dumps(dict(started=start,events=events,finished=time.time()),indent=2))
if __name__=='__main__':main()
