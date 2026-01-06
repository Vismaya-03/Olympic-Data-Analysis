# Olympics Data Analysis Web App

An interactive **data analysis and visualization web application** built using **Streamlit** to explore historical Olympic Games data.  
The app provides insights into medal tallies, country-wise performance, athlete demographics, and overall Olympic trends through rich visualizations.

---

##  Project Overview

This project analyzes historical Olympic data to answer questions such as:

- How have Olympic participation and events evolved over time?
- Which countries dominate the medal tally?
- What are the age, height, and weight patterns of successful athletes?
- How has men vs women participation changed across years?

The application is fully interactive and allows users to explore insights dynamically using filters and dropdowns.

---

## 🚀 Features

### 🥇 Medal Tally
- Filter medals by **Year**, **Country**, and **Season**
- View overall and specific Olympic medal tallies
- Dynamically updated tables

### 📊 Overall Analysis
- Key statistics:
  - Editions  
  - Host Cities  
  - Sports  
  - Events  
  - Nations  
  - Athletes  
- Time-series analysis of:
  - Participating nations  
  - Number of events  
  - Athlete participation  
- Heatmap showing sport-wise event distribution across years  
- Most successful athletes (overall or by sport)

### Country-wise Analysis
- Medal performance of a selected country over time  
- Sport-wise success heatmap  
- Top 10 most decorated athletes from a country  

### Athlete Analysis
- Age distribution of:
  - All athletes  
  - Gold, Silver, Bronze medalists  
- Sport-wise age distribution of gold medalists  
- Height vs Weight scatter analysis  
- Men vs Women participation trends  

---

## Tech Stack
- **Python**
- **Streamlit** – Web application framework
- **Pandas** – Data manipulation
- **Matplotlib & Seaborn** – Static visualizations
- **Plotly** – Interactive charts
- **Plotly Figure Factory** – Distribution plots

---

## 📂 Dataset Used
- `athlete_events.csv` – Historical Olympic athlete data  
- `noc_regions.csv` – National Olympic Committee region mapping  
  [Data Link](https://www.kaggle.com/datasets/heesoo37/120-years-of-olympic-history-athletes-and-results)
The datasets are preprocessed and merged before analysis.

