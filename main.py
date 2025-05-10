from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, HttpUrl
from typing import List, Dict, Optional
import json
import os

app = FastAPI(title="YouTube Video Organizer", version="v1")


# Data Models
class VideoEntry(BaseModel):
    title: str
    url: HttpUrl
    watched: bool = False

    # Add this method to make the model JSON serializable
    def dict(self, *args, **kwargs):
        d = super().dict(*args, **kwargs)
        d["url"] = str(d["url"])  # Convert HttpUrl to string
        return d


class CategoryVideos(BaseModel):
    videos: List[VideoEntry]


# File operations
JSON_FILE = "videos.json"


def initialize_json_file():
    """Create an empty JSON file if it doesn't exist or is corrupted"""
    if not os.path.exists(JSON_FILE) or os.path.getsize(JSON_FILE) == 0:
        with open(JSON_FILE, "w", encoding="utf-8") as f:
            json.dump({}, f)
    else:
        try:
            with open(JSON_FILE, "r", encoding="utf-8") as f:
                json.load(f)  # Try to load to check if it's valid
        except json.JSONDecodeError:
            # Backup the corrupted file
            backup_file = f"{JSON_FILE}.bak"
            print(f"Backing up corrupted {JSON_FILE} to {backup_file}")
            os.rename(JSON_FILE, backup_file)
            # Create a new empty file
            with open(JSON_FILE, "w", encoding="utf-8") as f:
                json.dump({}, f)


def load_videos() -> Dict:
    """Load videos from JSON file, with error handling"""
    initialize_json_file()  # Make sure the file exists and is valid
    with open(JSON_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_videos(data: Dict):
    """Save videos to JSON file"""
    # Ensure the data is JSON serializable
    serializable_data = {}
    for category, videos in data.items():
        serializable_data[category] = [
            {
                "title": video["title"],
                "url": str(video["url"]),  # Convert URL to string
                "watched": video["watched"],
            }
            for video in videos
        ]

    with open(JSON_FILE, "w", encoding="utf-8") as f:
        json.dump(serializable_data, f, indent=2)


@app.get("/categories")
async def get_categories():
    """Get all categories"""
    videos = load_videos()
    return {"categories": list(videos.keys())}


@app.get("/categories/{category}")
async def get_category_videos(category: str):
    """Get all videos in a category"""
    videos = load_videos()
    if category not in videos:
        raise HTTPException(status_code=404, detail="Category not found")
    return {category: videos[category]}


@app.post("/categories/{category}/videos")
async def add_video(category: str, video: VideoEntry):
    videos = load_videos()  # Load the entire existing data

    if category not in videos:
        videos[category] = []

    # Check for duplicate URLs
    if any(v["url"] == str(video.url) for v in videos[category]):
        raise HTTPException(status_code=400, detail="Video URL already exists")

    videos[category].append(
        {"title": video.title, "url": str(video.url), "watched": video.watched}
    )

    save_videos(videos)  # Save the entire updated data
    return {"message": "Video added successfully"}


@app.get("/videos")
async def get_video_by_url(url: str):
    """Get detailed information about a specific video using its URL"""
    videos = load_videos()

    # Search for the video in all categories
    for category, video_list in videos.items():
        for video in video_list:
            if video["url"] == url:
                return {
                    "category": category,
                    "video": {
                        "title": video["title"],
                        "url": video["url"],
                        "watched": video["watched"],
                    },
                }

    # If video not found, raise 404 error
    raise HTTPException(status_code=404, detail="Video not found")


@app.put("/categories/{category}/videos")
async def update_video(category: str, url: str, video: VideoEntry):
    """Update a video by URL"""
    videos = load_videos()
    if category not in videos:
        raise HTTPException(status_code=404, detail="Category not found")

    video_dict = {"title": video.title, "url": str(video.url), "watched": video.watched}

    for idx, v in enumerate(videos[category]):
        if v["url"] == url:
            videos[category][idx] = video_dict
            save_videos(videos)
            return {"message": "Video updated successfully"}
    raise HTTPException(status_code=404, detail="Video not found")


@app.delete("/categories/{category}/videos")
async def delete_video(category: str, url: str):
    """Delete a video by URL"""
    videos = load_videos()
    if category not in videos:
        raise HTTPException(status_code=404, detail="Category not found")

    initial_length = len(videos[category])
    videos[category] = [v for v in videos[category] if v["url"] != url]

    if len(videos[category]) == initial_length:
        raise HTTPException(status_code=404, detail="Video not found")

    save_videos(videos)
    return {"message": "Video deleted successfully"}


@app.patch("/categories/{category}/videos/watched")
async def toggle_watched(category: str, url: str):
    """Toggle watched status by URL"""
    videos = load_videos()
    if category not in videos:
        raise HTTPException(status_code=404, detail="Category not found")

    for v in videos[category]:
        if v["url"] == url:
            v["watched"] = not v["watched"]
            save_videos(videos)
            return {"message": "Watched status toggled successfully"}

    raise HTTPException(status_code=404, detail="Video not found")


# Initialize the JSON file when the app starts
@app.on_event("startup")
async def startup_event():
    initialize_json_file()
