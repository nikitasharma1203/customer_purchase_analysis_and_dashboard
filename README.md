# Bike Buyers Data Analysis Project

*(Excel · Python · Power BI · Streamlit )*

## 🌐 Live Streamlit App
The project includes a deployed Streamlit application for automated data cleaning checks and exploratory data analysis.
https://customerpurchaseanalysisanddashboard-zmxskm2t273vjomsjyucak.streamlit.app/


## Project Overview



This project analyzes customer demographic and lifestyle data to understand the factors influencing bike purchasing behavior. The analysis was performed end-to-end using Microsoft Excel and python for data cleaning, EDA, and dashboarding, and Power BI for interactive business intelligence visualization.



The project demonstrates practical data analysis skills including data cleaning, exploratory data analysis (EDA), dashboard creation, and BI reporting.



## Project Files \& Structure



Bike-Buyers-Data-Analysis/

│

├── Bike\_Buyers\_Analysis.xlsx

│   ├── Raw\_Data        → Original dataset (unchanged)

│   ├── Cleaned\_Data    → Cleaned \& processed dataset

│   ├── EDA             → Pivot tables \& analysis

│   └── Dashboard       → Interactive Excel dashboard

│

├── Bike\_Buyers\_PowerBI.pbix

│   → Interactive Power BI dashboard

│
  
  -customer_purchase_python_eda.ipynb
│     Data cleaning & EDA using Python (Pandas, Seaborn)

├── Bike\_Buyers\_PowerBI\_Report.pdf

│   → Exported Power BI dashboard (PDF)

│

├── Bike\_Buyers\_Data\_Analysis\_Report.pdf

│

├── data\_cleaning+eda\_app.py

│   → Generalized Streamlit app for data cleaning checks \& EDA

│

├── requirements.txt

│

│

└── README.md



## Tools \& Technologies Used



* Microsoft Excel



* Data Cleaning



* Feature Engineering



* Pivot Tables



* Interactive Dashboard with Slicers


* Python


* Power BI



* Data Modeling



* DAX Measures



* Interactive Visualizations



* Python \& Streamlit



* Generalized EDA web application



* Reusable for any dataset



## Data Cleaning Process



Removed duplicate customer records using unique IDs



Handled missing values:



* Categorical columns → replaced with “Unknown”



* Numerical columns → mean imputation



Standardized text values (Yes/No, casing, extra spaces)



Created derived features:



* Age Group



* Income Group



## Exploratory Data Analysis (EDA)



Key analyses performed using Excel Pivot Tables:



Bike purchase distribution



Income vs bike purchase behavior



Age group vs purchase trends



Commute distance impact on purchase



Region-wise bike purchase comparison



## Dashboards



#### Excel Dashboard



KPI Metrics:



* Total Customers



* Bike Buyers



* Purchase Rate



* Interactive charts with slicers:



* Gender



* Age Group



* Region



* Income Group



#### Power BI Dashboard



* Replicated Excel insights using Power BI



* DAX measures for KPIs



* Interactive filters and visuals



## Streamlit EDA Application



A generalized Streamlit app (data\_cleaning+eda\_app.py) was developed to perform:



* Dataset overview



* Missing value summary



* Automatic detection of numeric \& categorical columns



* Interactive filters



* Auto-generated EDA visualizations



## Key Insights



* Higher income customers are more likely to purchase bikes



* Customers aged 30–50 form the primary buyer segment



* Short commute distances significantly increase bike purchases



* Regional differences strongly affect purchasing behavior
