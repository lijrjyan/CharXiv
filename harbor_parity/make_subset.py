"""Build the Harbor parity subset of the CharXiv validation split.

Writes data/{descriptive,reasoning}_val.json and data/image_metadata_val.json
restricted to the 100 chart ids in parity_figure_ids.txt (the ids used by the
Harbor adapter's ``--split parity``: random.Random(42).sample of the 1,000
validation charts) into <out>/data, and copies the matching charts into
<out>/images. Run from the repository root after downloading the images to
./images (see the main README).

    python harbor_parity/make_subset.py --out parity_run1
"""

import argparse
import json
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True, help="output run directory")
    ap.add_argument("--image_dir", default=os.path.join(ROOT, "images"))
    args = ap.parse_args()

    with open(os.path.join(HERE, "parity_figure_ids.txt")) as f:
        ids = [line.strip() for line in f if line.strip()]
    os.makedirs(os.path.join(args.out, "data"), exist_ok=True)
    os.makedirs(os.path.join(args.out, "images"), exist_ok=True)
    for mode in ("descriptive", "reasoning"):
        with open(os.path.join(ROOT, "data", f"{mode}_val.json")) as f:
            data = json.load(f)
        with open(os.path.join(args.out, "data", f"{mode}_val.json"), "w") as f:
            json.dump({k: data[k] for k in ids}, f)
    shutil.copy(
        os.path.join(ROOT, "data", "image_metadata_val.json"),
        os.path.join(args.out, "data", "image_metadata_val.json"),
    )
    for k in ids:
        shutil.copy(
            os.path.join(args.image_dir, f"{k}.jpg"),
            os.path.join(args.out, "images", f"{k}.jpg"),
        )
    if not os.path.lexists(os.path.join(args.out, "src")):
        os.symlink(os.path.join(ROOT, "src"), os.path.join(args.out, "src"))
    print(f"{len(ids)} charts -> {args.out}")


if __name__ == "__main__":
    main()
