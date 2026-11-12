# Mobile App Business Intelligence & Customer Intelligence Platform

An end-to-end Data Science and Business Intelligence project that transforms customer and e-commerce activity data into actionable business insights using Python, SQL, Excel, Power BI, Machine Learning, Deep Learning, and Explainable AI.

The platform combines data analytics, predictive modelling, and interactive dashboards to understand customer behaviour, analyse business performance, and predict purchase decisions.

## Project Overview

Businesses generate large amounts of customer interaction data through digital platforms. Analysing this data helps organisations understand customer preferences, improve conversion rates, identify business opportunities, and make data-driven decisions.

This project provides an integrated intelligence platform that covers the complete data science workflow, from raw data preprocessing to analytics, machine learning predictions, and API-based application integration.

## Key Objectives

- Analyse customer behaviour and purchasing patterns.
- Perform data cleaning, preprocessing, and exploratory data analysis.
- Build SQL queries for business intelligence.
- Develop Excel and Power BI dashboards.
- Apply Machine Learning algorithms for purchase prediction.
- Implement an Artificial Neural Network (ANN).
- Use Explainable AI techniques to understand model predictions.
- Develop REST APIs using FastAPI.
- Build an interactive application using Streamlit.

## Technology Stack

| Category | Technologies |
|---|---|
| Programming | Python |
| Data Analysis | Pandas, NumPy |
| Visualization | Matplotlib, Seaborn, Plotly |
| Database | MySQL, SQL |
| Spreadsheet Analytics | Microsoft Excel |
| Business Intelligence | Power BI |
| Machine Learning | Scikit-learn |
| Deep Learning | Artificial Neural Network (ANN) |
| Explainable AI | SHAP |
| Backend | FastAPI |
| Frontend | Streamlit |
| Development Tools | VS Code, Jupyter Notebook, Git |

## Project Structure

```text
Mobile App Business Intelligence & Customer Intelligence Platform/
│
├── .venv/
├── .vscode/
│
├── backend/
│   ├── app/
│   ├── routes/
│   │   ├── customers.py
│   │   └── prediction.py
│   ├── schemas/
│   ├── services/
│   ├── main.py
│   ├── inspect_data.py
│   ├── inspect_model.py
│   └── requirements.txt
│
├── data/
│
├── docs/
│
├── excel/
│
├── frontend/
│   └── app.py
│
├── models/
│   └── NEXORA_RF_Explainable_Model.pkl
│
├── notebooks/
│
├── power_bi/
│
├── reports/
│   └── README.md
│
├── sql/
│   ├── 01_database_setup.sql
│   └── 02_data_quality.sql
│
├── src/
│   ├── data_analysis/
│   ├── evaluation/
│   ├── models/
│   └── preprocessing/
│
├── Ecommerce_Business_Intelligence.xlsx
├── requirements.txt
└── README.md
```

*Note: This structure follows the folders and files visible in the project screenshots. Some folders may contain additional files.*

## Project Modules

### 1. Data Collection and Preprocessing

- Load and inspect the dataset.
- Handle missing values and duplicate records.
- Perform data cleaning and transformation.
- Encode categorical variables.
- Perform feature engineering.
- Prepare processed data for analytics and model training.

**Tools:** Python, Pandas, NumPy, Scikit-learn.

### 2. Exploratory Data Analysis

Perform exploratory analysis to identify patterns and relationships in customer and transaction data.

Key analysis areas:

- Customer behaviour analysis.
- Revenue analysis.
- Product category analysis.
- Marketing channel performance.
- Device-based customer behaviour.
- Purchase conversion analysis.
- Cart abandonment analysis.
- Monthly revenue trends.

**Tools:** Pandas, Matplotlib, Seaborn.

### 3. SQL Business Analytics

Use MySQL to organise and analyse business data.

SQL scripts include:

- `01_database_setup.sql` – Database setup.
- `02_data_quality.sql` – Data quality checks.

Business analysis can include aggregation, filtering, joins, subqueries, CTEs, and window functions.

### 4. Excel Business Dashboard

Develop an interactive Excel dashboard to monitor important business KPIs and analyse customer and revenue performance.

Dashboard analysis includes:

- Total Revenue.
- Total Purchases.
- Total Sessions.
- Average Order Value.
- Purchase Conversion Rate.
- Revenue by Product Category.
- Revenue by Marketing Channel.
- Customer Behaviour by Device.
- Monthly Revenue Analysis.
- Cart Abandonment Analysis.

**Tools:** Microsoft Excel, Pivot Tables, Pivot Charts, Power Query.

### 5. Power BI Dashboard

Create interactive Power BI reports to present business insights and model intelligence.

Dashboard pages:

**Business Intelligence**
- Business performance.
- Customer behaviour.
- Revenue trends.
- Purchase conversion.
- Marketing performance.

**ML & DL Intelligence**
- Predictive analytics.
- Machine Learning insights.
- Model performance and evaluation.
- Deep Learning insights.

### 6. Machine Learning

Develop predictive models to identify whether a customer session is likely to result in a purchase.

The project includes a Random Forest model integrated with the prediction application.

Model artifact:

`models/NEXORA_RF_Explainable_Model.pkl`

The saved artifact contains the trained model, preprocessing pipeline, and feature names.

Model evaluation can include:

- Accuracy.
- Precision.
- Recall.
- F1-score.
- Confusion Matrix.

### 7. Deep Learning

Explore Artificial Neural Networks for customer purchase prediction.

ANN architecture:

```text
Input Features
      |
Dense Layer (64 Neurons, ReLU)
      |
Dense Layer (32 Neurons, ReLU)
      |
Output Layer (1 Neuron, Sigmoid)
      |
Purchase Prediction
```

### 8. Explainable AI

Use Explainable AI to understand the factors influencing model predictions.

**SHAP (SHapley Additive exPlanations)** is integrated into the backend to help interpret feature contributions and understand why a model produces a particular prediction.

### 9. FastAPI Backend

Develop REST APIs to connect the predictive model and customer analytics with the frontend.

Main API endpoints:

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/` | Root endpoint |
| GET | `/health` | Health check |
| GET | `/api/v1/customers` | Retrieve customer records |
| GET | `/api/v1/customers/summary` | Customer summary |
| GET | `/api/v1/customers/analytics/device` | Device analytics |
| GET | `/api/v1/customers/analytics/category` | Category analytics |
| GET | `/api/v1/customers/analytics/channel` | Marketing analytics |
| GET | `/api/v1/customers/analytics/monthly` | Monthly analytics |
| POST | `/api/v1/predict` | Predict purchase behaviour |
| POST | `/api/v1/explain` | Explain model predictions |

Interactive API documentation is available through FastAPI Swagger UI.

### 10. Streamlit Frontend

Develop an interactive web application using Streamlit.

Application modules include:

1. Business Overview
2. Customer Records
3. Device Analytics
4. Category Analytics
5. Marketing Analytics
6. Monthly Analytics
7. Purchase Prediction
8. Explainable AI (SHAP)

The application connects with the FastAPI backend to retrieve analytics and generate predictions.

## Installation and Setup

### Step 1: Clone the Repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

### Step 2: Navigate to the Project

```bash
cd "Mobile App Business Intelligence & Customer Intelligence Platform"
```

### Step 3: Create a Virtual Environment

```bash
python -m venv .venv
```

### Step 4: Activate the Environment

**Windows PowerShell:**

```powershell
.\.venv\Scripts\Activate.ps1
```

### Step 5: Install Dependencies

```bash
python -m pip install -r requirements.txt
```

## Running the Application

The backend and frontend should run in separate terminals.

### Terminal 1: Start FastAPI Backend

```bash
python -m uvicorn backend.main:app --reload
```

Backend URL:

`http://127.0.0.1:8000`

API documentation:

`http://127.0.0.1:8000/docs`

### Terminal 2: Start Streamlit Frontend

```bash
python -m streamlit run frontend/app.py
```

Frontend URL:

`http://localhost:8501`

## Expected Outcomes

- A structured data preprocessing and analysis workflow.
- SQL-based business analytics.
- Interactive Excel and Power BI dashboards.
- Machine Learning-based purchase prediction.
- Deep Learning experimentation using ANN.
- Explainable predictions using SHAP.
- REST API integration using FastAPI.
- Interactive analytics application using Streamlit.

## Future Enhancements

- Deploy the application to a cloud platform.
- Add user authentication and role-based access.
- Integrate real-time customer activity data.
- Expand predictive analytics capabilities.
- Improve model monitoring and performance tracking.
- Add additional Explainable AI visualizations.

## Conclusion

The Mobile App Business Intelligence & Customer Intelligence Platform demonstrates an end-to-end Data Science workflow by integrating data engineering, business analytics, predictive modelling, explainable AI, backend development, and interactive application development.

It demonstrates how raw customer data can be transformed into meaningful business insights and predictive intelligence to support better business decisions.

---

**Project Focus:** Data Science | Business Intelligence | Machine Learning | Deep Learning | Explainable AI | FastAPI | Streamlit
