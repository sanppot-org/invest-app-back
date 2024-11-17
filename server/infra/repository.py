from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pandas as pd

engine = create_engine("mysql://root:1234@localhost:3306/invest", encoding="utf-8")
conn = engine.connect()

session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = session()

df = pd.read_sql_query(sql="", con=conn)
df
