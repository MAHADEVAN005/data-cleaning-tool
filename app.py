import streamlit as st
import pandas as pd
from data_cleaner import clean_csv

# ---------------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------------
st.set_page_config(
    page_title="Automatic Data Cleaning Tool",
    page_icon="🧼",
    layout="wide",
)

# ---------------------------------------------------------
# THEME TOGGLE
# ---------------------------------------------------------
st.sidebar.markdown("## 🎨 Theme Settings")

dark_mode = st.sidebar.toggle("🌙 Enable Dark Mode", value=True)

# ---------------------------------------------------------
# CLEAN CSS INJECTION  (NO TEXT LEAK)
# ---------------------------------------------------------
if dark_mode:
    bg_css = """
    <style>
        .stApp {
            background: linear-gradient(135deg, #0f172a, #020617);
            color: #f1f5f9 !important;
        }
        h1,h2,h3,h4,h5,p,div,span {
            color: #f1f5f9 !important;
        }
        .upload-box {
            border: 2px dashed #38bdf8 !important;
            background: rgba(56,189,248,0.10) !important;
            border-radius: 16px;
            padding: 20px;
        }
        .logo-box {
            background: linear-gradient(135deg,#6366f1,#ec4899);
            width: 70px;
            height: 70px;
            border-radius: 18px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 28px;
            font-weight: 900;
            color: white;
            box-shadow: 0 4px 30px rgba(99,102,241,0.7);
        }
    </style>
    """
else:
    bg_css = """
    <style>
        .stApp {
            background: linear-gradient(135deg, #ffffff, #eef2ff);
            color: #020617 !important;
        }
        h1,h2,h3,h4,h5,p,div,span {
            color: #020617 !important;
        }
        .upload-box {
            border: 2px dashed #3b82f6 !important;
            background: rgba(191,219,254,0.40) !important;
            border-radius: 16px;
            padding: 20px;
        }
        .logo-box {
            background: linear-gradient(135deg,#3b82f6,#ec4899);
            width: 70px;
            height: 70px;
            border-radius: 18px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 28px;
            font-weight: 900;
            color: white;
            box-shadow: 0 4px 30px rgba(59,130,246,0.7);
        }
    </style>
    """

st.markdown(bg_css, unsafe_allow_html=True)

# ---------------------------------------------------------
# HEADER
# ---------------------------------------------------------
colL, colR = st.columns([1, 6])

with colL:
    st.markdown('<div class="logo-box">MD</div>', unsafe_allow_html=True)

with colR:
    st.markdown("""
    <h1>✨ Automatic CSV Cleaning Tool</h1>
    <p style='opacity:0.75;'>Smart Cleaning • Missing Value Insights • Charts • Profiling</p>
    """, unsafe_allow_html=True)

st.write("")

# ---------------------------------------------------------
# UPLOAD SECTION
# ---------------------------------------------------------

st.markdown("### 📤 Upload Your File")

colA, colB = st.columns([2, 1])

with colA:
    st.markdown('<div class="upload-box">', unsafe_allow_html=True)
    uploaded = st.file_uploader(
        "Drag or Browse Files",
        type=["csv", "xlsx", "json", "tsv"],
        label_visibility="collapsed",
    )
    st.markdown('</div>', unsafe_allow_html=True)

with colB:
    st.markdown("#### ✔ Supported Formats")
    st.write("• CSV\n• Excel (.xlsx)\n• JSON\n• TSV")
    st.caption("Max ~200MB per file")

st.write("")

# ---------------------------------------------------------
# LOAD FILE
# ---------------------------------------------------------
df = None
cleaned_df = None
missing_info = {}

if uploaded:
    ext = uploaded.name.split(".")[-1].lower()
    try:
        if ext == "csv":
            df = pd.read_csv(uploaded)
        elif ext == "xlsx":
            df = pd.read_excel(uploaded)
        elif ext == "json":
            df = pd.read_json(uploaded)
        elif ext == "tsv":
            df = pd.read_csv(uploaded, sep="\t")
    except:
        st.error("❌ Unable to read file.")

# ---------------------------------------------------------
# RAW PREVIEW
# ---------------------------------------------------------
if df is not None:
    st.markdown("### 👀 Raw Data Preview")
    st.dataframe(df.head(200), use_container_width=True)

    df.to_csv("raw_temp.csv", index=False)

    if st.button("✨ Clean & Analyze Data", type="primary", use_container_width=True):
        missing_info = clean_csv("raw_temp.csv", "cleaned_output.csv")
        cleaned_df = pd.read_csv("cleaned_output.csv")

# ---------------------------------------------------------
# CLEANED OUTPUT
# ---------------------------------------------------------
if cleaned_df is not None:
    st.markdown("### 🧼 Cleaned Data")
    st.dataframe(cleaned_df, use_container_width=True)

    st.write("")
    st.markdown("### 📊 Missing Value Summary")

    if not missing_info:
        st.success("🎉 No missing values found in original dataset!")
    else:
        for col, rows in missing_info.items():
            st.markdown(f"**❗ {col} — {len(rows)} missing**")
            for r in rows:
                st.write(f"- Row {r['row']} → Name: {r['name']}")

    st.write("")
    st.markdown("### ⬇️ Download Cleaned CSV")

    with open("cleaned_output.csv", "rb") as f:
        st.download_button(
            label="💾 Download Cleaned File",
            data=f,
            file_name="cleaned_data.csv",
            mime="text/csv",
            use_container_width=True
        )
