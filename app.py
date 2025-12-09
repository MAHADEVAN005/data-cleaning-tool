import streamlit as st
import pandas as pd
import base64
from data_cleaner import clean_csv

# -------------------------------
# PAGE CONFIG + DARK MODE SWITCH
# -------------------------------
st.set_page_config(
    page_title="Automatic Data Cleaning Tool",
    page_icon="🧼",
    layout="wide"
)

# DARK MODE TOGGLE
dark = st.checkbox("🌙 Dark Mode", value=False)

if dark:
    st.markdown("""
        <style>
            body { background-color: #111111; color: white; }
            .stApp { background-color: #111111; }
            .card { 
                background-color: #1e1e1e;
                padding: 20px; 
                border-radius: 15px; 
                color: white; 
                box-shadow: 0 0 10px rgba(255,255,255,0.15);
            }
        </style>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
        <style>
            .card { 
                background-color: #ffffff;
                padding: 20px; 
                border-radius: 15px; 
                box-shadow: 0 0 10px rgba(0,0,0,0.1);
            }
        </style>
    """, unsafe_allow_html=True)

# -------------------------------
# LOGO + TITLE
# -------------------------------
logo_base64 = """
PHN2ZyB3aWR0aD0iNjQiIGhlaWdodD0iNjQiIHZpZXdCb3g9IjAgMCA2NCA2NCIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPGNpcmNsZSBjeD0iMzIiIGN5PSIzMiIgcj0iMzIiIGZpbGw9IiM0Mjg1RkYiLz4KPHBhdGggZD0iTTI1IDI4TDMwIDM0TDM5IDI0IiBzdHJva2U9IndoaXRlIiBzdHJva2Utd2lkdGg9IjQiLz4KPC9zdmc+
"""

st.markdown(
    f"""
    <div style="text-align:center;">
        <img src="data:image/svg+xml;base64,{logo_base64}" width="90">
        <h1 style="font-size:40px; margin-top:10px;">✨ Automatic CSV Cleaning Tool</h1>
        <p style="font-size:18px; opacity:0.8;">Smart Data Cleaning • Missing Value Report • One-Click Processing</p>
    </div>
    <br>
    """,
    unsafe_allow_html=True,
)

# -------------------------------
# FILE UPLOAD SECTION
# -------------------------------
st.markdown("### 📤 Upload Your File")

uploaded = st.file_uploader(
    "Drag & Drop or Browse",
    type=["csv", "xlsx", "json", "tsv"],
    help="Supported Formats: CSV, XLSX, JSON, TSV (Max 200 MB)"
)

st.markdown("""
**Supported File Types:**  
✔ CSV  
✔ Excel (.xlsx)  
✔ JSON  
✔ TSV  
""")

# -------------------------------
# PROCESS LOGIC
# -------------------------------
if uploaded:

    # READ BASED ON FORMAT
    ext = uploaded.name.split(".")[-1].lower()

    if ext == "csv":
        df = pd.read_csv(uploaded)
    elif ext == "xlsx":
        df = pd.read_excel(uploaded)
    elif ext == "json":
        df = pd.read_json(uploaded)
    elif ext == "tsv":
        df = pd.read_csv(uploaded, sep="\t")
    else:
        st.error("❌ Unsupported Format")
        st.stop()

    st.markdown("### 👀 Raw Data Preview")
    st.dataframe(df, use_container_width=True)

    raw_path = "raw_temp.csv"
    df.to_csv(raw_path, index=False)

    if st.button("✨ Clean Data"):
        cleaned_path = "cleaned_output.csv"

        # RUN CLEANING ENGINE
        missing_report = clean_csv(raw_path, cleaned_path)
        cleaned_df = pd.read_csv(cleaned_path)

        # -------------------------
        # CLEAN RESULT DISPLAY
        # -------------------------

        st.markdown("## 🧼 Cleaned Data Preview")
        st.dataframe(cleaned_df.style.highlight_null(null_color="red"), use_container_width=True)

        # -------------------------
        # DOWNLOAD CLEANED FILE
        # -------------------------
        with open(cleaned_path, "rb") as f:
            st.download_button(
                label="⬇️ Download Cleaned CSV",
                data=f,
                file_name="cleaned_data.csv",
                mime="text/csv"
            )

        # -------------------------
        # SUMMARY CARDS
        # -------------------------
        st.markdown("## 📊 Missing Values Summary")

        if not missing_report:
            st.success("🎉 No missing values found!")
        else:
            for col, rows in missing_report.items():
                st.markdown(
                    f"""
                    <div class="card">
                        <h3>❗ {col} — {len(rows)} missing</h3>
                        <ul>
                    """,
                    unsafe_allow_html=True
                )

                for entry in rows:
                    st.markdown(
                        f"""
                        <li>Row {entry['row']} — Name: {entry['name']}</li>
                        """,
                        unsafe_allow_html=True,
                    )

                st.markdown("</ul></div>", unsafe_allow_html=True)

# -------------------------------
# CONTACT SECTION
# -------------------------------

st.markdown("<br><hr>", unsafe_allow_html=True)

st.markdown("""
### 📞 Contact  
**Email:** mahadevankaliyappan@gmail.com  
**Phone:** +91 7708497524  
""")

