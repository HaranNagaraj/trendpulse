import os
import glob
import pandas as pd

def process_data():
    # Step 1: Find and Load JSON File from data/ folder
    data_dir = "data"
    json_files = glob.glob(os.path.join(data_dir, "trends_*.json"))
    
    if not json_files:
        print("Error: No trends_YYYYMMDD.json file found in data/ directory.")
        return

    # Pick the latest generated JSON file
    input_file = json_files[0]
    df = pd.read_json(input_file)
    print(f"Loaded {len(df)} stories from {input_file}\n")

    # Step 2: Clean the Data
    
    # 2.1 Remove Duplicates (based on post_id)
    df = df.drop_duplicates(subset=["post_id"])
    print(f"After removing duplicates: {len(df)}")

    # 2.2 Missing values — drop rows where post_id, title, or score is missing
    df = df.dropna(subset=["post_id", "title", "score"])
    print(f"After removing nulls: {len(df)}")

    # 2.3 Low quality — remove stories where score is less than 5
    df = df[df["score"] >= 5]
    print(f"After removing low scores: {len(df)}\n")

    # 2.4 Data types — make sure score and num_comments are integers
    df["score"] = df["score"].fillna(0).astype(int)
    df["num_comments"] = df["num_comments"].fillna(0).astype(int)

    # 2.5 Whitespace — strip extra spaces from the title column
    df["title"] = df["title"].astype(str).str.strip()

    # Step 3: Save as CSV and Print Summary
    output_path = os.path.join(data_dir, "trends_clean.csv")
    df.to_csv(output_path, index=False)
    
    print(f"Saved {len(df)} rows to {output_path}\n")

    # Print stories per category summary
    print("Stories per category:")
    category_summary = df["category"].value_counts()
    for cat, count in category_summary.items():
        print(f"  {cat:<15} {count}")

if __name__ == "__main__":
    process_data()