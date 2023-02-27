# -*- coding: utf-8 -*-
"""
Created on Sat Feb 25 19:10:28 2023
@author: chuan
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time
from bs4 import BeautifulSoup
import pandas as pd

user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
driver = webdriver.Chrome('./chromedriver')
driver.maximize_window()
time.sleep(3)
driver.implicitly_wait(8)
driver.get('https://www.yourator.co/companies')
print(driver.title)
print('Wait...connecting')
driver.implicitly_wait(10)

#Click on cancel button
cancelBtn = driver.find_element(By.XPATH, '//*[@id="headlessui-dialog-1"]/div[2]/div[4]/div/label/span[1]')
cancelBtn.click()
driver.implicitly_wait(5)
cancelBtn = driver.find_element(By.XPATH,'//*[@id="headlessui-dialog-1"]/div[2]/button')
ActionChains(driver).move_to_element(cancelBtn).click(cancelBtn).perform()

#找總共幾頁(抓不到)
last_pageBtn = driver.find_element(By.CLASS_NAME,'last')
last_pageBtn.click()
driver.implicitly_wait(5)
last_page_num = driver.find_element(By.XPATH,'//*[@id="y-company-list-cards"]/div/div[5]/ul/li[7]')
last_page=last_page_num.text
print('共有'+last_page+'頁')

soup = BeautifulSoup(driver.page_source, 'html.parser')
for n in range(1,4):
    driver.maximize_window()
    time.sleep(3)
    driver.implicitly_wait(8)
    driver.get('https://www.yourator.co/companies?page='+str(n))
    print(driver.title)
    print('Page'+str(n)+'...')
    print('Wait...connecting')
    #company name
    driver.implicitly_wait(5)
    title = driver.find_elements(By.CLASS_NAME,'y-new-card__title')
    L=[]
    for item in title:
        print(item.text)
        L.append(item.text)
    data = pd.DataFrame(L,columns=['company_name'])
    #link
    L1=[]
    for k in range(1,31):
        link = driver.find_element(By.XPATH,'//*[@id="y-company-list-cards"]/div/div[4]/div/div['+str(k)+']/a/div[2]/div[1]/div[2]/a')
        print(link.get_attribute('href'))
        L1.append(link.get_attribute('href'))
    data['url']=L1
    #description
    driver.implicitly_wait(5)
    des = driver.find_elements(By.CLASS_NAME,'y-new-card__description.y-company-card__description')
    L2=[]
    for item in des:
        L2.append(item.text)
    L3=[]
    for item in L2:
        content=item.replace('\n','')
        L3.append(content)
    data['description'] = L3
    #city
    L4=[]
    for i in range(1,31):
        city = driver.find_element(By.XPATH,'//*[@id="y-company-list-cards"]/div/div[4]/div/div['+str(i)+']/a/div[2]/div[3]/div[1]/div[1]/a')
        L4.append(city.text)
    
    data['city'] = L4
    #industry
    L5=[]
    for i in range(1,31):
        industry = driver.find_element(By.XPATH,'//*[@id="y-company-list-cards"]/div/div[4]/div/div['+str(i)+']/a/div[2]/div[3]/div[1]/div[2]/a')
        L5.append(industry.text)
    data['industry'] = L5
    #tag (不一定每家都有)
    L6=[]
    for i in range(1,31):
        try:
            tag = driver.find_element(By.XPATH,'//*[@id="y-company-list-cards"]/div/div[4]/div/div['+str(i)+']/a/div[2]/div[3]/div[1]/div[3]')
            L6.append(tag.text)
        except:
            pass
            L6.append(' ')
    L7=[]
    for item in L6:
        a=item.replace('\n',';')
        L7.append(a)
    data['tag'] = L7
    
    #輸出
    data.to_csv('yourator'+str(n)+'.csv',encoding='utf-8-sig')