# Loan & Credit Data Analysis Dashboard

An interactive data-analysis dashboard built with **Python, Pandas, Streamlit, and Plotly**. It explores loan applications, applicant income, credit scores, employment types, loan purposes, and application outcomes.

> **Important:** The included dataset is synthetic and created for demonstration. This project is educational and must not be used to make real lending, credit eligibility, or other high-impact decisions.

## Features

- KPI cards for application count, approval share, average annual income, and average credit score
- Interactive filters for loan status, loan purpose, employment type, and credit-score range
- Charts for application outcomes, loan purpose, income versus loan amount, and credit-score distribution
- Summary statistics grouped by employment type
- CSV upload support (with required-column validation)
- Download filtered records as CSV
- Basic data-quality checks for duplicates, missing values, and invalid credit scores

## Tech stack

- Python
- Pandas
- Streamlit
- Plotly

## Project structure

```text
loan-credit-analysis/
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
└── data/
    └── loan_credit_data.csv
```

## Run locally

1. Install Python 3.10 or newer.
2. Open a terminal in this project folder.
3. Create and activate a virtual environment (recommended):

   **Windows**
   ```bash
   py -m venv .venv
   .venv\Scripts\activate
   ```

   **macOS/Linux**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
5. Launch the app:
   ```bash
   streamlit run app.py
   ```

## CSV format

Uploaded CSV files should include these columns:

- `applicant_id`
- `age`
- `annual_income`
- `loan_amount`
- `credit_score`
- `employment_type`
- `loan_purpose`
- `loan_status`

The dashboard expects loan statuses such as `Approved`, `Rejected`, and `Pending`. Keep applicant data synthetic or anonymized.

## Suggested GitHub description

Interactive Python dashboard for exploratory analysis of synthetic loan and credit data, with filters, Plotly charts, data-quality checks, and CSV export.

## Ideas for future improvements

- Add unit tests for data validation and summary calculations
- Add date-based trends if a timestamp field is introduced
- Add a notebook documenting the analysis questions and findings
- Add screenshots of the running dashboard to this README
- Deploy the Streamlit app and add its public URL here

## Portfolio note

Before listing this project on a resume, run it locally, verify its features, and add screenshots of your own run. Describe the work accurately and do not claim real-world model accuracy or lending predictions.
