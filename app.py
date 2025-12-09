import streamlit as st
import pandas as pd
from data_cleaner import clean_csv

# -------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------
st.set_page_config(
    page_title="Automatic Data Cleaning Tool",
    page_icon="🧼",
    layout="wide",
)

# -------------------------------------------------
# CUSTOM CSS (Gradient BG + Animations + Cards)
# -------------------------------------------------
st.markdown(
    """
    <style>
        .stApp {
            background: linear-gradient(135deg, #0f172a 0%, #020617 40%, #111827 100%);
            color: #f9fafb;
            font-family: "Inter", system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
        }
        h1, h2, h3, h4, h5 {
            color: #f9fafb;
        }
        .main-card {
            background: rgba(15,23,42,0.85);
            padding: 24px 28px;
            border-radius: 18px;
            box-shadow: 0 18px 40px rgba(0,0,0,0.55);
            border: 1px solid rgba(148,163,184,0.35);
            backdrop-filter: blur(14px);
            animation: fadeIn 0.7s ease-out;
        }
        .section-card {
            background: rgba(15,23,42,0.92);
            padding: 18px 20px;
            border-radius: 16px;
            box-shadow: 0 10px 28px rgba(0,0,0,0.4);
            border: 1px solid rgba(148,163,184,0.35);
            backdrop-filter: blur(10px);
            margin-bottom: 14px;
            animation: floatUp 0.5s ease-out;
        }
        .metric-card {
            text-align: left;
            padding: 12px 16px;
            border-radius: 16px;
            background: linear-gradient(135deg, #1d283a, #020617);
            border: 1px solid rgba(148,163,184,0.6);
            box-shadow: 0 12px 24px rgba(15,23,42,0.9);
            transition: transform 0.15s ease-out, box-shadow 0.15s ease-out, border-color 0.15s ease-out;
        }
        .metric-card:hover {
            transform: translateY(-3px);
            box-shadow: 0 20px 40px rgba(15,23,42,1);
            border-color: #38bdf8;
        }
        .metric-label {
            font-size: 13px;
            color: #9ca3af;
            text-transform: uppercase;
            letter-spacing: 0.06em;
        }
        .metric-value {
            font-size: 24px;
            font-weight: 700;
            color: #e5e7eb;
        }
        .metric-sub {
            font-size: 12px;
            color: #9ca3af;
        }
        .missing-badge {
            display: inline-flex;
            align-items: center;
            padding: 4px 10px;
            border-radius: 999px;
            font-size: 12px;
            background: rgba(248,113,113,0.12);
            color: #fecaca;
            border: 1px solid rgba(248,113,113,0.4);
            margin-bottom: 8px;
        }
        .missing-row {
            font-size: 13px;
            color: #e5e7eb;
            margin-left: 8px;
        }
        .header-logo {
            width: 56px;
            height: 56px;
            border-radius: 18px;
            background: conic-gradient(from 200deg, #22d3ee, #6366f1, #ec4899, #22d3ee);
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-weight: 900;
            font-size: 22px;
            box-shadow: 0 12px 30px rgba(59,130,246,0.75);
            animation: pulseGlow 2s infinite alternate;
        }
        .header-icon {
            font-size: 28px;
        }
        .upload-zone > div > div {
            border-radius: 16px !important;
            border: 1.4px dashed rgba(148,163,184,0.8) !important;
            background: radial-gradient(circle at top left, rgba(59,130,246,0.08), rgba(15,23,42,0.95));
        }
        .dataframe tbody tr:hover {
            background-color: rgba(55,65,81,0.55) !important;
        }
        .contact-pill {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            padding: 6px 10px;
            border-radius: 999px;
            border: 1px solid rgba(148,163,184,0.6);
            background: rgba(15,23,42,0.9);
            color: #e5e7eb;
            font-size: 13px;
            margin-right: 8px;
        }
        .contact-pill span.emoji {
            font-size: 16px;
        }
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(14px); }
            to { opacity: 1; transform: translateY(0); }
        }
        @keyframes floatUp {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        @keyframes pulseGlow {
            from { box-shadow: 0 0 20px rgba(129,140,248,0.6); }
            to { box-shadow: 0 0 35px rgba(236,72,153,0.95); }
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# -------------------------------------------------
# SIDEBAR – THEME & FILTER PLACEHOLDER
# -------------------------------------------------
st.sidebar.markdown("## ⚙️ Controls")
dark_mode = st.sidebar.toggle("🌙 Dark mode", value=True)

if not dark_mode:
    # just reduce background darkness a bit
    st.markdown(
        """
        <style>
        .stApp {
            background: radial-gradient(circle at top, #e5e7eb 0%, #cbd5f5 30%, #94a3b8 100%);
            color: #020617;
        }
        h1,h2,h3,h4,h5 { color: #020617; }
        </style>
        """,
        unsafe_allow_html=True,
    )

st.sidebar.markdown("---")
st.sidebar.markdown("### 📂 File Info")
st.sidebar.write("Supported formats:")
st.sidebar.write("• CSV\n• Excel (.xlsx)\n• JSON\n• TSV")

st.sidebar.markdown("---")
st.sidebar.markdown("### 📞 Contact")
st.sidebar.markdown(
    """
    <div class="contact-pill"><span class="emoji">📧</span><span>mahadevankaliyappan@gmail.com</span></div>
    <div class="contact-pill"><span class="emoji">📞</span><span>+91 7708497524</span></div>
    """,
    unsafe_allow_html=True,
)

# -------------------------------------------------
# HEADER
# -------------------------------------------------
with st.container():
    col_logo, col_title = st.columns([1, 6])
    with col_logo:
        st.markdown(
            """
            <div class="header-logo">
                <span class="header-icon">DC</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col_title:
        st.markdown(
            """
            <div style="margin-left: 6px;">
                <h1 style="margin-bottom:2px;">Automatic CSV Cleaning Tool</h1>
                <p style="font-size:15px; opacity:0.8;">
                    Smart Data Cleaning • Missing Value Insights • Interactive Visual Summary
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

st.write("")  # spacing

# -------------------------------------------------
# MAIN CARD
# -------------------------------------------------
with st.container():
    st.markdown('<div class="main-card">', unsafe_allow_html=True)

    # -------- Upload Section --------
    st.markdown("### 📤 Upload Your File")

    up_col1, up_col2 = st.columns([2, 1])
    with up_col1:
        st.markdown('<div class="upload-zone">', unsafe_allow_html=True)
        uploaded_file = st.file_uploader(
            "Drag & Drop or Browse",
            type=["csv", "xlsx", "json", "tsv"],
            label_visibility="collapsed",
        )
        st.markdown("</div>", unsafe_allow_html=True)
    with up_col2:
        st.markdown("##### ✅ Supported File Types")
        st.write("• CSV")
        st.write("• Excel (.xlsx)")
        st.write("• JSON")
        st.write("• TSV")
        st.caption("Max ~200MB (subject to Streamlit Cloud limits)")

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
            df = None

    if df is not None:
        st.markdown("### 👀 Raw Data Preview")
        st.dataframe(df.head(200), use_container_width=True)

        raw_path = "raw_temp.csv"
        df.to_csv(raw_path, index=False)

        if st.button("✨ Clean & Analyze Data", use_container_width=True, type="primary"):
            cleaned_path = "cleaned_output.csv"
            missing_report = clean_csv(raw_path, cleaned_path)
            cleaned_df = pd.read_csv(cleaned_path)

    # After button click & cleaning
    if cleaned_df is not None:
        st.markdown("")

        # --------- Top Metrics Row ----------
        total_rows = len(cleaned_df)
        total_cols = len(cleaned_df.columns)
        total_missing_cells = sum(len(v) for v in missing_report.values()) if missing_report else 0

        m1, m2, m3 = st.columns(3)
        with m1:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-label">ROWS</div>
                    <div class="metric-value">{total_rows}</div>
                    <div class="metric-sub">Records after cleaning</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with m2:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-label">COLUMNS</div>
                    <div class="metric-value">{total_cols}</div>
                    <div class="metric-sub">Fields in dataset</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with m3:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-label">MISSING VALUES (ORIGINAL)</div>
                    <div class="metric-value">{total_missing_cells}</div>
                    <div class="metric-sub">Cells fixed during cleaning</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.write("")
        c1, c2 = st.columns([2, 1.4])

        # -------- Cleaned Data + Filtered View --------
        with c1:
            st.markdown("### 🧼 Cleaned Data")
            st.dataframe(cleaned_df.head(300), use_container_width=True)

            st.markdown("### 🔎 Filtered View (Sidebar Filters)")
            filtered_df = cleaned_df.copy()

            # sidebar filters
            st.sidebar.markdown("---")
            st.sidebar.markdown("### 🔍 Filters (After Cleaning)")
            if not cleaned_df.empty:
                num_cols = cleaned_df.select_dtypes(include=["int64", "float64"]).columns.tolist()
                cat_cols = cleaned_df.select_dtypes(include=["object"]).columns.tolist()

                if num_cols:
                    num_col = st.sidebar.selectbox("Numeric column filter", ["None"] + num_cols)
                    if num_col != "None":
                        min_val = float(cleaned_df[num_col].min())
                        max_val = float(cleaned_df[num_col].max())
                        rng = st.sidebar.slider(
                            f"{num_col} range",
                            min_val,
                            max_val,
                            (min_val, max_val),
                        )
                        filtered_df = filtered_df[
                            (filtered_df[num_col] >= rng[0]) & (filtered_df[num_col] <= rng[1])
                        ]

                if cat_cols:
                    cat_col = st.sidebar.selectbox("Categorical column filter", ["None"] + cat_cols)
                    if cat_col != "None":
                        options = sorted(cleaned_df[cat_col].dropna().unique().tolist())
                        selected_vals = st.sidebar.multiselect(f"{cat_col} values", options)
                        if selected_vals:
                            filtered_df = filtered_df[filtered_df[cat_col].isin(selected_vals)]

            st.dataframe(filtered_df.head(300), use_container_width=True)

        # -------- Missing Summary + Charts / Profiling --------
        with c2:
            st.markdown("### 📊 Missing Values Summary")
            if not missing_report:
                st.success("🎉 No missing values were found in the original dataset!")
            else:
                for col, rows in missing_report.items():
                    st.markdown(
                        f'<div class="section-card"><div class="missing-badge">❗ {col} — {len(rows)} missing</div>',
                        unsafe_allow_html=True,
                    )
                    for entry in rows:
                        st.markdown(
                            f'<div class="missing-row">• Row {entry["row"]} — Name: {entry["name"]}</div>',
                            unsafe_allow_html=True,
                        )
                    st.markdown("</div>", unsafe_allow_html=True)

            # charts
            st.markdown("### 📈 Quick Column Chart")
            if not cleaned_df.empty:
                numeric_cols = cleaned_df.select_dtypes(include=["int64", "float64"]).columns.tolist()
                if numeric_cols:
                    chart_col = st.selectbox("Select numeric column", numeric_cols, key="chart_col")
                    st.bar_chart(cleaned_df[chart_col])
                else:
                    st.info("No numeric columns available for chart.")

            # profiling
            st.markdown("### 🧠 Column Profiling")
            profile_rows = []
            for col in cleaned_df.columns:
                series = cleaned_df[col]
                profile_rows.append({
                    "Column": col,
                    "Type": str(series.dtype),
                    "Missing": series.isna().sum(),
                    "Unique": series.nunique(),
                    "Min": series.min() if pd.api.types.is_numeric_dtype(series) else None,
                    "Max": series.max() if pd.api.types.is_numeric_dtype(series) else None,
                    "Example": series.dropna().iloc[0] if series.dropna().shape[0] > 0 else None
                })
            profile_df = pd.DataFrame(profile_rows)
            st.dataframe(profile_df, use_container_width=True)

        st.markdown("### ⬇️ Download Cleaned File")
        with open("cleaned_output.csv", "rb") as f:
            st.download_button(
                label="💾 Download Cleaned CSV",
                data=f,
                file_name="cleaned_data.csv",
                mime="text/csv",
                use_container_width=True,
            )

    st.markdown("</div>", unsafe_allow_html=True)  # close main-card
