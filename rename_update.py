import os, json, re

# ⚙️ 설정값
BASE_URL = "https://github.com/hy2025yj/its_not_popup/assets"  # 🔥 수정하세요
ASSETS_DIR = "assets"
POSTS_FILE = "posts.json"
OUTPUT_FILE = "posts_updated.json"

# --- 파일 이름 정리 함수 ---
def normalize_filename(folder_idx, idx, ext):
    """폴더 번호와 순번으로 파일명 통일"""
    return f"{folder_idx:02d}_{idx+1}{ext.lower()}"

# --- 폴더 내 파일 리네이밍 ---
def rename_assets():
    folder_map = {}  # {folder_name: [새 파일명 리스트]}
    for folder_name in sorted(os.listdir(ASSETS_DIR)):
        folder_path = os.path.join(ASSETS_DIR, folder_name)
        if not os.path.isdir(folder_path):
            continue

        files = [f for f in os.listdir(folder_path) if not f.startswith(".")]
        files.sort()
        new_names = []

        for i, old_name in enumerate(files):
            ext = os.path.splitext(old_name)[1]
            new_name = normalize_filename(int(folder_name), i, ext)
            old_path = os.path.join(folder_path, old_name)
            new_path = os.path.join(folder_path, new_name)

            # rename 수행
            os.rename(old_path, new_path)
            new_names.append(new_name)
            print(f"✅ {old_name} → {new_name}")

        folder_map[folder_name] = new_names
    return folder_map

# --- posts.json 업데이트 ---
def update_posts(folder_map):
    with open(POSTS_FILE, "r", encoding="utf-8") as f:
        posts = json.load(f)

    for i, post in enumerate(posts, start=1):
        folder = f"{i:02d}"
        if folder not in folder_map:
            print(f"⚠️ Warning: {folder} not found in assets/")
            continue

        new_image_urls = [f"{BASE_URL}/{folder}/{fn}" for fn in folder_map[folder]]
        post["images"] = new_image_urls

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(posts, f, ensure_ascii=False, indent=2)
    print(f"\n🎉 Done! Updated JSON saved → {OUTPUT_FILE}")

# --- 실행 ---
if __name__ == "__main__":
    print("🔧 Start renaming and updating posts.json...")
    folder_map = rename_assets()
    update_posts(folder_map)
