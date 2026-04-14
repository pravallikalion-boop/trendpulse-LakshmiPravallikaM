import pandas as pd
import os

# 🔹 Step 1: Load JSON
file_path = "data/trends_20260414.json"   # 👉 change date if needed

if not os.path.exists(file_path):
    print("❌ File not found:", file_path)
    exit()

df = pd.read_json(file_path)

print(f"Loaded {len(df)} stories from {file_path}\n")

# 🔹 Step 2: Clean Data

# Remove duplicates
df = df.drop_duplicates(subset=["post_id"])
print(f"After removing duplicates: {len(df)}")

# Remove missing values
df = df.dropna(subset=["post_id", "title", "score"])
print(f"After removing nulls: {len(df)}")

# Fix data types
df["score"] = df["score"].astype(int)
df["num_comments"] = df["num_comments"].astype(int)

# Remove low quality (score < 5)
df = df[df["score"] >= 5]
print(f"After removing low scores: {len(df)}")

# Strip whitespace from title
df["title"] = df["title"].str.strip()

# 🔹 Step 3: Save CSV
output_path = "data/trends_clean.csv"

df.to_csv(output_path, index=False)

print(f"\nSaved {len(df)} rows to {output_path}")

# 🔹 Summary
print("\nStories per category:")
print(df["category"].value_counts())