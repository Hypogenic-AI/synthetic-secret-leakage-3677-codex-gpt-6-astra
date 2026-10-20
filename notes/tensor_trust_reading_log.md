# Literature review: synthetic secret leakage

## Reading record (in progress)
Tensor Trust chunk 1, pp.1–3: human game data contains 126,808 attacks (69,906 distinct) and 46,457 defenses (39,731 distinct). Opening and closing defenses surround attacker input. Successful legitimate access is tested during defense creation; this motivates a separate authorization capability check, though access-granting is not the same as permission to disclose a secret. Game collection used GPT-3.5 Turbo with temperature 0. Context-secret extraction is distinct from training-data memorization.

Tensor Trust chunk 2, pp.4–6: benchmarks adversarially filter defenses that accept legitimate codes across three reference models; extraction uses case-insensitive verbatim inclusion, paired with defense validity. Paper says 569 extraction examples; downloaded release has 570, so use downloaded count and document version discrepancy. Human detection set exposes indirect/partial leaks missed by exact match; GPT-4 detection reports 97% precision, 84% recall. These are historical paper results, not our scorer validation. Repeated characters are an attack category, not evidence for repeated conversational pressure.

Tensor Trust chunk 3, pp.7–9: eight model baselines; robustness must be read jointly with defense validity because weak instruction-following can look secure. Extraction and hijacking rankings differ. Message-role ablation on GPT-3.5 finds little improvement from system roles alone; do not assume that transfers to this target. Longer replies may disclose more instructions; output budgets and truncation must be recorded.

Tensor Trust chunk 4, pp.10–12: transfer demonstrations are qualitative and sometimes manually adapted; they cannot estimate our fixed-pressure effect. Prior games include Gandalf and prompt-attack competitions. Human-designed attacks are interpretable but collection incentives and GPT-3.5-specific artifacts limit transfer. Consent/research governance and reference list are included here.

Tensor Trust chunk 5, pp.13–15: references include 'Prompts should not be seen as secrets' (Zhang & Ippolito). Appendix distinguishes exact access-grant regex scoring from extraction scoring. Player histories encourage adaptation and sharing, so raw attacks are not independent randomized repeated-pressure observations. Rank restrictions and moderation further shape the collection.

Tensor Trust chunk 6, pp.16–18: data cleanup excludes inappropriate material and names. Table A2 reports extraction robustness 12.3% for GPT-3.5 and 69.1% for GPT-4, with defense validity 91.1% and 89.5% respectively, on adversarially selected examples. Baseline input serializations differ by model. These results are not neutral-population leakage rates and should not be used as target effect priors without qualification.

Tensor Trust chunk 7, pp.19–21: extraction generation cap was 200 tokens versus 30 for hijacking, underscoring budget confounding. Detection set has 230 examples, manual review, indirect/riddle/translation cases, and deliberately mismatched hard negatives; it is scorer calibration data, not a natural prevalence sample. GPT-4 detection accuracy 90.9%, precision 97.0%, recall 84.3%. LDA is descriptive rather than causal evidence.

Tensor Trust chunk 8, pp.22–24: taxonomy examples and transfer tests compare direct requests with attack prefixes and a dummy unrelated-text prefix. Dummy-prefix success can be substantial, supporting a neutral repetition control rather than comparing only with no interaction. Transfer tasks differ from secret disclosure and provide no evidence about this checkpoint.

Tensor Trust chunk 9, pp.25–27: screenshots illustrate answer-prefix transfer and repeated-character language effects. These are selected examples, not paired conversational trials. No additional benchmark or model-target evidence for the proposed effect.

Tensor Trust chunk 10, pp.28–30: further manually adapted transfer demonstrations and screenshots. Their harmful-task content is not needed for this synthetic benchmark; reuse extraction methodology only. Qualitative success examples do not establish prevalence or causal pressure effects.

Tensor Trust chunk 11, pp.31–33: transfer screenshots and representative defenses. Some user-created access codes themselves contain instructions, motivating fresh alphanumeric synthetic secrets instead of unfiltered human access codes. Delimiters and closing reminders are present but do not constitute a guaranteed privilege boundary.

Tensor Trust chunk 12, p.34: 100-sample message-role ablation, five serializations; table extraction robustness spans 27–35% (prose says 27–32%, a minor inconsistency). Composite example combines roleplay, repeated characters, and updated-instruction framing, making attribution impossible without controlled component comparisons. All 12 chunks/34 pages visually reviewed; no claim that selected screenshots are independent trials.
