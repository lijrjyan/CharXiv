# CharXiv parity fork for the Harbor adapter

This branch is upstream CharXiv at `7ebe88f` with the minimum changes needed to
run the original side of the parity experiment for the Harbor CharXiv adapter
([harbor-framework/adapters#85](https://github.com/harbor-framework/adapters/pull/85)).

## Changes to upstream code

1. **Judge model** (`src/descriptive_utils.py`, `src/reasoning_utils.py`): upstream
   hard-codes `gpt-4o-2024-05-13`, which OpenAI has retired. The judge is now read
   from `CHARXIV_JUDGE_MODEL` and defaults to `gpt-4o-2024-08-06`, the same default
   as the Harbor verifier.
2. **Descriptive grading batch** (`src/evaluate.py`): `nq_per_query=1`, one question
   per judge call, because each Harbor task is graded on its own. The prompt
   template is unchanged.
3. **OpenAI base URL** (`src/generate_lib/gpt.py`): read from `OPENAI_BASE_URL`
   (default `https://api.openai.com/v1`) so that an API proxy can be used.

Generation, prompts, call parameters, retries and scoring are otherwise upstream's.

## Running

Download the images into `./images` as described in the main README, install
`openai requests tqdm`, then run each of the three runs in its own directory:

```bash
export OPENAI_API_KEY=...
for r in 1 2 3; do harbor_parity/run_parity.sh parity_run$r; done
```

`parity_figure_ids.txt` lists the 100 validation charts of the adapter's
`--split parity` subset (all 5 questions per chart: 400 descriptive + 100
reasoning). Accuracy per metric is the fraction of `score == 1` in
`parity_run*/results/scores-<model>-{descriptive,reasoning}_val.json`.

## Reported runs (2026-11-16, gpt-4o-mini-2024-07-18)

| Metric | Run 1 | Run 2 | Run 3 |
|---|---|---|---|
| descriptive accuracy (%) | 74.5 | 73.5 | 75.0 |
| reasoning accuracy (%) | 33.0 | 36.0 | 34.0 |
