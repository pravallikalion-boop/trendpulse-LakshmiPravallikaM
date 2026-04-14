import pandas as pd
import os

file_path = "data/trends_20260414.json"   # 👈 change if different

if not os.path.exists(file_path):
    print("❌ JSON file not found:", file_path)
    exit()

df = pd.read_json(file_path)

# cleaning
df = df.drop_duplicates(subset=["post_id"])
df = df.dropna(subset=["post_id", "title", "score"])
df["score"] = df["score"].astype(int)
df["num_comments"] = df["num_comments"].astype(int)
df = df[df["score"] >= 5]
df["title"] = df["title"].str.strip()

# save clean file
output_path = "data/trends_clean.csv"
df.to_csv(output_path, index=False)

print("✅ trends_clean.csv created successfully")