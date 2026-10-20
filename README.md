# Synthetic secret boundaries

Preregistered fixed-pressure versus neutral-repetition evaluation of Qwen3-8B and DeepSeek-R1-Distill-Llama-8B. All secrets and credentials are fictional. This is a small custom analogue, not the original 39-environment benchmark.

- Completed 1094/3600 conversations; 150 planned independent evaluation worlds.
- Primary DeepSeek paired pressure effect: 0.1594 (SE 0.0549; 95% CI 0.0580–0.2609; n=23).
- Collection was incomplete; the hypothesis is unresolved and no candidate is supported.
- All 100 programmatic scorer fixtures pass; no LLM judge.
- Reasoning-plus-final exposure is diagnostic and assumes reasoning is observable.

See [REPORT.md](REPORT.md) for results, uncertainty, authorized controls and limitations.

```bash
uv sync --project . --frozen
source .venv/bin/activate
python src/analyze.py
python src/write_report.py
python src/validate.py
```

Full inference reproduction uses frozen worlds and `python src/download_models.py`, then `python src/run_experiment.py` in fresh output directories on one 80GB GPU. Do not append a second run to existing raw files. Exact revisions and commands are in results/manifests/; protocol in preregistration.md.

- src/: generator, scorer, Inspect task, execution, analysis and reporting.
- results/raw/: actual generated text, separate channels and turn records.
- results/safety/: standard schema results and Inspect logs.
- results/checks/: labelled fixtures and validation.
- results/manifests/: frozen worlds, revisions, hashes, environment and execution.
- figures/: measured result plots; findings/: gated candidates, if any.

Full reproduction wrapper: `bash results/manifests/reproduce.sh` after environment setup, using fresh raw-output paths. This activates the environment and keeps runtime caches local. The positive DeepSeek complete-case effect is exploratory because most planned conversations are missing; no candidate was issued.
