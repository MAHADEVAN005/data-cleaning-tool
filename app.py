import streamlit as st
import pandas as pd
from data_cleaner import clean_csv
import os

st.title("🧼 Automatic CSV Cleaning Tool")

uploaded = st.file_uploader("Upload your CSV file", type=["csv"])

# We define missing_report = None outside the button
missing_report = None  

if uploaded:
    st.subheader("🔍 Raw Data Preview")
    df = pd.read_csv(uploaded)
    st.write(df)

    raw_path = "raw_uploaded.csv"
    df.to_csv(raw_path, index=False)

    if st.button("✨ Clean Data"):
        output_path = "cleaned_output.csv"

        # clean_csv returns missing report now
        missing_report = clean_csv(raw_path, output_path)

        cleaned_df = pd.read_csv(output_path)

        st.subheader("✅ Cleaned Data Preview")
        st.write(cleaned_df)

        st.download_button(
            label="⬇️ Download Cleaned CSV",
            data=open(output_path, "rb"),
            file_name="cleaned_data.csv",
            mime="text/csv"
        )

        # Missing Summary Box
        st.subheader("📊 Missing Values Summary")

        if missing_report:
            for col, items in missing_report.items():
                st.markdown(f"### ❗ {col} — {len(items)} missing")

                for entry in items:
                    st.write(
                        f"- Row **{entry['row']}** — Name: **{entry['name']}**"
                    )
        else:
            st.success("No missing values found!")
