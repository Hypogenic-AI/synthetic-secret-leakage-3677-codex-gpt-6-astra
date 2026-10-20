# Cloned author repositories

Read-only reference clones; none installed into the project environment or run against a model. No user-specified repositories were provided.

| Repository | Local path | Commit | Purpose |
|---|---|---|---|
|https://github.com/HumanCompatibleAI/tensor-trust|tensor-trust/|f0b055451415e23d444703fbb8a47daf1d4b2c3c|Official game, extraction benchmark creation, evaluation metrics|
|https://github.com/deepseek-ai/DeepSeek-R1|DeepSeek-R1/|0cf78561f1d51c84a21b2190626b21116d5c68bb|Official model documentation, licenses and deployment examples|
|https://github.com/y0mingzhang/prompt-extraction|prompt-extraction/|dc00b2f6d3cef1a2b9c85fe67b8fa2d3354e21cf|COLM 2024 extraction and confidence-estimation reference implementation|

Tensor Trust: reviewed root and data-pipeline READMEs, data-pipeline/setup.py and src/ttdata/eval_extraction.py. `access_code_in_output` implements lowercased substring matching; `single_model_eval` pairs extraction with valid-code access. Related files: data-pipeline/src/ttdata/eval_metrics.py, eval_prompt_extraction_detection.py, create_extraction_robustness_dataset.py. Pipeline depends on pandas/pyarrow/torch/transformers, cloud SDKs and PostgreSQL; urllib3 is pinned <1.27, incompatible with this project's modern requests dependency. The web application additionally needs Django/Redis/Node. Do not install the full stack to run a small custom experiment. Upstream run-pipeline initial-load requires a private SQL dump; public benchmark files avoid that dependency. Code MIT license; data license separately unspecified.

DeepSeek-R1: README is documentation, not an inference engine. Use vLLM/Transformers separately in the isolated environment if feasible; use the model's own tokenizer config. README usage guidance recommends temperature 0.5–0.7, no system prompt, and a thinking prefix. See experiment_protocol.md for the explicit policy deviation. Distill-Llama-8B derives from Llama-3.1-8B; review upstream Llama licensing as well as repository MIT terms. The repository PDF is excluded by sparse checkout; papers/ holds the downloaded scientific PDF.

Prompt-extraction: README, requirements and key file layout reviewed. Entry points: src/evaluate-extraction.py, src/hf-prompt-extraction.py, src/llama-chat-prompt-extraction.py, src/finetune-similarity-predictor.py. Requirements include torch, transformers, bitsandbytes, accelerate and legacy openai==0.28; installing wholesale is unnecessary. Llama-2 chat serialization is not suitable for DeepSeek-R1 unchanged. No learned leakage detector weights were downloaded. Sparse checkout omits bundled data/ and attacks/ to keep the code reference separate from evaluation data. MIT license.

Reproduction from workspace root (run pwd first):
```bash
pwd
git clone --depth 1 https://github.com/HumanCompatibleAI/tensor-trust.git code/tensor-trust
git clone --depth 1 https://github.com/deepseek-ai/DeepSeek-R1.git code/DeepSeek-R1
git clone --depth 1 https://github.com/y0mingzhang/prompt-extraction.git code/prompt-extraction
```
These commands fetch current HEAD. To reproduce this snapshot, fetch each listed commit and checkout it detached; apply sparse-checkout exclusions described above. Clones are git-ignored in the parent workspace; this catalog retains provenance.
