import re, json, os
from pathlib import Path

# 설정
TEXT_FILE = "leaflet.txt"   # 리플렛 내용 텍스트 파일
ASSETS_DIR = Path("assets") # 이미지 폴더가 있는 경로 (01, 02, ...)
OUTPUT_FILE = "posts.json"

# 텍스트 읽기
text = Path(TEXT_FILE).read_text(encoding="utf-8")

# --- 1. 포스트 블록 분리 (—--- 같은 구분선)
posts_raw = [p.strip() for p in re.split(r"—[-\s]+", text) if p.strip()]

# --- 2. 이미지 폴더 목록 (01, 02, 03, ...)
folders = sorted([f for f in ASSETS_DIR.iterdir() if f.is_dir()])
if len(posts_raw) != len(folders):
    print(f"⚠️ 경고: 텍스트({len(posts_raw)})개 vs 폴더({len(folders)})개 불일치")

posts = []
for idx, raw in enumerate(posts_raw, start=1):
    folder = folders[idx-1] if idx-1 < len(folders) else None
    post_id = f"{idx:02d}"

    post = {
        "id": post_id,
        "account": None,
        "likes": None,
        "date": None,
        "caption": None,
        "images": []
    }

    # 계정, 날짜, 좋아요, 캡션 추출
    acc = re.search(r"계정\s*이름[:：]\s*(.+)", raw)
    date = re.search(r"날짜[:：]\s*(.+)", raw)
    like = re.search(r"좋아요[:：]\s*(.+)", raw)
    cap = re.search(r"캡션[:：]\s*(.*)", raw, re.S)

    if acc: post["account"] = acc.group(1).strip()
    if date: post["date"] = date.group(1).strip()
    if like:
        val = like.group(1).strip()
        post["likes"] = val if not val.isdigit() else int(val)
    if cap:
        caption = cap.group(1).strip()
        post["caption"] = caption.replace("\n", "\n").strip()

    # --- 3. 이미지 파일 탐색 (폴더명 = 순번)
    if folder and folder.exists():
        imgs = sorted([
            str(folder.as_posix() + "/" + f)
            for f in os.listdir(folder)
            if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp'))
        ])
        post["images"] = imgs

    posts.append(post)

# --- 4. JSON 저장
Path(OUTPUT_FILE).write_text(json.dumps(posts, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"✔ posts.json 생성 완료 ({len(posts)}개 포스트)")

