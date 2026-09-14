import pandas as pd
from sqlalchemy import create_engine

df = pd.read_csv("cleaned_earthquake_data.csv")
df["time"] = pd.to_datetime(df["time"],errors="coerce")
df["updated"] = pd.to_datetime(df["updated"],errors="coerce")
print(df.shape)
engine = create_engine("mysql+pymysql://root:gopi_ramesh@localhost/project_db")
with engine.connect()as conn:
    print("MySql connected successfully!")
df.to_sql("earthquakes", con=engine, if_exists="replace", index=False)
print("Data inserted successfully!")