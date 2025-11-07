# rename_folders.py
import os

root = "assets_raw"   # 다운로드 받은 원본 폴더
dest = "assets"       # 새로 정리된 폴더

os.makedirs(dest, exist_ok=True)
folders = [f for f in os.listdir(root) if os.path.isdir(os.path.join(root, f))]

for i, name in enumerate(sorted(folders), start=1):
    newname = f"{i:02d}"
    os.rename(os.path.join(root, name), os.path.join(dest, newname))
    print(f"{name} → {newname}")

