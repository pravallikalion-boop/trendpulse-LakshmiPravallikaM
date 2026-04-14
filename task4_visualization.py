import pandas as pd
import numpy as np
import os

# Load cleaned data
file_path = "data/trends_clean.csv"

if not os.path.exists(file_path):
    print("❌ File not found:", file_path)
    exit()

df = pd.read_csv(file_path)

print(f"Loaded data: {df.shape}\n")

# Averages
avg_score = df["score"].mean()
avg_comments = df["num_comments"].mean()

print("Average score   :", int(avg_score))
print("Average comments:", int(avg_comments))


# -------------------------------
# NumPy Analysis
# -------------------------------

scores = df["score"].values

print("\n--- NumPy Stats ---")
print("Mean score   :", int(np.mean(scores)))
print("Median score :", int(np.median(scores)))
print("Std deviation:", int(np.std(scores)))
print("Max score    :", int(np.max(scores)))
print("Min score    :", int(np.min(scores)))

# Category with most stories
top_category = df["category"].value_counts().idxmax()
top_count = df["category"].value_counts().max()

print(f"\nMost stories in: {top_category} ({top_count} stories)")

# Most commented story
top_story = df.loc[df["num_comments"].idxmax()]

print(f"\nMost commented story: \"{top_story['title']}\" — {top_story['num_comments']} comments")


# -------------------------------
# Add new columns
# -------------------------------

df["engagement"] = df["num_comments"] / (df["score"] + 1)
df["is_popular"] = df["score"] > avg_score


# -------------------------------
# SAVE FILE (IMPORTANT)
# -------------------------------

output_path = "data/trends_analysed.csv"
df.to_csv(output_path, index=False)

print(f"\n✅ Saved to {output_path}")