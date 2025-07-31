import streamlit as st
import mysql.connector
import pandas as pd
import plotly.express as px
from datetime import datetime

# --- PAGE CONFIG ---
st.set_page_config(page_title="Placement Dashboard", layout="wide")

# --- DATABASE CONNECTION ---
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="monikha_19",  # change if needed
        database="placement_app"
    )

conn = get_connection()

# --- SIDEBAR NAVIGATION ---
st.sidebar.title("📂 Navigation")
menu = st.sidebar.radio("Go to", ["🏠 Home", "🔍 Filters", "📊 Visualisation", "💾 Download"])

# --- LOAD DATA FROM DATABASE ---
@st.cache_data(ttl=600)
def load_data():
    query = """
        SELECT s.student_id, s.name, s.gender, s.city, s.course_batch,
               p.company_name, p.placement_package,
               sk.communication, sk.teamwork, sk.presentation,
               sk.leadership, sk.critical_thinking, sk.interpersonal_skills
        FROM students s
        LEFT JOIN placements p ON s.student_id = p.student_id
        LEFT JOIN soft_skills sk ON s.student_id = sk.student_id
    """
    return pd.read_sql(query, conn)

df = load_data()

# --- HOME PAGE ---
if menu == "🏠 Home":
    st.title("📈 Placement Eligibility Dashboard")
    st.markdown("""
    This dashboard is designed for HRs and placement teams to:
    - 🔍 Filter students based on key eligibility criteria  
    - 📊 Visualize placement insights  
    - 💾 Export eligible candidates
    """)

# --- FILTER PAGE ---
elif menu == "🔍 Filters":
    st.title("🎯 Shortlist Students for Placement")

    # --- DROPDOWNS & SLIDERS ---
    col1, col2, col3, col4 = st.columns(4)

    # Get unique values from actual data
    departments = df['course_batch'].dropna().unique().tolist()
    genders = df['gender'].dropna().unique().tolist()
    cities = df['city'].dropna().unique().tolist()

    # Add 'All' option
    departments.insert(0, "All")
    genders.insert(0, "All")
    cities.insert(0, "All")
    statuses = ["All", "Placed", "Not Placed"]

    with col1:
        selected_dept = st.selectbox("🏫 Course / Department", departments)
    with col2:
        selected_gender = st.selectbox("🚻 Gender", genders)
    with col3:
        selected_city = st.selectbox("🌆 City", cities)
    with col4:
        selected_status = st.selectbox("🎓 Placement Status", statuses)

    col5, col6 = st.columns(2)
    with col5:
        min_comm = st.slider("🗣️ Min Communication Skill (0–10)", 0, 10, 0)
    with col6:
        min_package = st.slider("💰 Min Package (LPA)", 0, 20, 0)

    # --- APPLY FILTER BUTTON ---
    if st.button("🔍 View Eligible Students"):
        filtered_df = df.copy()

        # Apply each filter conditionally
        if selected_dept != "All":
            filtered_df = filtered_df[filtered_df['course_batch'] == selected_dept]
        if selected_gender != "All":
            filtered_df = filtered_df[filtered_df['gender'] == selected_gender]
        if selected_city != "All":
            filtered_df = filtered_df[filtered_df['city'] == selected_city]
        if selected_status == "Placed":
            filtered_df = filtered_df[filtered_df['company_name'].notnull()]
        elif selected_status == "Not Placed":
            filtered_df = filtered_df[filtered_df['company_name'].isnull()]
        if 'communication' in filtered_df.columns:
            filtered_df = filtered_df[filtered_df['communication'] >= min_comm]
        if 'placement_package' in filtered_df.columns:
            filtered_df['placement_package'] = pd.to_numeric(filtered_df['placement_package'], errors='coerce')
            filtered_df = filtered_df[filtered_df['placement_package'].fillna(0) >= min_package]

        st.success(f"✅ {len(filtered_df)} students found.")
        st.dataframe(filtered_df)

        # Optional: allow download
        st.download_button("📥 Download Results", filtered_df.to_csv(index=False), file_name="shortlisted_students.csv")


# --- VISUALISATION PAGE ---
elif menu == "📊 Visualisation":
    st.title("📌 Placement Visualisation")

    # 1.Pie – Placement Status
    pie_data = df['company_name'].notnull().value_counts().reset_index()
    pie_data.columns = ['Status', 'Count']
    pie_data['Status'] = pie_data['Status'].replace({True: 'Placed', False: 'Not Placed'})
    st.plotly_chart(px.pie(pie_data, names="Status", values="Count", title="Placement Status Distribution"))



    # 2. Bar Chart – Placement count by batch
    st.subheader("📊 Placement Count by Course Batch")
    if "course_batch" in df.columns:
        bar_data = df.copy()
        bar_data['Status'] = bar_data['company_name'].notnull().replace({True: 'Placed', False: 'Not Placed'})
        batch_placement = bar_data.groupby(['course_batch', 'Status'])['student_id'].count().reset_index()
        batch_placement.columns = ['Batch', 'Status', 'Count']
        fig1 = px.bar(batch_placement, x="Batch", y="Count", color="Status", barmode="group",
                      title="Placed vs Not Placed Students by Batch")
        st.plotly_chart(fig1, use_container_width=True)
    else:
        st.warning("No course_batch data available.")

    # 3. Scatter Plot – Communication Skill vs Placement Package
    st.subheader("💬 Communication Skill vs Placement Package")
    scatter_data = df.dropna(subset=["communication", "placement_package"])
    if not scatter_data.empty:
        fig2 = px.scatter(scatter_data,
                          x="communication", y="placement_package",
                          size="presentation", color="teamwork",
                          title="Do Better Communicators Get Better Packages?",
                          labels={"communication": "Communication Score", "placement_package": "Package (LPA)"},
                          hover_data=["name", "company_name"])
        st.plotly_chart(fig2, use_container_width=True)
    else:
        st.warning("Insufficient data for scatter plot.")

    # 4. Bar Chart – Students by City
    st.subheader("🌆 Students Distribution by City")
    if "city" in df.columns:
        city_data = df["city"].value_counts().reset_index()
        city_data.columns = ["City", "Count"]
        fig3 = px.bar(city_data, x="City", y="Count", title="Number of Students by City")
        st.plotly_chart(fig3, use_container_width=True)
    else:
        st.warning("City data not available.")


# --- DOWNLOAD PAGE ---
elif menu == "💾 Download":
    st.title("⬇️ Download Student Data")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    csv_data = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📥 Download CSV",
        data=csv_data,
        file_name=f"placement_data_{timestamp}.csv",
        mime="text/csv"
    )
