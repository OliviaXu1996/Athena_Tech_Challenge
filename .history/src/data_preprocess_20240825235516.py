import pandas as pd

""" 
data_preprocess:

input:
output:
"""
file_path_1 = '/Users/wenyaoxu/Desktop/Athena_technical_challenge/Data/Equitable_Owner_History.csv'

df_1 = pd.read_csv(file_path_1)
df_1['Reallocation_Date'] = pd.to_datetime(df_1['Reallocation_Date'],format='%d/%m/%Y').dt.strftime('%Y/%m/%d')
df_1['From_Equitable_Owner_Id'] = df_1['From_Equitable_Owner_Id'].fillna('NULL')
df_1.to_csv('output_file.csv',index=False)


/


