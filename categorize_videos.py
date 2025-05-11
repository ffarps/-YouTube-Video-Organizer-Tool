import json
import re

INPUT_FILE = "playlist_58353859-cfbc-4d37-9796-11877808c8fb_stripped.json"
OUTPUT_FILE = "playlist_58353859-cfbc-4d37-9796-11877808c8fb_categorized.json"

CATEGORIES = [
    "Podcasts",
    "Clothes",
    "Productivity",
    "Self_Help",
    "Cameras",
    "Tech",
    "CyberSecurity",
    "Web_Development",
    "Software_Development",
    "AI",
    "AI_Development",
    "Personal_Finances",
    "Games",
    "Nutrition",
    "Guitar",
    "Watches",
    "Workouts",
    "Other",
    "Shows_and_Animes",
    "to_think"
]

# Simple keyword mapping for categories (can be expanded)
CATEGORY_KEYWORDS = {
    "Podcasts": ["podcast", "interview", "lex fridman", "episode"],
    "Clothes": ["clothes", "style", "fashion", "wardrobe", "outfit", "wear", "watches", "watch snob"],
    "Productivity": ["productivity", "focus", "work", "job", "career", "tips", "organize", "routine", "time management", "motivation", "boot time"],
    "Self_Help": ["self-help", "addiction", "confidence", "social media", "stop", "help", "improve", "overcome", "doom scrolling", "mental", "psychology"],
    "Cameras": ["camera", "photography", "dslr", "lens", "shoot", "video camera"],
    "Tech": ["tech", "technology", "server", "hardware", "nas", "gpu", "cuda", "linux", "bsd", "open source", "hosting", "vps", "cloud", "truenas", "deep learning", "ai", "nvidia", "git", "open source license"],
    "CyberSecurity": ["cybersecurity", "security", "hack", "scam", "phishing", "crypto", "privacy"],
    "Web_Development": ["web development", "web", "hosting", "server", "website", "html", "css", "javascript"],
    "Software_Development": ["software", "development", "programming", "code", "engineer", "git", "open source", "project", "build", "deploy"],
    "AI": ["ai", "artificial intelligence", "machine learning", "deep learning", "karpathy", "singularity", "neural", "cuda"],
    "AI_Development": ["ai development", "ai", "machine learning", "deep learning", "karpathy", "neural"],
    "Personal_Finances": ["finance", "money", "budget", "purchases", "invest", "affordable", "cheap", "finances"],
    "Games": ["game", "gaming", "playstation", "xbox", "nintendo", "video game"],
    "Nutrition": ["nutrition", "diet", "food", "health", "brain"],
    "Guitar": ["guitar", "music", "song", "ballad", "acoustic", "pocket guitar", "musician"],
    "Watches": ["watch", "watches", "timepiece"],
    "Workouts": ["workout", "exercise", "fitness", "gym", "training", "bootcamp"],
    "Shows_and_Animes": ["show", "anime", "series", "episode", "tv", "animes"],
    "to_think": ["think", "singularity", "brain", "psychology", "philosophy", "debate", "question", "why", "what is"]
}

def categorize_video(title):
    title_lower = title.lower()
    for category, keywords in CATEGORY_KEYWORDS.items():
        for kw in keywords:
            if kw in title_lower:
                return category
    return None

def main():
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    categorized = {cat: [] for cat in CATEGORIES}
    suggested_categories = {}

    for video in data["videos"]:
        title = video["title"]
        category = categorize_video(title)
        if category:
            categorized[category].append(video)
        else:
            # Fallback to 'Other' if no match
            categorized["Other"].append(video)

    output = {"categories": categorized}
    if suggested_categories:
        output["suggested_categories"] = suggested_categories

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"Categorized file saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
