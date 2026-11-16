#!/bin/bash
# One original-side parity run: generate -> evaluate -> get_stats on the parity subset.
# usage (from the repository root): OPENAI_API_KEY=... harbor_parity/run_parity.sh parity_run1
set -euo pipefail
RUN=$1
M=${CHARXIV_MODEL:-gpt-4o-mini-2024-07-18}
python harbor_parity/make_subset.py --out "$RUN"
cd "$RUN"
for mode in descriptive reasoning; do
  python src/generate.py --model_name "$M" --model_path "$M" --model_api "$OPENAI_API_KEY" \
    --mode $mode --data_dir ./data --image_dir ./images --output_dir ./results
done
for mode in descriptive reasoning; do
  python src/evaluate.py --model_name "$M" --split val --mode $mode --api_key "$OPENAI_API_KEY"
done
python src/get_stats.py --model_name "$M" --split val
