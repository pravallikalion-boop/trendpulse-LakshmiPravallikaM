# task1_datacollection.py

import requests
import time
import json
import os
from datetime import datetime

headers = {"User-Agent": "Mozilla/5.0"}  

CATEGORIES = {
    "technology": ["ai", "software", "tech", "code", "computer", "data", "cloud", "api", "gpu", "llm"],
    "worldnews": ["war", "government", "country", "president", "election", "climate", "attack", "global"],
    "sports": ["nfl", "nba", "fifa", "sport", "game", "team", "player", "league", "championship"],
    "science": ["research", "study", "space", "physics", "biology", "discovery", "nasa", "genome"],
    "entertainment": ["movie", "film", "music", "netflix", "game", "book", "show", "award", "streaming"]
}


def get_category(title):
    title = title.lower()
    for category, keywords in CATEGORIES.items():
        for word in keywords:
            if word in title:
                return category
    return "general"  


def fetch_data():
    url = "https://hacker-news.firebaseio.com/v0/topstories.json"
    
    try:
        ids = requests.get(url, headers=headers).json()[:200]  # limit for speed
    except Exception as e:
        print("❌ Error fetching IDs:", e)
        return []

    collected = []
    
    # include general category
    category_count = {cat: 0 for cat in CATEGORIES}
    category_count["general"] = 0

    for story_id in ids:
        try:
            res = requests.get(
                f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json",
                headers=headers
            )

            data = res.json()

            if not data or "title" not in data:
                continue

            category = get_category(data["title"])

            # ✅ allow general + avoid strict filtering
            if category_count.get(category, 0) < 25:

                story = {
                    "post_id": data.get("id"),
                    "title": data.get("title"),
                    "category": category,
                    "score": data.get("score", 0),
                    "num_comments": data.get("descendants", 0),
                    "author": data.get("by"),
                    "collected_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }

                collected.append(story)
                category_count[category] += 1

                print(f"✅ Added: {data['title'][:60]}...")  # debug

                # stop if enough data collected
                if len(collected) >= 100:
                    break

            time.sleep(0.1)

        except Exception as e:
            print(f"❌ Error fetching {story_id}: {e}")

    return collected


def save_json(data):
    try:
        os.makedirs("data", exist_ok=True)

        filename = f"data/trends_{datetime.now().strftime('%Y%m%d')}.json"

        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

        print(f"\n🎉 SUCCESS!")
        print(f"📊 Collected {len(data)} stories")
        print(f"📁 File saved at: {filename}")

    except Exception as e:
        print("❌ Error saving file:", e)


if __name__ == "__main__":
    print(" Starting data collection...\n")

    data = fetch_data()

    print("\nDEBUG → Total collected:", len(data))  # important debug

    save_json(data)

    print("\n Script finished!")