# task1_dataCollection.py

import requests
import time
import json
import os
from datetime import datetime

# User-Agent to avoid request blocking
headers = {"User-Agent": "Mozilla/5.0"}

# Categories and keywords mapping
CATEGORIES = {
    "technology": ["ai", "software", "tech", "code", "computer", "data", "cloud", "api", "gpu", "llm"],
    "worldnews": ["war", "government", "country", "president", "election", "climate", "attack", "global"],
    "sports": ["nfl", "nba", "fifa", "sport", "game", "team", "player", "league", "championship"],
    "science": ["research", "study", "space", "physics", "biology", "discovery", "nasa", "genome"],
    "entertainment": ["movie", "film", "music", "netflix", "game", "book", "show", "award", "streaming"]
}

# Function to assign category based on title
def get_category(title):
    title = title.lower()
    for category, keywords in CATEGORIES.items():
        for word in keywords:
            if word in title:
                return category
    return "general"  # fallback category


# Function to fetch data from Hacker News API
def fetch_data():
    url = "https://hacker-news.firebaseio.com/v0/topstories.json"

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # ensure no HTTP error
        ids = response.json()[:200]  # limit for speed
    except Exception as e:
        print("❌ Error fetching story IDs:", e)
        return []

    collected = []

    # Track category counts
    category_count = {cat: 0 for cat in CATEGORIES}
    category_count["general"] = 0

    # Loop through story IDs
    for story_id in ids:
        try:
            res = requests.get(
                f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json",
                headers=headers
            )

            data = res.json()

            # Skip if no data
            if not data or "title" not in data:
                continue

            category = get_category(data["title"])

            # Limit per category (max 25)
            if category_count.get(category, 0) < 25:

                # Create story object with required 7 fields
                story = {
                    "post_id": data.get("id"),
                    "title": data.get("title"),
                    "category": category,
                    "score": data.get("score", 0),
                    "num_comments": data.get("descendants", 0),
                    "author": data.get("by"),
                    "collected_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }

                # Validate all required fields
                required_fields = ["post_id", "title", "category", "score", "num_comments", "author", "collected_at"]

                if all(story[field] is not None for field in required_fields):
                    collected.append(story)
                    category_count[category] += 1

                    print(f"✅ Added: {story['title'][:50]}...")

                # Stop when 100 stories collected
                if len(collected) >= 100:
                    break

            # Small delay to avoid API overload
            time.sleep(0.1)

        except Exception as e:
            print(f"❌ Error fetching story {story_id}: {e}")

    return collected


# Function to save JSON file
def save_json(data):
    try:
        os.makedirs("data", exist_ok=True)

        filename = f"data/trends_{datetime.now().strftime('%Y%m%d')}.json"

        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

        print("\n🎉 SUCCESS!")
        print(f"📊 Collected {len(data)} stories")
        print(f"📁 File saved at: {filename}")

        # Final validations
        if len(data) >= 100:
            print("✅ 100+ stories collected")
        else:
            print("⚠️ Less than 100 stories collected")

        # Check fields
        required_fields = ["post_id", "title", "category", "score", "num_comments", "author", "collected_at"]

        valid = all(all(field in d and d[field] is not None for field in required_fields) for d in data)

        if valid:
            print("✅ All stories have required fields")
        else:
            print("❌ Some stories missing fields")

    except Exception as e:
        print("❌ Error saving file:", e)


# Main execution
if __name__ == "__main__":
    print("🚀 Starting data collection...\n")

    data = fetch_data()

    print(f"\nDEBUG → Total collected: {len(data)}")

    save_json(data)

    print("\n✅ Script finished successfully!")