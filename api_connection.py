# %%
import pandas as pd

# %%
import urllib.parse
from sqlalchemy import create_engine, text

raw_pw = "eric!!@@##"
enc_pw = urllib.parse.quote_plus(raw_pw)  # handles all special chars
url = f"postgresql://eric:{enc_pw}@172.16.19.203:5432/test_dw"
engine = create_engine(url)


# %%
from sqlalchemy import inspect

inspector = inspect(engine)
print("Tables in test_dw:", inspector.get_table_names())
# If you need columns for a specific table:
print("Columns in inventory_table:", inspector.get_columns('bin_contents'))


# %%
erp_df = pd.read_sql(
    text("""
    SELECT
        location_code,
        bin_code,
        item_no,
        model_name,
        quantity_base,
        available_to_allocate
    FROM bin_contents
    """),
    con=engine
)

# %%
erp_df = erp_df[
    erp_df['location_code'].isin(['INDY', 'IRVINE_CA', 'IRVINE_VN']) &
    ~erp_df['bin_code'].isin(['113.02.02','113.03.02','113.04.01','LOADING','SEALED'])
]

# %%
from business_process import inventory_process

# %%
final_df = inventory_process(erp_df)

# %%
from sqlalchemy import create_engine

final_df.to_sql(
    name='final_inventory_plan',   # new table name in Postgres
    con=engine,
    if_exists='replace',           # options: 'fail', 'replace', 'append'
    index=False                    # don’t write DataFrame’s index as a column
)

#print("Table ‘final_inventory_plan’ created with", len(final_df), "rows.")


# %%



