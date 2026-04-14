# task2_clean_data.py

import pandas as pd
import os

# -------------------------------
# Load JSON file
# -------------------------------

file_path = "data/trends_20260414.json"  # 👈 change date if needed

if not os.path.exists(file_path):
    print("❌ JSON file not found:", file_path)
    exit()

# Load JSON into DataFrame
df = pd.read_json(file_path)

print(f"Loaded {len(df)} rows from JSON\n")


# -------------------------------
# Remove duplicates
# -------------------------------

df = df.drop_duplicates(subset=["post_id"])
print(f"After removing duplicates: {len(df)}")


# -------------------------------
# Remove missing values
# -------------------------------

df = df.dropna(subset=["post_id", "title", "score"])
print(f"After removing nulls: {len(df)}")


# -------------------------------
# Fix data types
# -------------------------------

df["score"] = df["score"].astype(int)
df["num_comments"] = df["num_comments"].astype(int)


# -------------------------------
# Remove low quality (score < 5)
# -------------------------------

df = df[df["score"] >= 5]
print(f"After removing low scores: {len(df)}")


# -------------------------------
# Clean text (remove extra spaces)
# -------------------------------

df["title"] = df["title"].str.strip()


# -------------------------------
# Save cleaned CSV
# -------------------------------

output_path = "data/trends_clean.csv"
df.to_csv(output_path, index=False)

print(f"\n✅ Saved {len(df)} rows to {output_path}")


# -------------------------------
# Stories per category summary
# -------------------------------

print("\nStories per category:")
print(df["category"].value_counts())