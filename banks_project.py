from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np
import sqlite3
from datetime import datetime 


def log_progress(message):
    timestamp_format = '%Y-%h-%d-%H:%M:%S'
    now = datetime.now() 
    timestamp = now.strftime(timestamp_format) 
    with open("./code_log.txt","a") as f: 
        f.write(timestamp + ' : ' + message + '\n')    

url = 'https://web.archive.org/web/20230908091635/https://en.wikipedia.org/wiki/List_of_largest_banks'
table_attribs = ['Bank_Name', 'Market_Cap']
csv_path = './banks.csv'
log_progress('Preliminaries complete. Initiating ETL process')
def extract(url, table_attribs):
    page = requests.get(url).text
    data = BeautifulSoup(page, 'html.parser')
    df = pd.DataFrame(columns=table_attribs)
    tables = data.find_all('tbody')
    rows = tables[0].find_all('tr')

    for row in rows:
        col = row.find_all('td')
        if len(col) >= 2:  
            a_tags = col[1].find_all('a')
            bank_name=a_tags[1]
            market_cap = col[2].get_text(strip=True) 
            data_dict = {"Bank_Name": bank_name, "Market_Cap": market_cap}
            df1 = pd.DataFrame(data_dict, index=[0])
            df = pd.concat([df, df1], ignore_index=True)


    return df

def transform(df):
   exchange_rates = {'GBP': 0.73, 'EUR': 0.85, 'INR': 74.93}
   df['Market_Cap'] = pd.to_numeric(df['Market_Cap'])
   df['MC_GBP_Billion'] = np.round(df['Market_Cap'] * exchange_rates['GBP'], 2)
   df['MC_EUR_Billion'] = np.round(df['Market_Cap'] * exchange_rates['EUR'], 2)
   df['MC_INR_Billion'] = np.round(df['Market_Cap'] * exchange_rates['INR'], 2)
   return df

def load_to_csv(df,csv_path):
  df.to_csv(csv_path)

def load_to_db(df, sql_connection, table_name):
    df.to_sql(table_name, sql_connection, if_exists='replace', index=False)

def run_query(query_statement, sql_connection):
    print(query_statement)
    query_output = pd.read_sql(query_statement, sql_connection)
    print(query_output)
df = extract(url, table_attribs)
log_progress('Data extraction complete. Initiating Transformation process')
df = transform(df)
log_progress("Data transformation complete. Initiating Loading process")
load_to_csv(df,csv_path)
log_progress('Data saved to CSV file')
sql_connection = sqlite3.connect('Banks.db')
log_progress('SQL Connection initiated')
load_to_db(df,sql_connection,"Largest_banks")
log_progress('Data loaded to Database as a table, Executing queries')
run_query('SELECT * FROM Largest_banks',sql_connection)
run_query('SELECT AVG(MC_GBP_Billion) FROM Largest_banks',sql_connection)
run_query('SELECT Bank_Name from Largest_banks LIMIT 5',sql_connection)
log_progress('Process Complete')
sql_connection.close()
log_progress('Server Connection closed')

