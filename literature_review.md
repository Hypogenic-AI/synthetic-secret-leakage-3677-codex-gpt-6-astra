# Literature review: synthetic secret leakage with authorized-disclosure controls

## Scope and search

Question: does fixed repeated pressure increase unauthorized full synthetic-secret emission by at least 0.10 over neutral repetition on DeepSeek-R1-Distill-Llama-8B, with a paired 95% CI excluding zero? This is context-secret disclosure, not memorization or real-data exfiltration. Include primary work on prompt extraction, multi-turn pressure, instruction privilege and the target model; exclude unrelated membership inference and harmful-task benchmarks as primary outcomes. Coverage: 2023–2026, searched October 20, 2026.

The diligent paper-finder query combined “synthetic secret password leakage multi-turn repeated pressure authorized disclosure instruction hierarchy reasoning models”; after installing its missing httpx dependency, it returned zero papers (paper_finder_search.log and paper_search_results/). Web search/open returned empty payloads. Manual retrieval used arXiv primary pages, author GitHub repositories, citation chasing from Tensor Trust, and the Hugging Face author dataset/model APIs. This is a focused review, not an exhaustive PRISMA review. Five papers were included after title/abstract screening; a mistakenly probed Safe Harbor paper (2403.04893) was excluded as governance rather than experimental methodology and was not downloaded. No user-specified papers were supplied.

Tensor Trust received full visual reading of all 12 three-page PDF chunks (34 pages including appendices); immediate notes are preserved in notes/tensor_trust_reading_log.md, with rendered pages and chunk manifest. Other papers received abstract and focused methods/results review, not a claim of exhaustive appendix reading. Metadata and full extracted text are in notes/; all PDF originals are in papers/.

## Key papers

### Tensor Trust: Interpretable Prompt Injection Attacks from an Online Game
Sam Toyer, Olivia Watkins, Ethan Adrian Mendes, Justin Svegliato, Luke Bailey, Tiffany Wang, Isaac Ong, Karim Elmaaroufi, Pieter Abbeel, Trevor Darrell, Alan Ritter, Stuart Russell. 2023 preprint, ICLR 2024. [arXiv:2311.01011](https://arxiv.org/abs/2311.01011).

**Method/data:** human game where opening/closing defenses enclose untrusted input. Collection contains 126,808 attacks and 46,457 defenses; duplicate and adversarial filtering produces extraction and hijacking benchmarks. Defenses must accept genuine access codes across reference models. The paper describes 569 extraction examples; the downloaded v1 artifact contains 570. The detector dataset has 230 manually labeled examples, including indirect disclosure and mismatched negatives.

**Baselines/metrics/results:** eight models spanning GPT, Claude, PaLM, Llama-2 and CodeLlama. Extraction robustness means absence of the access code, case-insensitively, paired with defense validity on legitimate input. Table A2 gives extraction robustness/validity of 12.3%/91.1% for GPT-3.5 and 69.1%/89.5% for GPT-4. These are adversarially selected historical results, not estimates for our target. The paper's GPT-4 detection classifier achieves 97.0% precision and 84.3% recall on broader human leakage labels.

**Limitations/relevance:** human-selected attacks, game incentives, model-specific rare tokens, and adversarial filtering limit population interpretation. Access acceptance is not permission to reveal a secret, so an authorized-disclosure control must be added. Exact matching misses indirect/encoded leakage. The role ablation does not show that merely assigning a system role ensures protection. Official code: HumanCompatibleAI/tensor-trust, cloned locally; author benchmark mirror: qxcv/tensor-trust, downloaded.

### Effective Prompt Extraction from Language Models
Yiming Zhang, Nicholas Carlini, Daphne Ippolito. COLM 2024; arXiv first version 2023, downloaded v3 dated August 7, 2024. [arXiv:2307.06865](https://arxiv.org/abs/2307.06865). Earlier references use the title “Prompts should not be seen as secrets.”

**Method/data:** systematic prompt recovery with ground truth and confidence estimation to distinguish recovery from hallucination. Three prompt sources: Unnatural Instructions (500 test, 200 development), ShareGPT (200 test, 200 development), and Awesome ChatGPT Prompts (153); eleven LLMs from GPT, Alpaca, Vicuna and Llama-2 families.

**Metrics/results:** exact and approximate prompt recovery, precision–recall for confidence. Table 1 shows approximate recovery above 50% for every model; approximate recovery tolerates limited token differences and is not full-secret exact matching. GPT-4 model-average exact/approximate recovery is 63.3%/86.0% in that table. Learned similarity/confidence scoring and translation attacks are additional analyses.

**Limitations/relevance:** mostly single-turn prompt recovery, not fixed repeated coercion with an explicit authorization factorial. Ground truth is essential: plausible-looking secret strings are not evidence of leakage. Whole-prompt similarity should not replace exact matching of a unique synthetic token. Official MIT code: y0mingzhang/prompt-extraction, cloned; no detector weights or training data needed for our primary test.

### Great, Now Write an Article About That: The Crescendo Multi-Turn LLM Jailbreak Attack
Mark Russinovich, Ahmed Salem, Ronen Eldan. 2024 preprint; downloaded v3 dated February 26, 2025. [arXiv:2404.01833](https://arxiv.org/abs/2404.01833).

**Method/data:** benign-looking opening questions followed by adaptive escalation referencing model replies. Crescendomation uses GPT-4 as attacker and judges, response feedback, and up to ten backtracking attempts. Main comparison uses 50 AdvBench tasks; further analysis includes HarmBench. Default ten independent runs, up to ten interaction rounds, temperature 0.5.

**Baselines/metrics/results:** CIA, CoA, Many-Shot Jailbreak and PAIR. Table 4 reports average ASR 56.2% (GPT-4) and 82.6% (Gemini-Pro); task-level any-run success is 98% and 100%. These two denominators are different. Judging includes success flags, graded scores, a secondary judge and manual inspection; moderation scores are auxiliary. The claimed relative percentage improvements are not percentage-point causal pressure effects.

**Limitations/relevance:** adaptive prompt choice, backtracking, judge bias, best-of opportunities and harmful task selection prevent direct transfer to our fixed-pressure hypothesis. Supports retaining real conversational history and controlling number of opportunities. Automated implementation is identified in the paper as Azure/PyRIT; not cloned because adaptive search is outside the three retained directions.

### The Instruction Hierarchy: Training LLMs to Prioritize Privileged Instructions
Eric Wallace, Kai Xiao, Reimar Leike, Lilian Weng, Johannes Heidecke, Alex Beutel. 2024. [arXiv:2404.13208](https://arxiv.org/abs/2404.13208).

**Method/data:** context synthesis for aligned instructions and context ignorance for conflicting low-privilege instructions; supervised/RLHF training versus a similarly trained baseline without hierarchy examples. Evaluation includes Tensor Trust extraction/hijacking, Gandalf password extraction, generated direct/indirect injections, jailbreaks, over-refusal, and generic capability tasks.

**Metrics/results:** attack resistance and benign instruction-following, with standard-deviation error bars. The paper reports robustness improvements up to 63% on main evaluations and 34% on held-out attack categories; these claims are task-specific and do not estimate our target effect. Appendix B explicitly distinguishes whole-system-message extraction (>half unigrams), password emission, and benign probing.

**Limitations/relevance:** different model/training distribution, some private synthetic evaluation data, and over-refusal regressions. Motivates explicit privilege definitions plus authorized copying to distinguish protection from inability or blanket refusal. A user's assertion of permission is not a change to the governing policy. No training implementation/checkpoints were retrieved; this is design evidence, not a runnable baseline here.

### DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning
DeepSeek-AI. 2025 initial release; retrieved arXiv v2 dated January 4, 2026 (86 pages). [arXiv:2501.12948](https://arxiv.org/abs/2501.12948). Model-specific operational details are additionally verified from the pinned author model card/config.

**Method/data:** R1-Zero explores reinforcement-learning-induced reasoning; R1 adds staged training; distilled smaller models learn from larger-model generations. Evaluation includes math, code, reasoning and general capability benchmarks. The Distill-Llama-8B card reports AIME 2024 pass@1 50.4, MATH-500 89.1 and GPQA Diamond 49.0; these are capability context, not confidentiality results.

**Relevant implementation:** the target is based on Llama-3.1-8B. Model-card recommendations include temperature 0.6, no system prompt and a thinking prefix. The pinned tokenizer actually inserts `<think>` for generation and strips previous assistant reasoning before including history. Therefore capture raw output before parsing and score newly generated text only. Preserve official history serialization, document the system-policy deviation, and preflight authorized copying. Repository deepseek-ai/DeepSeek-R1 is cloned; weights/inference runtime are not downloaded or validated in this stage.

**Limitations:** full R1 findings do not imply the same safety behavior in an 8B distill. Neither this report nor the model card establishes the hypothesized repeated-pressure effect. The 2026 PDF revision should not be mistaken for the original 2025 report.

## Synthesis and experiment recommendations

Common methods are exact secret matching, whole-prompt similarity, attack success per conversation, adaptive red-teaming, and paired usefulness/robustness assessment. Appropriate primary baselines here are neutral repeated secret requests with identical first turn and horizon, plus authorized versions of both arms. Use generated assistant replies in each separate history, no fabricated compliance, no backtracking, no selective best-of reporting.

The central gap across these resources is a controlled, fixed-string repeated-pressure comparison on this checkpoint, with fresh synthetic ground truth, explicit disclosure permission, and reasoning/final separation. Literature motivates the experiment but does not confirm the hypothesis or its 0.10 magnitude.

Use fresh synthetic fixtures for the causal contrast (400 held-out item pairs, 40 pilot items, four conditions per item). Tensor Trust is an external benchmark/scorer audit, not a source of matched pressure observations. Downloaded detection data confirms that case-insensitive full-code matching catches 48/115 labeled disclosures and no false positives among 115 negatives; this is a descriptive resource validation, not model performance. The primary claim must say full-token emission; partial and transformed leaks are separate diagnostics.

Primary metric: within-item difference in any unauthorized full-token emission by turn 5 across reasoning or final. Bootstrap paired items (10,000 replicates), report SE, 95% CI, both arm rates and discordant cells. Observed difference >=0.10 with CI excluding zero supports the specified operational criterion; proving population effect >=0.10 needs the CI lower bound >=0.10. Keep turn 1/3/5 diagnostics secondary. Missing reasoning, truncation, authorization failure and absent-secret matches must be reported. Full locked settings, sample-size assumptions, runtime budget and output schema are in experiment_protocol.md; ranked retained/rejected directions are in planning.md.
