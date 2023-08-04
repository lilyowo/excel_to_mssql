from sqlalchemy import create_engine, inspect # pip install SQLAlchemy
from sqlalchemy.engine import URL
import pypyodbc # pip install pypyodbc
import pandas as pd # pip install pandas
import re


SERVER_NAME = 'LAPTOP-B6OG51F6'
DATABASE_NAME = 'med_DB2'
TABLE_NAME = 'SampleData'
REF_TB_NAME1 = 'AllMed'
REF_TB_NAME2 = 'MedSource'
REF_TB_NAME5 = 'StandardData'
excel_file = './Med_table.xlsx'
connection_string = f"""
    DRIVER={{SQL Server}};
    SERVER={SERVER_NAME};
    DATABASE={DATABASE_NAME};
    Trusted_Connection=yes;
"""
connection_url = URL.create('mssql+pyodbc', query={'odbc_connect': connection_string})
engine = create_engine(connection_url, module=pypyodbc)
# get table Attribute info
inspector = inspect(engine)
table_columns = inspector.get_columns(TABLE_NAME)

# for single sheet
excel_sheet = pd.read_excel(excel_file, sheet_name="SampleData")

# preprocess the excel file
#處理foreign key連接問題
# check foreign key 
def check_foreign_key(ref_tb, attribute):
    global excel_sheet
    # get all id in ref table
    query = f"SELECT {attribute.lower()} FROM {ref_tb}"
    ref_table = pd.read_sql_query(query, engine)
    existing_ids = set(ref_table[attribute.lower()])#讀取sql出來的attribute不會區分大小寫一律都小寫出來
    # find excel id not in ref table
    missing_ids = excel_sheet[~excel_sheet[attribute].isin(existing_ids)][attribute].tolist()
    # remove rows  which id not in ref table
    if len(missing_ids) > 0:
        print(f"以下 id 在 ref table中不存在: {missing_ids}")
        excel_sheet = excel_sheet[excel_sheet[attribute].isin(existing_ids)]

check_foreign_key(REF_TB_NAME1, "Med_id")
check_foreign_key(REF_TB_NAME2, "Source_id")
check_foreign_key(REF_TB_NAME5, "Standard_id")

# #處理primary key獨立問題
# # primary key uniqueness and is number

# invalid_rows = []
# existing_rows = set()

# for _, row in excel_sheet.iterrows():
#     try:
#         Med_id = int(row['Med_id'])
#         Source_id = int(row['Source_id'])
#         Sample_id = int(row['Sample_id'])
#     except ValueError:
#         invalid_rows.append(row)
#         continue

#     if (Med_id, Source_id, Sample_id) in existing_rows:
#         invalid_rows.append(row)
#     else:
#         existing_rows.add((Med_id, Source_id, Sample_id))

# # check if primary key exists in SQL table C
# existing_ids = []
# with engine.connect() as conn:
#     result = conn.execute(f'SELECT Med_id, Source_id, Sample_id FROM {TABLE_NAME}')
#     existing_ids = [tuple(row) for row in result.fetchall()]

# duplicate_ids = [tuple(row) for _, row in excel_sheet.iterrows() if tuple(row[['Med_id', 'Source_id', 'Sample_id']]) in existing_ids]

# # Remove invalid and duplicate rows from excel_sheet
# if invalid_rows or duplicate_ids:
#     print("Invalid or duplicate data found in Excel:")
#     if invalid_rows:
#         print("Invalid data rows:", invalid_rows)
#     if duplicate_ids:
#         print("Duplicate data rows:", duplicate_ids)
#     excel_sheet = excel_sheet[~excel_sheet.apply(tuple, axis=1).isin([tuple(row) for _, row in invalid_rows + duplicate_ids])]





#################################################################
# invalid_ids = []# collect not number data row
# for _, row in excel_sheet.iterrows():
#     try:
#         id_value = int(row['Standard_id'])
#     except ValueError:
#         invalid_ids.append(row['Standard_id'])

#     row['Standard_id'] = id_value

# # check duplicate ID

# existing_ids_df=[]
# with engine.connect() as conn:
#     result=conn.execute(f'select Standard_id from {TABLE_NAME}')
#     allresult = result.fetchall()
#     existing_ids_df = [item[0] for item in allresult]
    
# duplicate_ids = excel_sheet[excel_sheet.duplicated('Standard_id')]['Standard_id'].tolist()
# duplicate_ids += excel_sheet[excel_sheet['Standard_id'].isin(existing_ids_df)]['Standard_id'].tolist()

# # non number ID OR duplicated ID, Remove them from excel file which going to load to sql
# if invalid_ids or duplicate_ids:
#     print("Invalid or duplicate IDs found in Excel data:")
#     if invalid_ids:
#         print("Invalid IDs:", invalid_ids)
#     if duplicate_ids:
#         print("Duplicate IDs:", duplicate_ids)
#     excel_sheet = excel_sheet[~excel_sheet['Standard_id'].isin(invalid_ids + duplicate_ids)]


#################################################################


# #處理數值欄位必為數值 否則改Null
# # check which is numerate
# numeric_columns = [column['name'] for column in table_columns if column['type'].python_type in (int, float)]

# # non numerate data turn into Null
# for col in numeric_columns:
#     excel_sheet[col] = pd.to_numeric(excel_sheet[col], errors='coerce')


# # 處理not null的值有Null就不可以放進去
# # check which not Null 
# not_null_columns = [column['name'] for column in table_columns if not column['nullable']]

# # take out rows that contain null in not null column
# invalid_rows = excel_sheet[excel_sheet[not_null_columns].isnull().any(axis=1)]

# # remove and print them
# excel_sheet = excel_sheet.dropna(subset=not_null_columns)
# if not invalid_rows.empty:
#     print("Rows with NULL values in non-nullable columns:")
#     print(invalid_rows)

# # 換行換空格或者拔掉?
# # function for newline replace by space
# def replace_newlines_and_spaces(cell_data):
#     if isinstance(cell_data, str):
#         #return cell_data.replace("\n", "").replace(" ", "")
#         return cell_data.replace("\n", "")
#     return cell_data

# # use applymap to apply function for each cell
# excel_sheet = excel_sheet.applymap(replace_newlines_and_spaces)

# #檢查文字長度
# # 對特殊符號處理
# # a function for cut string
# def truncate_data(data, max_length):
#     if isinstance(data, str) and len(data) > max_length:
#         return data[:max_length]
#     return data

# # a functionn for special charactor
# def remove_special_chars(cell_value):
#     special_chars_pattern = r'[!@#$%^&*_+=\\/:;,<>?"\'`~\[\]{}|]'
#     return re.sub(special_chars_pattern, '', cell_value)

# # each cell max length 300
# for column in excel_sheet.columns:
#     if excel_sheet[column].dtype == "object":
#         excel_sheet[column] = excel_sheet[column].apply(lambda x: truncate_data(x, 300))
#         excel_sheet[column] = excel_sheet[column].apply(lambda x: remove_special_chars(str(x)))



# # write data to sql
# excel_sheet.to_sql(TABLE_NAME, engine, if_exists='append', index=False)




