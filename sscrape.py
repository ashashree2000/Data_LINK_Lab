# -*- coding: utf-8 -*-
"""sscrape.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1nxB9kJOoq2DW5lxcferHyTrRTEznqEqv
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

url = "https://himkosh.nic.in/eHPOLTIS/PublicReports/wfrmBudgetAllocationbyFD.aspx"


driver = webdriver.Chrome()
driver.get(url)

response = requests.get(url)
content = response.content


WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'txtFromDate')))

from_date = driver.find_element(By.ID, "txtFromDate")
from_date.clear()
from_date.send_keys("01/04/2018")


to_date = driver.find_element(By.ID, "txtQueryDate")
to_date.clear()
to_date.send_keys("31/03/2022")


# report_data = Select(driver.find_element(By.ID, "ctl00_ContentPlaceHolder1_ddlReportData"))
# report_data.select_by_visible_text("Demand and HOA Wise Summary")


unit = driver.find_element(By.ID, "MainContent_rbtUnit_0")
unit.click()
# unit.select_by_visible_text("Rupees")
# Find and click the submit button
submit_button = driver.find_element(By.ID, "btnGetdata")
submit_button.click()


time.sleep(5)

soup = BeautifulSoup(content, 'html.parser')


table = soup.find('table')


data = []
for row in table.find_all('td'):
    cols = row.find_all('td')
    cols = [col.text.strip() for col in cols]
    data.append(cols)


df = pd.DataFrame(data)
print(data)
driver.get(url)
