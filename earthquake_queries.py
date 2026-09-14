import streamlit as st
import pandas as pd
from sqlalchemy import create_engine,text
engine = create_engine(
    "mysql+pymysql://root:gopi_ramesh@localhost/project_db"
)
print("MySql connected successfully!")


# SQL queries for 30 tasks
# --------------------------

queries = {
    "1. Top 10 strongest earthquakes (mag)": """
        Select * from earthquakes order by mag desc limit 10;
    """,

    "2. Top 10 deepest earthquakes (depth_km)": """
        select * from earthquakes order by depth_km desc limit 10;
    """,

    "3. Shallow earthquakes < 50 km and mag > 7.5": """
        select * from earthquakes where depth_km < 50 and mag > 7.5;
    """,

    "4. Average depth per continent": """
        select 'continent logic not available in db' as note;
    """,

    "5. Average magnitude per magnitude type (magType)": """
        select magtype, avg(mag) as average_magnitude 
        from earthquakes group by magtype;
    """,

    "6. Year with most earthquakes": """
        select year, count(*) as earthquakes_count from 
        earthquakes group by year order by earthquakes_count desc limit 1;
    """,

    "7. Month with highest number of earthquakes": """
        select month, count(*) as earthquakes_count from earthquakes 
        group by month order by earthquakes_count desc limit 1;
    """,

    "8. Day of week with most earthquakes": """
        select day_of_week, count(*) as earthquakes_count from earthquakes 
        group by day_of_week order by earthquakes_count desc limit 1;
    """,

    "9. Count of earthquakes per hour of day": """
        select hour(time) as hour, count(*) as earthquake_count from 
        earthquakes group by hour(time) order by hour;
    """,

    "10. Most active reporting network (net)": """
        select net, count(*) as earthquake_count from earthquakes 
        group by net order by earthquake_count desc limit 1;
    """,

    "11.  Top 5 places with highest casualties": """
        select place, max(felt) as casualties from earthquakes
        group by place order by casualties desc limit 5;
    """,

    "12.  Total estimated economic loss per continent": """
          select 'not available no economic lose column as note;
    """,

    "13.  Average economic loss by alert level": """
          select alert, count(*) as count from earthquakes 
          group by alert;
    """,

    "14.  Count of reviewed vs automatic earthquakes (status)": """
          select status, count(*) as earthquake_count from earthquakes 
          group by status;
    """,

    "15.  Count by earthquake type (type)": """
          select type, count(*) as earthquake_count from earthquakes 
          group by type;
    """,

    "16.  Number of earthquakes by data type (types)": """
          select types, count(*) as no_of_earthquake from earthquakes 
          group by types;
    """,

    "17.  Average RMS and gap per continent": """
          select 'continent mapping not available' as note;
    """,

    "18.  Events with high station coverage (nst > threshold)": """
          select * from earthquakes where nst > 50;
    """,

    "19.  Number of tsunamis triggered per year": """
          select year, count(*) as tsunami_count from earthquakes 
          where tsunami = 1 group by year;
    """,

    "20.  Count earthquakes by alert levels (red, orange, etc.)": """
          select alert, count(*) as earthquake_count from 
          earthquakes group by alert;
    """,

    "21.Find the top 5 countries with the highest average magnitude of earthquakes in the past 5 years": """
        select place, avg(mag) as average_magnitude from earthquakes 
        group by place order by average_magnitude desc limit 5;
    """,

    "22.Find countries that have experienced both shallow and deep earthquakes within the same month": """
        select country, year, month from earthquakes group by country, year, month 
        having min(depth_km) < 50 and max(depth_km) >= 50;
    """,

    "23.Compute the year-over-year growth rate in the total number of earthquakes globally": """
        select year, count(*) as earthquake_count, round(
        (count(*) - lag(count(*)) over (order by year)) / lag(count(*)) 
        over (order by year) * 100, 2) as growth_rate_percent 
        from earthquakes group by year order by year;
    """,

    "24. List the 3 most seismically active regions by combining both frequency and average magnitude": """
         select country, count(*) as earthquake_count, round(avg(mag), 2) 
         as average_magnitude from earthquakes group by country order by 
         earthquake_count desc, average_magnitude desc limit 3;
    """,

    "25. For each country, calculate the average depth of earthquakes within ±5° latitude range of the equator": """
         select country, avg(depth_km) as average_depth from earthquakes 
         where latitude between -5 and 5 group by country
    """,

    "26. Identify countries having the highest ratio of shallow to deep earthquakes": """
         select country, sum(depth_km < 70) as shallow,
         sum(depth_km > 300) as deep,
         sum(depth_km < 70) / nullif(sum(depth_km > 300),0) as ratio
         from earthquakes group by country order by ratio desc;
    """,

    "27. Find the average magnitude difference between earthquakes with tsunami alerts and those without": """
         SELECT AVG(CASE WHEN tsunami = 1 THEN mag END) AS avg_mag_tsunami, 
         AVG(CASE WHEN tsunami = 0 THEN mag END) AS avg_mag_no_tsunami,
         AVG(CASE WHEN tsunami = 1 THEN mag END) - AVG(CASE WHEN tsunami = 0 THEN 
         mag END) AS magnitude_difference FROM earthquakes;
    """,

    "28. Using the gap and rms columns, identify events with the lowest data reliability (highest average error margins)": """
         select * from earthquakes order by gap desc, rms desc limit 20;
    """,

    "29. Find pairs of consecutive earthquakes (by time) that occurred within 50 km of each other and within 1 hour": """
         select 'requires advanced spatial logic' as note;
    """,

    "30. Determine the regions with the highest frequency of deep-focus earthquakes (depth > 300 km)": """
         SELECT country, COUNT(*) AS deep_earthquake_count FROM earthquakes 
         WHERE depth_km > 300 GROUP BY country ORDER BY deep_earthquake_count DESC;
    """
}

print("\nRunning SQL queries...\n")

for name, query in queries.items():
    print("=" * 60)
    print(name)
    print("=" * 60)

    try:
        result = pd.read_sql(query, engine)
        print(result)
        print()
    except Exception as e:
        print("Error:", e)
        print()




# --------------------------------
# STREAMLIT UI
#---------------------------------
st.title("Earthquake Data analysis Dashboard")
st.write("Select any problem statement (1-30) to run the corresponding sql query.")

task = st.selectbox("Choose task number",list(queries.keys()))

if st.button("Run Query"):
    query = queries[task]
    df = pd.read_sql(query, engine)

    st.subheader(f"Result for Task:{task}")
    st.dataframe(df,use_container_width=True)
