# 🧼 Data Cleaning Automation Tool (Python + Streamlit)

A complete, production-ready **Data Cleaning Framework** built using **Python, Pandas, and Streamlit**.  
This tool automatically detects missing values, generates detailed missing reports, cleans messy datasets, normalizes dates, removes duplicates, and exports a fully cleaned CSV.

Includes:
- 🔥 Command Line Interface (CLI)
- 🌐 Web UI (Streamlit)
- 📊 Missing Values Summary Panel

---

## 🚀 Features

### 🧹 1. Automatic Data Cleaning Engine
- Removes duplicate rows  
- Standardizes column names  
- Strips extra spaces  
- Auto-detects and converts valid date columns  
- Fills missing **numeric values** using *median*  
- Fills missing **text values** using *mode*

---

### 🔍 2. Missing Value Detection (Before Cleaning)
Get detailed explanation of where the missing values are and who they belong to.

Example:

```
Missing Values Summary:
age → Missing at Row 1 (Name: Karthik)
salary → Missing at Row 2 (Name: Priya)
city → Missing at Row 3 (Name: Priya)
```

---

### 🌐 3. Streamlit Web UI  
A clean and interactive interface.

**Features:**
- Upload messy CSV  
- Preview raw data  
- One-click “Clean Data”  
- Download cleaned CSV  
- Missing Value Summary Panel  

Run the app:

```bash
streamlit run app.py
```

---

### 🖥️ 4. CLI Tool (Command Line Interface)

Run from terminal:

```bash
python cli.py --input raw.csv --output cleaned.csv
```

---

## 📂 Project Structure

```
data_cleaning_tool/
│── app.py                # Streamlit Web UI
│── cli.py                # CLI Entry Point
│── setup.py              # Packaging Config
│── requirements.txt      # Dependencies
│── data_cleaner/
│     ├── cleaner.py      # Core Cleaning Engine
│     └── __init__.py     # Module Export
```

---

## ▶️ Installation (Developer Mode)

```bash
pip install -e .
```

---

## 🧠 Technologies Used
- Python  
- Pandas  
- Streamlit  
- VS Code  
- Git & GitHub  

---

## ⭐ Future Enhancements
- XLSX file support  
- Missing value heatmap  
- Duplicate detection visualization  
- Automated data profiling  
- Online hosted version (Streamlit Cloud)

---

## 👨‍💻 Author

**Mahadevan K**  
Data Analyst & Front-End Developer  

GitHub: https://github.com/MAHADEVAN005  
LinkedIn: https://www.linkedin.com/in/mahadevan-k-0a2718298  
Email: mahadevan5563@gmail.com  

---

## 🤝 Contributions  
Suggestions & pull requests are welcome!
