# %%
import concurrent.futures
import csv
import json
import os
import queue
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

import pandas as pd
import pg8000
import psycopg2
from bs4 import BeautifulSoup
from psycopg2.extras import RealDictCursor
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
#Creating the Service object
service = Service(ChromeDriverManager().install())

#Defining the service driver
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=service, options=options)

main_url = 'https://supremo.nic.in/KnowYourOfficerIAS.aspx'
driver.get(main_url)


driver.find_element(By.CLASS_NAME, 'chosen-choices').click()
ul = driver.find_element(By.CLASS_NAME, 'chosen-results')
li = ul.find_elements(By.TAG_NAME, 'li')

for i in range(0, len(li)):
    print(i)
    driver.find_element(By.CLASS_NAME, 'chosen-choices').click()
    time.sleep(0.5)
    li = ul.find_elements(By.TAG_NAME, 'li')
    li[i].click()
    break


button = driver.find_element(By.CSS_SELECTOR, '#btnSubmit')
button.click()


tr_tags = driver.find_elements(By.TAG_NAME, 'tr')[1:]
a_tags = [tr.find_element(By.TAG_NAME, 'a') for tr in tr_tags]

print(a_tags)


# Set an implicit wait for the driver
driver.implicitly_wait(10)

# Create a directory to save the tables
if not os.path.exists('tables'):
    os.makedirs('tables')


import pandas as pd
from selenium.webdriver.common.by import By

def extract_table(driver, a):
    try:
        a.click()
        driver.switch_to.window(driver.window_handles[1])
        table = driver.find_element(By.TAG_NAME, "table")
        
        #Converting table to DataFrame
        df = pd.read_html(table.get_attribute('outerHTML'))[0]
        
        #Drop rows and columns with all null values
        df.dropna(axis=0, how='all', inplace=True)
        df.dropna(axis=1, how='all', inplace=True)
        
        return df
                
    finally:
        driver.close()
        driver.switch_to.window(driver.window_handles[0])

import os
import pandas as pd
from bs4 import BeautifulSoup
def save_tables_to_excel(html_files_dir, output_dir):
    #output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    #working on HTML files in the directory
    for filename in os.listdir(html_files_dir):
        if filename.endswith('.html'):
            filepath = os.path.join(html_files_dir, filename)
            #reading the file
            with open(filepath, 'r', encoding='utf-8') as file:
                html_content = file.read()

            # Parsing the HTML content
            soup = BeautifulSoup(html_content, 'html.parser')

            # Finding all tables in the HTML file
            tables = soup.find_all('table')

            #convert each table to a DataFrame
            for i, table in enumerate(tables):
                df = pd.read_html(str(table))[0]  # Assuming the first table is the relevant one

                # Drop rows and columns with all null values
                df.dropna(axis=0, how='all', inplace=True)
                df.dropna(axis=1, how='all', inplace=True)

                #Converting MultiIndex columns to regular columns
                df.columns = ['_'.join(col).strip() if isinstance(col, tuple) else col for col in df.columns.values]

                #Save the DataFrame to Excel 
                output_filename = f"{filename.split('.')[0]}_table_{i + 1}"
                if output_format == 'excel':
                    df.to_excel(os.path.join(output_dir, f"{output_filename}.xlsx"), index=False)
                else:
                    print("Invalid output format specified. Please choose 'excel' or 'csv'.")

html_files_dir = 'tables'
output_dir = 'tables'
output_format = 'excel'

save_tables_to_excel(html_files_dir, output_dir)




for a in a_tags:
    extract_table(a)
