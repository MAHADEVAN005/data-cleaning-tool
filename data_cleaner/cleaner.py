import pandas as pd
import os

def clean_csv(input_path, output_path):
    print("\n🔄 Loading file...")
    df = pd.read_csv(input_path)

    # -------------------------------------------
    # 1️⃣ FIND MISSING VALUES BEFORE CLEANING
    # -------------------------------------------
    missing_report = {}

    # Identify name-like column BEFORE renaming
    name_col = None
    for col in df.columns:
        if col.lower() in ["name", "full_name", "customer", "person"]:
            name_col = col
            break

    # Collect missing row info
    for col in df.columns:
        missing_rows = df[df[col].isna()]
        if len(missing_rows) > 0:
            missing_report[col] = []
            for idx, row in missing_rows.iterrows():
                missing_report[col].append({
                    "row": idx,
                    "name": row[name_col] if name_col else None
                })

    # -------------------------------------------
    # 2️⃣ CLEANING PROCESS
    # -------------------------------------------

    print("✨ Standardizing column names...")
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )

    print("🧹 Removing duplicates...")
    removed_duplicates = df.duplicated().sum()
    df = df.drop_duplicates()

    print("🩹 Handling missing values...")
    for col in df.columns:
        if df[col].dtype in ["int64", "float64"]:
            df[col].fillna(df[col].median(), inplace=True)
        else:
            df[col].fillna(df[col].mode()[0], inplace=True)

    print("📅 Converting date columns...")
    for col in df.columns:
        if df[col].dtype == "object":
            try:
                df[col] = pd.to_datetime(df[col], errors="raise")
            except:
                pass

    # -------------------------------------------
    # 3️⃣ SAVE FILE
    # -------------------------------------------

    print("💾 Saving cleaned file...")
    dir_name = os.path.dirname(output_path)
    if dir_name:
        os.makedirs(dir_name, exist_ok=True)

    df.to_csv(output_path, index=False)

    print("\n✅ CLEANING COMPLETE!")
    print(f"🚫 Duplicates Removed: {removed_duplicates}")
    print(f"📁 Cleaned File Saved To: {output_path}")

    # RETURN MISSING REPORT FOR UI
    return missing_report
