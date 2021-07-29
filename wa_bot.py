from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.common.by import By
import time
import string

import ai

driver = webdriver.Chrome()
driver.get('https://web.whatsapp.com')

input()

wait = WebDriverWait(driver, 30)

xpath = '//*[@id="main"]/footer/div[1]/div[2]/div/div[1]/div/div[2]'
out_box = wait.until(EC.presence_of_element_located((By.XPATH, xpath))) 

while True: 
    message = driver.find_elements_by_xpath("//span[@class='i0jNr selectable-text copyable-text']")[-1].text.lower()
    print(f'Message: {message}')

    if message[:3] == 'mom':
        print('Is a challenge')
        response = ai.run(message[3:])
        response = ''.join(c for c in response if c.isalnum() or c == ' ')
        out_box.send_keys('Max-o-Matic: ' + response + Keys.ENTER)
    time.sleep(1)

