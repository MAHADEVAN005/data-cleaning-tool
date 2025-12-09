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
# GLOBAL COLOR THEMES
# ---------------------------------------------------------
LIGHT_BG = """
.stApp {
    background: linear-gradient(135deg, #ffffff 0%, #eef2ff 50%, #dbeafe 100%);
    color: #0f172a;
}
h1,h2,h3,h4,h5,p,span,div { color: #0f172a !important; }
.upload-zone > div > div {
    border-radius: 16px !important;
    border: 2px dashed #3b82f6 !important;
    background: rgba(191,219,254,0.35) !important;
}
"""
DARK_BG = """
.stApp {
    background: linear-gradient(135deg, #0f172a 0%, #020617 40%, #0f172a 100%);
    color: #f1f5f9;
}
h1,h2,h3,h4,h5,p,span,div { color: #f1f5f9 !important; }
.upload-zone > div > div {
    border-radius: 16px !important;
    border: 2px dashed #38bdf8 !important;
    background: rgba(56,189,248,0.10) !important;
}
"""

# ---------------------------------------------------------
# SIDEBAR: DARK MODE TOGGLE
# ---------------------------------------------------------
st.sidebar.markdown("## 🌗 Theme Settings")
dark_mode = st.sidebar.toggle("Enable Dark Mode", value=True)

if dark_mode:
    st.markdown(DARK_BG, unsafe_allow_html=True)
else:
    st.markdown(LIGHT_BG, unsafe_allow_html=True)

# ---------------------------------------------------------
# CUSTOM CSS (CARDS + ANIMATIONS)
# ---------------------------------------------------------
st.markdown(
    """
    <style>
        .main-card {
            padding: 24px 28px;
            border-radius: 18px;
            margin-bottom: 22px;
            border: 1px solid rgba(148,163,184,0.35);
            backdrop-filter: blur(10px);
            animation: fadeIn 0.6s ease-out;
        }
        .metric-card {
            padding: 14px 18px;
            border-radius: 16px;
            margin-bottom: 12px;
            background: rgba(255,255,255,0.07);
            border: 1px solid rgba(148,163,184,0.4);
            backdrop-filter: blur(8px);
            transition: 0.2s ease;
        }
        .metric-card:hover {
            transform: translateY(-4px);
            border-color: #38bdf8;
        }
        .section-card {
            padding: 16px;
            border-radius: 16px;
            background: rgba(255,255,255,0.08);
            border: 1px solid rgba(148,163,184,0.3);
            margin-bottom: 12px;
        }
        .missing-badge {
            padding: 5px 10px;
            font-size: 13px;
            border-radius: 999px;
            background: rgba(239,68,68,0.20);
            border: 1px solid rgba(239,68,68,0.45);
            color: #fecaca;
        }
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(16px); }
            to { opacity: 1; transform: translateY(0); }
        }
        /* ---------------- LOGO ---------------- */
        .header-logo {
            width: 70px;
            height: 70px;
            border-radius: 20px;
            background: conic-gradient(from 220deg, #38bdf8, #6366f1, #ec4899, #38bdf8);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 26px;
            font-weight: 900;
            color: white;
            animation: glowPulse 1.8s infinite alternate;
            box-shadow: 0 14px 40px rgba(56,189,248,0.65);
        }
        @keyframes glowPulse {
            from { box-shadow: 0 0 16px rgba(56,189,248,0.6); }
            to { box-shadow: 0 0 30px rgba(236,72,153,0.9); }
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------
# HEADER (LOGO = MD)
# ---------------------------------------------------------
colL, colR = st.columns([1, 5])
with colL:
    st.markdown('<div class="header-logo">MD</div>', unsafe_allow_html=True)

with colR:
    st.markdown(
        """
        <h1 style="margin-bottom:6px;">✨ Automatic CSV Cleaning Tool</h1>
        <p style="opacity:0.85;">Smart Cleaning • Missing Value Insights • Charts • Profiling</p>
        """,
        unsafe_allow_html=True,
    )

# ---------------------------------------------------------
# MAIN UPLOAD SECTION
# ---------------------------------------------------------
st.markdown('<div class="main-card">', unsafe_allow_html=True)
st.markdown("### 📤 Upload Your File")

col_upload, col_info = st.columns([2, 1])

with col_upload:
    st.markdown('<div class="upload-zone">', unsafe_allow_html=True)
    uploaded_file = st.file_uploader(
        "Drag & Drop or Browse",
        type=["csv", "xlsx", "json", "tsv"],
        label_visibility="collapsed",
    )
    st.markdown('</div>', unsafe_allow_html=True)

with col_info:
    st.markdown("##### 📁 Supported Formats")
    st.write("✔ CSV\n✔ Excel (.xlsx)\n✔ JSON\n✔ TSV")
    st.caption("Max: ~200MB")

# ---------------------------------------------------------
# READ FILE
# ---------------------------------------------------------
df = None
cleaned_df = None
missing_report = {}

if uploaded_file:
    ext = uploaded_file.name.split(".")[-1].lower()

    try:
        if ext == "csv":
            df = pd.read_csv(uploaded_file)
        elif ext == "xlsx":
            df = pd.read_excel(uploaded_file)
        elif ext == "json":
            df = pd.read_json(uploaded_file)
        elif ext == "tsv":
            df = pd.read_csv(uploaded_file, sep="\t")
    except Exception as e:
        st.error(f"❌ Error reading file: {e}")

# ---------------------------------------------------------
# RAW PREVIEW
# ---------------------------------------------------------
if df is not None:
    st.markdown("### 👀 Raw Data Preview")
    st.dataframe(df.head(200), use_container_width=True)

    df.to_csv("raw_temp.csv", index=False)

    if st.button("✨ Clean & Analyze Data", type="primary", use_container_width=True):
        missing_report = clean_csv("raw_temp.csv", "cleaned_output.csv")
        cleaned_df = pd.read_csv("cleaned_output.csv")

st.markdown("</div>", unsafe_allow_html=True)

# ---------------------------------------------------------
# AFTER CLEANING — UI SECTIONS
# ---------------------------------------------------------
if cleaned_df is not None:

    # ------------ METRICS ROW ----------------
    rows = len(cleaned_df)
    cols = len(cleaned_df.columns)
    missing_count = sum(len(v) for v in missing_report.values())

    m1, m2, m3 = st.columns(3)
    m1.markdown(f"""<div class="metric-card">
        <div class="metric-label">ROWS</div>
        <div class="metric-value">{rows}</div></div>""", unsafe_allow_html=True)
    m2.markdown(f"""<div class="metric-card">
        <div class="metric-label">COLUMNS</div>
        <div class="metric-value">{cols}</div></div>""", unsafe_allow_html=True)
    m3.markdown(f"""<div class="metric-card">
        <div class="metric-label">MISSING FIXED</div>
        <div class="metric-value">{missing_count}</div></div>""", unsafe_allow_html=True)

    st.write("")

    # ------------ CLEANED TABLE + FILTERS ---------------
    left, right = st.columns([2, 1])

    with left:
        st.markdown("### 🧼 Cleaned Data")
        st.dataframe(cleaned_df, use_container_width=True)

    # ------------ MISSING SUMMARY ----------------
    with right:
        st.markdown("### 📊 Missing Summary")
        if not missing_report:
            st.success("🎉 No missing values originally!")
        else:
            for col, rows in missing_report.items():
                st.markdown(f"""<div class="section-card">
                    <div class="missing-badge">{col} — {len(rows)} missing</div>""",
                    unsafe_allow_html=True)
                for entry in rows:
                    st.markdown(f"""<div style='padding-left:6px;'>• Row {entry['row']} — Name: {entry['name']}</div>""",
                                unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)

    # ------------ DOWNLOAD ------------------
    st.markdown("### ⬇️ Download Cleaned CSV")
    with open("cleaned_output.csv", "rb") as f:
        st.download_button(
            label="💾 Download",
            data=f,
            file_name="cleaned_data.csv",
            mime="text/csv",
            use_container_width=True
        )
