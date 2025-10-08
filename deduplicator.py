import os
import csv

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent
DEPTREE_PATH = REPO_ROOT / 'deptrees' / 'Go'
OUTPUT_FILE = REPO_ROOT / 'go_dedup_deps.csv'

all_deps = set()
total = 0

for subdir in DEPTREE_PATH.iterdir():
    deps_file = subdir / 'deps.csv'
    if deps_file.exists():
        with open(deps_file, newline='') as f:
            reader = csv.reader(f)
            header = next(reader, None) # THe header is PACKAGE,VERSION
            for row in reader:
                total += 1
                if len(row) == 2:
                    package, version = row
                    all_deps.add((package.strip(), version.strip()))

with open(OUTPUT_FILE, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['PACKAGE', 'VERSION'])
    for package, version in sorted(all_deps):
        writer.writerow([package, version])

print(f"Dedup deps written in file: {OUTPUT_FILE}")
print(f"Count of deduplicated dependencies: {len(all_deps)}")
print(f"Total undeduped dependencies: {total}")