import json

INPUT_FILE = "playlist_58353859-cfbc-4d37-9796-11877808c8fb.json"
OUTPUT_FILE = "playlist_58353859-cfbc-4d37-9796-11877808c8fb_stripped.json"

with open(INPUT_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

videos = data.get("videos", [])

stripped_videos = []
for video in videos:
    # Only keep 'title' and 'url'
    stripped_video = {k: video[k] for k in ("title", "url") if k in video}
    stripped_videos.append(stripped_video)

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump({"videos": stripped_videos}, f, ensure_ascii=False, indent=2)

print(f"Stripped file saved to {OUTPUT_FILE}")
