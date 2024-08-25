import pandas as pd

""" 
data_preprocess:

input:
output:
"""
file_path = '/Users/wenyaoxu/Desktop/Athena_technical_challenge/Data/Equitable_Owner_History.csv'

df = pd.read_csv(file_path)
df['Reallocation_Date'] = pd.to_datetime(df['Reallocation_Date'],format='%d/%m/%Y').dt.strftime('%Y/%m/%d')

df.to_csv('output_file.csv',index=False)

