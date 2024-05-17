# Import necessary libraries
import os
import time
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

service = Service(ChromeDriverManager().install())
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

driver.implicitly_wait(10)
tr_tags = driver.find_elements(By.TAG_NAME, 'tr')[1:]
a_tags = [tr.find_element(By.TAG_NAME, 'a') for tr in tr_tags]

if not os.path.exists('tables'):
    os.makedirs('tables')

def extract_info_from_html(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    person_data = {}
    
    name_tag = soup.find('td', {'class': 'vertical_col_data'})
    person_data['Name'] = name_tag.text.strip() if name_tag else 'N/A'
    
    rows = soup.find_all('tr')
    for row in rows:
        cols = row.find_all('td')
        if len(cols) == 2:
            key = cols[0].text.strip().replace(' :', '')
            value = cols[1].text.strip()
            person_data[key] = value
    
    experience_table = soup.find('table', {'id': 'rounded-cornerA'})
    if experience_table:
        experience_rows = experience_table.find_all('tr')[2:]  # Skip header
        experiences = []
        for exp_row in experience_rows:
            exp_cols = exp_row.find_all('td')
            if len(exp_cols) >= 6:
                experience = {
                    'Designation/Level': exp_cols[1].text.strip(),
                    'Ministry/Department/Office/Location': exp_cols[2].text.strip(),
                    'Organisation': exp_cols[3].text.strip(),
                    'Experience(major/minor)': exp_cols[4].text.strip(),
                    'Period(From/To)': exp_cols[5].text.strip(),
                }
                experiences.append(experience)
        person_data['Experiences'] = experiences
    
    return person_data

combined_data = []

for a in a_tags:
    try:
        a.click()
        driver.switch_to.window(driver.window_handles[1])
        time.sleep(2)  

        # Extract the HTML content and parse it
        html_content = driver.page_source
        person_data = extract_info_from_html(html_content)
        combined_data.append(person_data)
                
    finally:
        driver.close()
        driver.switch_to.window(driver.window_handles[0])

for person in combined_data:
    experiences = person.pop('Experiences', [])
    for idx, exp in enumerate(experiences):
        for key, value in exp.items():
            person[f'Experience_{idx + 1}_{key}'] = value

df = pd.DataFrame(combined_data)

output_dir = 'tables'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

output_format = 'excel'  
output_filename = os.path.join(output_dir, 'combined_data.xlsx') if output_format == 'excel' else os.path.join(output_dir, 'combined_data.csv')

if output_format == 'excel':
    df.to_excel(output_filename, index=False)
else:
    df.to_csv(output_filename, index=False)

print(f"Data saved to {output_filename}")

# Close the driver
driver.quit()
