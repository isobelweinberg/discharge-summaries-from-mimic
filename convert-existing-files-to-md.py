import os
from pathlib import Path
output_dir = "data/mimic-iv-clinical-database-demo-2.2/output-data"

for file in os.listdir(output_dir):
    if file.endswith(".txt"):
        stem, ext = os.path.splitext(file)
        full_file_path = os.path.join(output_dir, file)
        full_stem_path = os.path.join(output_dir, stem + ".md")
        os.rename(full_file_path, full_stem_path)