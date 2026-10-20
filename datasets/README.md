# Dataset resources

Two downloaded benchmark files, from the author’s Hugging Face mirror `qxcv/tensor-trust`, pinned at revision `4de2b2fe01ba0cb6fbf7cbb9f1a3fabaf8157372`. URLs and SHA-256 hashes are in manifest.json. Data is local but ignored by git; documentation, manifest, and small samples are tracked. No credentials are needed.

| File | Rows | Bytes | Schema / purpose |
|---|---:|---:|---|
|tensor_trust_extraction.jsonl|570|685113|sample_id, pre_prompt, attack, post_prompt, access_code; external extraction benchmark|
|tensor_trust_detection.jsonl|230|160942|sample_id, access_code, llm_output, is_prompt_extraction; human-labeled detector audit|
|synthetic_cases.jsonl|1760|see filesystem|440 items × authorization (2) × pressure (2), five planned turns|
|no_secret_controls.jsonl|40|see filesystem|negative controls, expected synthetic token absent from input|

Download/reproduce from workspace root:
```bash
pwd
uv sync --project .
.venv/bin/python scripts/download_datasets.py
.venv/bin/python scripts/prepare_synthetic.py
```
Loading:
```python
import json
rows = [json.loads(line) for line in open('datasets/tensor_trust_extraction.jsonl')]
```

Extraction data has unique IDs, no nulls, two empty pre-prompts and 105 empty post-prompts. Empty prompt segments are valid optional fields. Detection data has 115 positives and 115 negatives, unique IDs and no empty/null fields. Case-insensitive full-code matching yields TP=48, FN=67, TN=115, FP=0, because human labels include indirect disclosures. This is not a model experiment. See notes/data_validation.json. The PDF reports 569 extraction examples; the downloaded v1 file has 570. Use the pinned artifact count.

No training split exists for these benchmark files. Do not train on them or tune an attack on reported evaluation items. Synthetic fixtures explicitly separate 40 pilot from 400 evaluation items; all four conditions for an item share secret, context, and seed. Pilot and evaluation secrets are disjoint. Four context labels vary a fixed policy template: results generalize over sampled synthetic tokens in this protocol, not an unlimited population of defenses. All tokens are fabricated and public fixtures, never real credentials.

The benchmark has no matched fixed-pressure/neutral or permission-to-disclose arms, so it cannot alone identify the proposed causal effect. It is retained for method grounding and detector auditing. The primary fixtures are custom because those missing controls are essential to the hypothesis; this is not a replacement claim for the original benchmark. Neutral turns still ask for the secret, while pressure adds insistence; the first turn is identical.

License: the data repository and HF metadata retrieved do not state an explicit data license. Do not infer a data license from the separately MIT-licensed code; retain provenance and clarify before redistribution. Synthetic fixture code is original project work; no upstream data is embedded in generated fixtures.

Examples: extraction_sample.json, detection_sample.json, synthetic_sample.json, each under 100 KB. The source code repository’s bundled attack/data folders are excluded by sparse checkout to keep datasets in this directory. No Kaggle/UCI fallback was needed after finding the directly relevant author benchmark on Hugging Face. Large raw game dumps (~99 MB compressed attacks) were not required or downloaded.
