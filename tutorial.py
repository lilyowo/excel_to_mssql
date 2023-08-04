from sqlalchemy import create_engine # pip install SQLAlchemy
from sqlalchemy.engine import URL
import pypyodbc # pip install pypyodbc
import pandas as pd # pip install pandas

SERVER_NAME = 'LAPTOP-B6OG51F6'
DATABASE_NAME = 'TestDB'
TABLE_NAME = 'Student'

excel_file = './Test_table.xlsx'

connection_string = f"""
    DRIVER={{SQL Server}};
    SERVER={SERVER_NAME};
    DATABASE={DATABASE_NAME};
    Trusted_Connection=yes;
"""
connection_url = URL.create('mssql+pyodbc', query={'odbc_connect': connection_string})
engine = create_engine(connection_url, module=pypyodbc)

# for single sheet
# excel_file = pd.read_excel(excel_file, sheet_name="SheetA")
# excel_file.to_sql(TABLE_NAME, engine, if_exists='append', index=False)

#preprocess excel file
df = pd.read_excel(excel_file, sheet_name="SheetA")

# 檢查欄位是否為數字，將數字欄位轉換為整數型態
numeric_columns = ['StudentID', 'Standardid']
df[numeric_columns] = df[numeric_columns].apply(pd.to_numeric, errors='coerce')

# 移除字串中的換行符號
df['StudentName'] = df['StudentName'].replace('\n', ' ', regex=True)

# # 檢查特殊符號並替換成空字串
# df['StudentName'] = df['StudentName'].replace('[^a-zA-Z0-9\s]', '', regex=True)

# 將資料寫入 SQL 資料庫
df.to_sql(TABLE_NAME, engine, if_exists='append', index=False)

#for all sheets in excel file
# excel_file = pd.read_excel(excel_file, sheet_name=None)
# print(excel_file)
# for sheet_name, df_data in excel_file.items():
#     print(f'Loading worksheet {sheet_name}...')
#     # {'fail', 'replace', 'append'}
#     df_data.to_sql(TABLE_NAME, engine, if_exists='append', index=False)

#the following can delete data in SQL
# with engine.connect() as conn:
#     conn.execute(f"DELETE FROM {TABLE_NAME} WHERE StudentName = 'apple'")

#the following can print SQL table
# with engine.connect() as conn:
#     result=conn.execute(f'select*from {TABLE_NAME}')
#     rows = result.fetchall()
#     for row in rows:
#         print(row)


