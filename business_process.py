import pandas as pd

def inventory_process(df_erp):
    df = pd.read_excel('3-3 -2025 USA Planning Dahua Product_Formula updated.xlsx', sheet_name="Inventory Planning", header=3)


    #erp_inventory = pd.read_excel('Inventory.xlsx')


    #erp_columns = ['location_code', 'bin_code', 'Item No.', 'Model Name', 'Quantity', 'Available to Allocate']


    #erp_inventory = erp_inventory[erp_columns]
    filtered_erp_inventory = df_erp


    #excluded_bincode = ['113.02.02','113.03.02', '113.04.01', 'LOADING', 'SEALED']
    #filtered_erp_inventory = filtered_erp_inventory[filtered_erp_inventory['bin_code'].apply(lambda x: True if x not in excluded_bincode else False)]

    def inventory_calulator(pn_number, location):
        # Input the pn number and the location_code, returns the inventory amont based on those condition
        df = filtered_erp_inventory[(filtered_erp_inventory['location_code'] == location) & (filtered_erp_inventory['item_no'] == pn_number)] 
        return df['available_to_allocate'].sum()

    def indy_inventory_calculator(df):
        df = df.copy()
        df['current_inventory'] = df['Current PN'].apply(lambda x: inventory_calulator(x, 'INDY'))
        df['old_inventory'] = df['Old PN/Notes'].apply(lambda x: inventory_calulator(x, 'INDY'))
        df['vn_inventory'] = df['越南 PN (Vietnam)'].apply(lambda x: inventory_calulator(x, 'INDY'))
        df['sum'] = df['current_inventory'] + df['old_inventory'] + df['vn_inventory']
        return df['sum']

    def irvine_inventory_calculator(df):
        df = df.copy()
        df['current_inventory'] = df['Current PN'].apply(lambda x: inventory_calulator(x, 'IRVINE_CA')) 
        df['old_inventory'] = df['Old PN/Notes'].apply(lambda x: inventory_calulator(x, 'IRVINE_CA'))
        df['vn_inventory'] = df['越南 PN (Vietnam)'].apply(lambda x: inventory_calulator(x, 'IRVINE_VN'))
        df['sum'] = df['current_inventory'] + df['old_inventory'] + df['vn_inventory']
        return df['sum']

    cleaned_df = df[['General Model','EXTERNAL MODEL NAME', 'Lumi Model', 'Replacement', 'Current PN', 'Old PN/Notes', '越南 PN (Vietnam)']]

    cleaned_df = cleaned_df.copy()

    cleaned_df['Irvine On Hand'] = irvine_inventory_calculator(cleaned_df)
    cleaned_df['Indy On Hand'] = indy_inventory_calculator(cleaned_df)
    cleaned_df['US On Hand'] = cleaned_df['Irvine On Hand'] + cleaned_df['Indy On Hand']

    column_mapping = {
    'General Model':        'general_model',
    'EXTERNAL MODEL NAME':  'external_model_name',
    'Lumi Model':           'lumi_model',
    'Replacement':          'replacement',
    'Current PN':           'current_pn',
    'Old PN/Notes':         'old_pn_notes',
    '越南 PN (Vietnam)':     'vn_pn',
    'Irvine On Hand':       'irvine_on_hand',
    'Indy On Hand':         'indy_on_hand',
    'US On Hand':           'us_on_hand'
  }
    cleaned_df = cleaned_df.rename(columns=column_mapping)
    
    return cleaned_df





