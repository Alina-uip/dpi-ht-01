import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
src = ROOT / "data" / "submission.json"
dst = ROOT / "submission.json"
shutil.copyfile(src, dst)
print(f"Copied {src.name} to /submission.json")
