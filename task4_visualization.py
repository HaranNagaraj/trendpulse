import os
import pandas as pd
import matplotlib.pyplot as plt

def generate_visualizations():
    # 1. Setup
    input_file = os.path.join("data", "trends_analysed.csv")
    if not os.path.exists(input_file):
        print(f"Error: {input_file} not found.")
        return

    df = pd.read_csv(input_file)

    # Create outputs directory if it doesn't exist
    output_dir = "outputs"
    os.makedirs(output_dir, exist_ok=True)

    # -------------------------------------------------------------
    # 2. Chart 1: Top 10 Stories by Score (Horizontal Bar Chart)
    # -------------------------------------------------------------
    top_10 = df.nlargest(10, "score").sort_values("score", ascending=True)
    
    # Shorten titles longer than 50 characters
    top_10_titles = [
        title[:47] + "..." if len(title) > 50 else title 
        for title in top_10["title"]
    ]

    plt.figure(figsize=(10, 6))
    plt.barh(top_10_titles, top_10["score"], color="skyblue")
    plt.title("Top 10 Stories by Score")
    plt.xlabel("Score")
    plt.ylabel("Story Title")
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "chart1_top_stories.png"))
    plt.close()

    # -------------------------------------------------------------
    # 3. Chart 2: Stories per Category (Bar Chart)
    # -------------------------------------------------------------
    cat_counts = df["category"].value_counts()
    colors = ["#4C72B0", "#DD8452", "#55A868", "#C44E52", "#8172B3", "#937860"]

    plt.figure(figsize=(8, 5))
    bars = plt.bar(cat_counts.index, cat_counts.values, color=colors[:len(cat_counts)])
    plt.title("Stories per Category")
    plt.xlabel("Category")
    plt.ylabel("Number of Stories")
    plt.xticks(rotation=15)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "chart2_categories.png"))
    plt.close()

    # -------------------------------------------------------------
    # 4. Chart 3: Score vs Comments (Scatter Plot)
    # -------------------------------------------------------------
    plt.figure(figsize=(8, 5))
    
    popular = df[df["is_popular"] == True]
    non_popular = df[df["is_popular"] == False]

    plt.scatter(non_popular["score"], non_popular["num_comments"], color="gray", alpha=0.6, label="Non-Popular")
    plt.scatter(popular["score"], popular["num_comments"], color="crimson", alpha=0.8, label="Popular")
    
    plt.title("Score vs Comments")
    plt.xlabel("Score")
    plt.ylabel("Number of Comments")
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "chart3_scatter.png"))
    plt.close()

    # -------------------------------------------------------------
    # Bonus: Combined TrendPulse Dashboard (3 Plots in 1 Figure)
    # -------------------------------------------------------------
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))
    fig.suptitle("TrendPulse Dashboard", fontsize=16, fontweight="bold")

    # Subplot 1: Top Stories
    axes[0].barh(top_10_titles, top_10["score"], color="skyblue")
    axes[0].set_title("Top 10 Stories by Score")
    axes[0].set_xlabel("Score")

    # Subplot 2: Categories
    axes[1].bar(cat_counts.index, cat_counts.values, color=colors[:len(cat_counts)])
    axes[1].set_title("Stories per Category")
    axes[1].set_xlabel("Category")
    axes[1].set_ylabel("Count")
    axes[1].tick_params(axis='x', rotation=15)

    # Subplot 3: Score vs Comments
    axes[2].scatter(non_popular["score"], non_popular["num_comments"], color="gray", alpha=0.6, label="Non-Popular")
    axes[2].scatter(popular["score"], popular["num_comments"], color="crimson", alpha=0.8, label="Popular")
    axes[2].set_title("Score vs Comments")
    axes[2].set_xlabel("Score")
    axes[2].set_ylabel("Comments")
    axes[2].legend()

    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "dashboard.png"))
    plt.close()

    print("Successfully generated all charts and saved in 'outputs/' folder:")
    print(" - outputs/chart1_top_stories.png")
    print(" - outputs/chart2_categories.png")
    print(" - outputs/chart3_scatter.png")
    print(" - outputs/dashboard.png")

if __name__ == "__main__":
    generate_visualizations()