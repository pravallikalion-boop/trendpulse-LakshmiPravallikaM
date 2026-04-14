import pandas as pd
import matplotlib.pyplot as plt
import os

print("🚀 Running Task 4...")

# -------------------------------
# Load file
# -------------------------------
file_path = "data/trends_analysed.csv"

if not os.path.exists(file_path):
    print("❌ File not found:", file_path)
    exit()

df = pd.read_csv(file_path)

# -------------------------------
# Create outputs folder
# -------------------------------
os.makedirs("outputs", exist_ok=True)
print("📁 outputs folder ready")

# -------------------------------
# Chart 1: Top 10 Stories
# -------------------------------
top10 = df.sort_values(by="score", ascending=False).head(10)
top10["title"] = top10["title"].apply(lambda x: x[:50] + "..." if len(x) > 50 else x)

plt.figure()
plt.barh(top10["title"], top10["score"])
plt.title("Top 10 Stories by Score")
plt.xlabel("Score")
plt.ylabel("Title")
plt.gca().invert_yaxis()
plt.savefig("outputs/chart1_top_stories.png")
plt.close()

print("✅ Chart 1 saved")

# -------------------------------
# Chart 2: Category count
# -------------------------------
counts = df["category"].value_counts()

plt.figure()
plt.bar(counts.index, counts.values)
plt.title("Stories per Category")
plt.xlabel("Category")
plt.ylabel("Count")
plt.savefig("outputs/chart2_categories.png")
plt.close()

print("✅ Chart 2 saved")

# -------------------------------
# Chart 3: Scatter
# -------------------------------
popular = df[df["is_popular"] == True]
not_popular = df[df["is_popular"] == False]

plt.figure()
plt.scatter(popular["score"], popular["num_comments"], label="Popular")
plt.scatter(not_popular["score"], not_popular["num_comments"], label="Not Popular")
plt.title("Score vs Comments")
plt.xlabel("Score")
plt.ylabel("Comments")
plt.legend()
plt.savefig("outputs/chart3_scatter.png")
plt.close()

print("✅ Chart 3 saved")

# -------------------------------
# Dashboard
# -------------------------------
fig, ax = plt.subplots(1, 3, figsize=(15, 5))

# chart 1
ax[0].barh(top10["title"], top10["score"])
ax[0].invert_yaxis()
ax[0].set_title("Top Stories")

# chart 2
ax[1].bar(counts.index, counts.values)
ax[1].set_title("Categories")

# chart 3
ax[2].scatter(popular["score"], popular["num_comments"])
ax[2].set_title("Score vs Comments")

plt.suptitle("TrendPulse Dashboard")
plt.savefig("outputs/dashboard.png")
plt.close()

print("✅ Dashboard saved")

print("\n🎉 ALL FILES CREATED IN outputs/")