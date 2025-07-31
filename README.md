# 📊 Placement Eligibility Dashboard

An interactive Streamlit web application designed in **Visual Studio Code**, with a **MySQL** backend integrated via **Python**. SQL queries are executed through **Jupyter Notebook**, making it easy to filter, visualize, and export student placement data. Built to assist HR professionals in streamlining the student shortlisting process during campus placements.

---

## 🚀 Features

- 🎯 Smart multi-dropdown filters (Department, Gender, Batch, Scores)
- 📈 Visual analytics using Plotly for technical and soft skills
- 📥 Export filtered student data as timestamped CSV files

---

## 🛠️ Tech Stack

- **Frontend**: Streamlit (Python)
- **Backend**: MySQL
- **Query Handling**: Jupyter Notebook
- **IDE**: Visual Studio Code
- **Visualization**: Plotly
- **Data Manipulation**: Pandas

---

## 📁 Folder Structure

```
placement-eligibility-dashboard/
│
├── placement_app.py             # Main Streamlit application      
├── notebooks/
│   └── placement_app.ipynb      # Jupyter Notebook with data analysis and table creation/insertion
└── README.md                    # This file
```

---

## 💻 Setup Instructions

1. **Clone the Repository**
   ```bash
   git clone https://github.com/monikha-19/Placement_Eligibility_Dashboard.git
   cd Placement_Eligibility_Dashboard
   ```

2. **Set up MySQL Database**
   - Create a MySQL database named `placement_app`
   - Run `placement_app.ipynb` to create required tables and insert data

3. **Install Dependencies**
   ```bash
   pip install streamlit mysql-connector-python pandas plotly
   ```

4. **Run the App**
   ```bash
   streamlit run placement_app.py
   ```

---

## 🙋‍♀️ About the Creator

Created by **Monikha S.**, a fresher with a passion for practical applications of technology.  

---
