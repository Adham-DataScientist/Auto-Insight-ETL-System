# 🚀 Auto-Insight ETL System

An automated, end-to-end **ETL (Extract, Transform, Load)** pipeline coupled with an interactive data exploration dashboard. This system is designed to seamlessly ingest raw business data, perform robust programmatic cleaning, and generate dynamic business intelligence insights on the fly.

---

## 🛠️ System Architecture & Workflow

The project is structured into three core phases:

### 1. Extraction & Ingestion (`Data Ingestion`)
* Automatically monitors and reads raw data from enterprise spreadsheets (`Updatee_Sales_Analysis_Report.xlsx`).
* Standardizes column schema dynamically, removing whitespace, correcting cases, and prepping data for stable downstream processing.

### 2. Transformation & Cleaning (`ETL Pipeline`)
* Handles missing values, enforces correct data types (Dates, Numeric, Categorical), and filters out anomalies.
* Computes high-level business metrics (Total Revenue, Transaction Counts, and Average Order Values).

### 3. Loading & Visualization (`Interactive Dashboard`)
* Loads the transformed data into a high-performance interactive dashboard built with **Streamlit** and **Plotly**.
* Features dynamic cross-filtering (by Country, Brand, and Gender) allowing decision-makers to slice and dice data seamlessly.
* Integrates predictive analytics capabilities to forecast business performance trends.

---

## 💻 Tech Stack

* **Language:** Python 3.x
* **Data Manipulation:** Pandas, NumPy
* **Interactive UI:** Streamlit
* **Data Visualization:** Plotly Express / Go
* **Deployment:** Streamlit Cloud / GitHub

---

## 🚀 Getting Started

### 1. Clone the Repository
```bash
git clone [https://github.com/Adham-DataScientist/Auto-Insight-ETL-System.git](https://github.com/Adham-DataScientist/Auto-Insight-ETL-System.git)
cd Auto-Insight-ETL-System
