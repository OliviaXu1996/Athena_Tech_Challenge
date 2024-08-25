import pandas as pd

""" 
data_preprocess:

input:
output:
"""
file_path_1 = '/Users/wenyaoxu/Desktop/Athena_technical_challenge/Data/Equitable_Owner_History.csv'

# df = pd.read_csv(file_path_1)
# df['Reallocation_Date'] = pd.to_datetime(df['Reallocation_Date'],format='%d/%m/%Y').dt.strftime('%Y/%m/%d')

# df.to_csv('output_file.csv',index=False)


file_path_2 = '/Users/wenyaoxu/Desktop/Athena_technical_challenge/Data/Accounting_Entry.csv'
df = pd.read_csv(file_path_2)
loan_account_ = df['Loan_Account_Id'].unique()
print(loan_account)
