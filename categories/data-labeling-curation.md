# Data Labeling & Curation

Use this category for programs where Jev annotates, filters, deduplicates, or triages data at scale, replacing slower or costlier human and LLM labeling steps.

## Submission format

```md
- [Name](URL) - Industry: one-sentence description of the Jev use case.
```

## Entries

- [jev-align (Sutro)](https://github.com/sutro-sh/jev-align) - Dataset engineering: evaluates CSV, Parquet, and JSONL rows with Jev `Choice`, `Score`, or `Boolean` decisions, sends ambiguous and audit samples to a human, and uses accepted human labels to optimize the saved definition with GEPA.
- [jev-curate](https://github.com/AkashPriyadarshii/jev-curate) - Dataset engineering: sifts synthetic JSONL and Parquet rows using Jev Noul checks and calibrated confidence scores, streaming passed records and rejections straight to disk.
- [typeful-triage](https://github.com/cephalization/jev-triage) - Open-source maintenance: multiplayer triage dashboard where Jev answers a fixed set of typed questions per issue — kind, severity, urgency, duplicate, and next step — and every human correction is kept and shown back to the model on later runs.
- [jlink](https://github.com/keltokhy/jlink) - Research data: links records under a plain-English match rule using Jev Noul pair judgments, with local candidate blocking and match resolution.
- [jgrep](https://github.com/keltokhy/jgrep) - Data filtering: filters text, structured records, functions, and diff hunks against plain-English descriptions using Jev Noul judgments.
- [jevgrep (allebee)](https://github.com/allebee/jevgrep) - Log triage: filters logs and other text streams, including live `tail -f` output, by asking Jev one Noul per line against a plain-English question and printing lines at or above a probability threshold, with a hand-labelled benchmark against Claude in the repository.
- [jev-research-pipeline](https://github.com/shimo4228/jev-research-pipeline) - Research monitoring: asks Jev Noul gates and Score dimensions per (paper, research question) on each daily fetch through Pydantic AI's typesafe model, keeps sources above a code-side threshold, and hands them to Qwen for question-centric Obsidian notes; offline tests replay recorded cassettes.
- [GroundingJev](https://github.com/xyzzzh/GroundingJev) - Visual annotation: a Jev-inspired Qwen3.5-0.8B model that maps an image and referring expression to four bounding-box coordinates in one forward pass, reporting an 8.61× inference speedup over its autoregressive base model.
