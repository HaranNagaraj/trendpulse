import os
import pandas as pd
import numpy as np

def run_analysis():
    # Step 1: Load and Explore
    input_file = os.path.join("data", "trends_clean.csv")
    
    if not os.path.exists(input_file):
        print(f"Error: {input_file} not found.")
        return

    df = pd.read_csv(input_file)
    print(f"Loaded data: {df.shape}\n")

    print("First 5 rows:")
    print(df.head())
    print()

    # Calculate average score and average comments using Pandas/NumPy
    avg_score = df["score"].mean()
    avg_comments = df["num_comments"].mean()

    print(f"Average score    : {avg_score:,.0f}" if avg_score >= 1000 else f"Average score    : {avg_score:.2f}")
    print(f"Average comments : {avg_comments:,.0f}" if avg_comments >= 1000 else f"Average comments : {avg_comments:.2f}")
    print("\n--- NumPy Stats ---")

    # Step 2: Basic Analysis with NumPy
    scores = df["score"].to_numpy()
    
    mean_score = np.mean(scores)
    median_score = np.median(scores)
    std_score = np.std(scores)
    max_score = np.max(scores)
    min_score = np.min(scores)

    print(f"Mean score     : {mean_score:,.0f}" if mean_score >= 1000 else f"Mean score     : {mean_score:.2f}")
    print(f"Median score   : {median_score:,.0f}" if median_score >= 1000 else f"Median score   : {median_score:.2f}")
    print(f"Std deviation  : {std_score:,.0f}" if std_score >= 1000 else f"Std deviation  : {std_score:.2f}")
    print(f"Max score      : {max_score:,.0f}")
    print(f"Min score      : {min_score}")
    print()

    # Category with most stories
    top_category = df["category"].mode()[0]
    top_category_count = (df["category"] == top_category).sum()
    print(f"Most stories in: {top_category} ({top_category_count} stories)\n")

    # Story with the most comments
    max_comment_idx = df["num_comments"].idxmax()
    most_commented_title = df.loc[max_comment_idx, "title"]
    most_commented_count = df.loc[max_comment_idx, "num_comments"]
    print(f'Most commented story: "{most_commented_title}" - {most_commented_count:,} comments\n')

    # Step 3: Add New Columns
    # engagement = num_comments / (score + 1)
    df["engagement"] = df["num_comments"] / (df["score"] + 1)

    # is_popular = True if score > average score, else False
    df["is_popular"] = df["score"] > avg_score

    # Step 4: Save the Result
    output_path = os.path.join("data", "trends_analysed.csv")
    df.to_csv(output_path, index=False)
    print(f"Saved to {output_path}")

if __name__ == "__main__":
    run_analysis()