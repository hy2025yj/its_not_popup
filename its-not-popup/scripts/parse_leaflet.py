# parse_leaflet.py
import re, json, os
from pathlib import Path

text_file = "leaflet.txt"  # 위 리플렛 내용을 저장한 텍스트 파일 경로
assets_dir = Path("../assets")

text = Path(text_file).read_text(encoding="utf-8")

# --- 1. 포스트 구분 ---
# "—---" 구분선 기준으로 분리
posts_raw = [p.strip() for p in re.split(r"—[-\s]+", text) if p.strip()]

posts = []
for idx, raw in enumerate(posts_raw, start=1):
    # 기본 구조
    post = {
        "id": f"{idx:02d}",
        "account": None,
        "likes": None,
        "date": None,
        "caption": None,
        "images": []
    }

    # --- 2. 필드 추출 ---
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

    # --- 3. 이미지 경로 매핑 ---
    folder = assets_dir / f"{idx:02d}"
    if folder.exists():
        imgs = sorted(
            [str(folder / f) for f in os.listdir(folder)
             if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp'))]
        )
        post["images"] = imgs

    posts.append(post)

# --- 4. JSON 저장 ---
Path("posts.json").write_text(json.dumps(posts, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"✔ posts.json 생성 완료 ({len(posts)}개 포스트)")

