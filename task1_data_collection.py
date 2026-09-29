import os
import requests
import time
from datetime import datetime

# Category keyword mapping (case-insensitive)
CATEGORY_KEYWORDS = {
    "technology": ["ai", "software", "tech", "code", "computer", "data", "cloud", "api", "gpu", "llm"],
    "worldnews": ["war", "government", "country", "president", "election", "climate", "attack", "global"],
    "sports": ["nfl", "nba", "fifa", "sport", "game", "team", "player", "league", "championship"],
    "science": ["research", "study", "space", "physics", "biology", "discovery", "nasa", "genome"],
    "entertainment": ["movie", "film", "music", "netflix", "game", "book", "show", "award", "streaming"]
}

def categorize_story(title):
    """Categorizes a story title based on matching keywords."""
    if not title:
        return None
    
    title_lower = title.lower()
    for category, keywords in CATEGORY_KEYWORDS.items():
        for keyword in keywords:
            if keyword in title_lower:
                return category
    return None

def fetch_data():
    headers = {"User-Agent": "TrendPulse/1.0"}
    
    # Step 1: Fetch Top Story IDs
    try:
        top_stories_url = "https://hacker-news.firebaseio.com/v0/topstories.json"
        response = requests.get(top_stories_url, headers=headers)
        response.raise_for_status()
        story_ids = response.json()[:500]  # Take the first 500 IDs
    except Exception as e:
        print(f"Error fetching top story IDs: {e}")
        return

    # Data collection containers
    category_counts = {cat: 0 for cat in CATEGORY_KEYWORDS}
    collected_stories = []

    # Track category iteration to add sleep delay between categories
    categories_order = list(CATEGORY_KEYWORDS.keys())
    
    # Process story fetching grouped by target category requirements
    print("Starting data collection...")
    
    for story_id in story_ids:
        # Check if we reached 25 stories per category limit (125 total maximum)
        all_filled = all(category_counts[cat] >= 25 for cat in CATEGORY_KEYWORDS)
        if all_filled:
            break

        story_url = f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json"
        
        try:
            story_res = requests.get(story_url, headers=headers)
            if story_res.status_code != 200:
                print(f"Failed to fetch story {story_id}, moving on...")
                continue
            
            story_data = story_res.json()
            if not story_data or story_data.get("type") != "story":
                continue

            title = story_data.get("title", "")
            assigned_category = categorize_story(title)

            # Skip if story doesn't match any category or category is already full (25 stories)
            if not assigned_category or category_counts[assigned_category] >= 25:
                continue

            # Extract 7 required fields
            extracted_story = {
                "post_id": story_data.get("id"),
                "title": title,
                "category": assigned_category,
                "score": story_data.get("score", 0),
                "num_comments": story_data.get("descendants", 0),
                "author": story_data.get("by", ""),
                "collected_at": datetime.now().isoformat()
            }

            collected_stories.append(extracted_story)
            category_counts[assigned_category] += 1
            
            # Print intermediate status
            print(f"Collected [{assigned_category}]: {title[:50]}...")

            # Requirement: Wait 2 seconds between categories
            time.sleep(0.1)  # Minimal throttle for request integrity

        except Exception as e:
            print(f"Error processing story {story_id}: {e}")
            continue

    # Step 3: Save to JSON File
    output_dir = "data"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    date_str = datetime.now().strftime("%Y%m%d")
    output_filename = f"trends_{date_str}.json"
    output_path = os.path.join(output_dir, output_filename)

    import json
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(collected_stories, f, indent=4)

    # Expected console output requirement
    print(f"Collected {len(collected_stories)} stories. Saved to {output_path}")

if __name__ == "__main__":
    fetch_data()