# -*- coding: utf-8 -*-
"""
Created on Sat Feb 25 19:10:28 2023
@author: chuan
"""
#%%

#Yourator 找公司
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

#找總共幾頁(*抓不到*)
last_pageBtn = driver.find_element(By.CLASS_NAME,'last')
last_pageBtn.click()
driver.implicitly_wait(8)

page_num = driver.find_element(By.XPATH,'//*[@id="y-company-list-cards"]/div/div[5]/ul/li[7]')
last_page_num = page_num.text
print('共有'+last_page_num+'頁')


for n in range(1,58):
    try:
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
    except:
        driver.maximize_window()
        time.sleep(3)
        driver.implicitly_wait(8)
        driver.get('https://www.yourator.co/companies?page=57')
        print(driver.title)
        print('Page'+str(n)+'...')
        print('Wait...connecting')
        #company name
        title = driver.find_elements(By.CLASS_NAME,'y-new-card__title')
        L=[]
        for item in title:
            print(item.text)
            L.append(item.text)
        number=len(L)
        data = pd.DataFrame(L,columns=['company_name'])
        #link
        L1=[]
        for k in range(1,number+1):
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
        for i in range(1,number+1):
            city = driver.find_element(By.XPATH,'//*[@id="y-company-list-cards"]/div/div[4]/div/div['+str(i)+']/a/div[2]/div[3]/div[1]/div[1]/a')
            L4.append(city.text)
        
        data['city'] = L4
        #industry
        L5=[]
        for i in range(1,number+1):
            industry = driver.find_element(By.XPATH,'//*[@id="y-company-list-cards"]/div/div[4]/div/div['+str(i)+']/a/div[2]/div[3]/div[1]/div[2]/a')
            L5.append(industry.text)
        data['industry'] = L5
        #tag (不一定每家都有)
        L6=[]
        for i in range(1,number+1):
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

#%%
#Yourator 找工作
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time
from bs4 import BeautifulSoup
import pandas as pd
import csv

user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
driver = webdriver.Chrome('./chromedriver')
driver.maximize_window()
time.sleep(3)
driver.implicitly_wait(8)
driver.get('https://www.yourator.co/jobs?sort=newest')
print(driver.title)
print('Wait...connecting')
driver.implicitly_wait(10)

#Click on cancel button
cancelBtn = driver.find_element(By.CLASS_NAME, '//*[@id="headlessui-dialog-31"]/div[2]/button')
cancelBtn.click()
driver.implicitly_wait(10)

# Click on the job category dropdown---爬不下來
category_dropdown = driver.find_element(By.XPATH, '//*[@id="headlessui-listbox-button-47"]')
category_dropdown.click()
time.sleep(10)

category=['前端工程','後端工程','全端工程','行動裝置開發',
'遊戲開發','測試工程','DevOps%20%2F%20SRE','韌體%20%2F%20電子電路',
'硬體工程','半導體','光電工程','資料工程%20%2F%20機器學習',
'MIS%20%2F%20網路管理','通訊電信','行銷企劃%20%2F%20社群經營',
'編輯%20%2F%20內容經營','廣告創意%20%2F%20企劃','攝影%20%2F%20影音製作',
'Growth Hacker','媒體公關%20%2F%20宣傳採買','人資',
'財務%20%2F%20會計','行政','營運','客戶服務','法務','商業開發',
'通路開發','實體經營','市場分析','銷售業務',
'專案%20%2F%20產品管理','UIUX%20%2F%20視覺設計',
'3D%20%2F%20動畫設計','教育%20%2F%20教學','外語高手','研究人員',
'其他']
driver = webdriver.Chrome('./chromedriver')
driver.maximize_window()
time.sleep(3)
driver.implicitly_wait(8)


for num in range(7,38):
    driver.get('https://www.yourator.co/jobs?category[]='+category[num])
    driver.implicitly_wait(10)

    #Click on cancel button
    try:
        cancelBtn = driver.find_element(By.XPATH, '//*[@id="headlessui-dialog-31"]/div[2]/button')
        cancelBtn.click()
        driver.implicitly_wait(10)
        
        for x in range(1, 4):
            driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
            time.sleep(5)
            
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        results = soup.find_all("p", class_="flex-initial")
        
        title=[]
        company=[]
        for n in range(len(results)):
            if n == 0 or n%2 == 0:
                print(results[n].getText())
                title.append(results[n].getText())
            else:
                company.append(results[n].getText())
        
        url=[]
        results = soup.find_all(["a","href"],target="_blank")
        for result in results:
            if '/companies/' in result.get("href"):
                print(result.get("href"))
                url.append(result.get("href"))
        url.pop(-1)
        job_list=pd.DataFrame(data=company,columns=["company"])
        job_list["title"]=title
        job_list["url"]=url

        job_list.to_csv(category[num]+'.csv',encoding='utf-8-sig')
    except:
        for x in range(1, 4):
            driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
            time.sleep(5)
            
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        results = soup.find_all("p", class_="flex-initial")
        
        title=[]
        company=[]
        for n in range(len(results)):
            if n == 0 or n%2 == 0:
                print(results[n].getText())
                title.append(results[n].getText())
            else:
                company.append(results[n].getText())
        
        url=[]
        results = soup.find_all(["a","href"],target="_blank")
        for result in results:
            if '/companies/' in result.get("href"):
                print(result.get("href"))
                url.append(result.get("href"))
        url.pop(-1)
        job_list=pd.DataFrame(data=company,columns=["company"])
        job_list["title"]=title
        job_list["url"]=url

        job_list.to_csv(category[num]+'.csv',encoding='utf-8-sig')
#%%
#爬內頁
for num in range(1,38):
    with open("C:/Users/chuan/OneDrive/桌面/jobs_20230801/"+category[num]+".csv",encoding='utf-8-sig') as csvfile:

    # 讀取 CSV 檔案內容
      rows = csv.reader(csvfile)
    
    # 以迴圈輸出每一列
      L=[]
      for row in rows:
        print(row)
        L.append(row)
    df=pd.DataFrame(L,columns=L[0])
    df=df.drop(index=0)
    
    driver = webdriver.Chrome('./chromedriver')
    driver.maximize_window()
    time.sleep(3)
    driver.implicitly_wait(8)
    
    work_location=[]
    company_address=[]
    work_type=[]
    job_description=[]
    requirements=[]
    benefit=[]
    salary=[]
    for item in df['url']:
        driver.get('https://www.yourator.co'+str(item))
        driver.implicitly_wait(10)
    
        for x in range(1, 4):
            driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
            time.sleep(5)
            
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        results = soup.find_all("p",class_="basic-info__address inline-flex flex-wrap")
        
        try:
            for n in range(len(results)):
                print(results[n].getText())
            work_location.append(results[0].getText().strip("\n"))
            company_address.append(results[1].getText().strip("\n"))
            
            results = soup.find_all("p",class_="basic-info__job_type inline-flex flex-wrap")
            for n in results:
                print(n.getText().strip("\n"))
                work_type.append(n.getText().strip("\n"))

            results = soup.find_all("section",class_="content__area unreset")
            for n in range(len(results)):
                print(results[n].getText().strip("\n"))
            job_description.append(results[0].getText().strip("\n"))
            requirements.append(results[1].getText().strip("\n"))

            results = soup.find_all("section",class_="content__area")
            for n in range(len(results)):
                print(results[n].getText().strip("\n"))
            salary.append(results[-2].getText().strip("\n"))
        except:
            for n in range(len(results)):
                print(results[n].getText())
            work_location.append(results[0].getText().strip("\n"))
            
            results = soup.find_all("p",class_="basic-info__job_type inline-flex flex-wrap")
            for n in results:
                print(n.getText().strip("\n"))
                work_type.append(n.getText().strip("\n"))
            
            results = soup.find_all("section",class_="content__area unreset")
            for n in range(len(results)):
                print(results[n].getText().strip("\n"))
            job_description.append(results[0].getText().strip("\n"))
            requirements.append(results[1].getText().strip("\n"))
            benefit.append(results[2].getText().strip("\n"))

            results = soup.find_all("section",class_="content__area")
            for n in range(len(results)):
                print(results[n].getText().strip("\n"))
            salary.append(results[-2].getText().strip("\n"))
        
    df['work_location']=work_location
    df['company_address']=company_address
    df['work_type']=work_type
    df['job_description']=job_description
    df['requirements']=requirements
    df['benefit']=benefit
    df['salary']=salary

    df.to_csv("C:/Users/chuan/OneDrive/桌面/jobs_20230806/"+category[num]+".csv", index=False)


#%%
#send_keys
for num in range(len(category)):
    search_bar = driver.find_element(By.XPATH,'//*[@id="job-list-app"]/section[1]/section/div[2]/div[1]/div/input')
    search_bar.send_keys(category[num])
    clickBtn = driver.find_element(By.XPATH,'//*[@id="job-list-app"]/section[1]/section/div[2]/div[1]/div/span/span/i')
    clickBtn.click()

    #job_title
    title = driver.find_elements(By.CLASS_NAME,'y-card-content-title')
    L=[]
    for item in title:
        print(item.text)
        L.append(item.text)
    data = pd.DataFrame(L,columns=['job_title'])
    #company_name
    company = driver.find_elements(By.CLASS_NAME,'y-card-content-subtitle')
    L1=[]
    for item in company:
        print(item.text)
        L1.append(item.text)
    data['company']=L1
    #category
    L2=[]
    for i in range(1,21):
        company = driver.find_element(By.XPATH,'//*[@id="y-job-list-cards"]/div/div[5]/div['+str(i)+']/div/div/div[3]/div[3]/a[1]')
        L2.append(company.text)
    data['category']=L2
    #salary
    salary = driver.find_elements(By.CLASS_NAME,'salary-description')
    L3=[]
    for item in salary:
        print(item.text)
        L3.append(item.text)
    data['salary']=L3
    #tag
    L4=[]
    for i in range(1,21):
        tag = driver.find_element(By.XPATH,'//*[@id="y-job-list-cards"]/div/div[5]/div['+str(i)+']/div/div/div[3]/div[3]/a[2]')
        L4.append(tag.text)
    data['tag']=L4
    #url
    L5=[]
    for k in range(1,21):
        link = driver.find_element(By.XPATH,'//*[@id="y-job-list-cards"]/div/div[5]/div['+str(k)+']/div/div/div[3]/div[1]/a')
        print(link.get_attribute('href'))
        L5.append(link.get_attribute('href'))
    data['url']=L5
    #輸出
    data.to_csv('yourator'+str(num)+'.csv',encoding='utf-8-sig')
#test    
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
driver = webdriver.Chrome('./chromedriver')
driver.maximize_window()
time.sleep(3)
driver.implicitly_wait(8)

for k in category[0:2]:
    my_dict={}
    job_title=[]
    company_name=[]
    job_category=[]
    job_salary=[]
    job_tag=[]
    job_url=[]
    my_dict['cate']=k
    my_dict['job_title']=job_title
    my_dict['company_name']=company_name
    my_dict['job_category']=job_category
    my_dict['job_salary']=job_salary
    my_dict['job_tag']=job_tag
    my_dict['job_url']=job_url
    for n in range(1,21):
        try:
            web_url='https://www.yourator.co/jobs?category[]='+k+'&sort=newest'+'&page='+str(n)
            driver.get(web_url)
            print(driver.title)
            print('Wait...connecting')
            driver.implicitly_wait(10)
            #job_title
            title = driver.find_elements(By.CLASS_NAME,'y-card-content-title')
            for item in title:
                print(item.text)
                my_dict['job_title'].append(item.text)
            #company_name
            company = driver.find_elements(By.CLASS_NAME,'y-card-content-subtitle')
            for item in company:
                print(item.text)
                my_dict['company_name'].append(item.text)
            #category
            for i in range(1,21):
                company = driver.find_element(By.XPATH,'//*[@id="y-job-list-cards"]/div/div[5]/div['+str(i)+']/div/div/div[3]/div[3]/a[1]')
                my_dict['job_category'].append(company.text)
            #salary
            salary = driver.find_elements(By.CLASS_NAME,'salary-description')
            for item in salary:
                print(item.text)
                my_dict['job_salary'].append(item.text)
            #tag
            for i in range(1,21):
                tag = driver.find_element(By.XPATH,'//*[@id="y-job-list-cards"]/div/div[5]/div['+str(i)+']/div/div/div[3]/div[3]/a[2]')
                my_dict['job_tag'].append(tag.text)
            #url
            for k in range(1,21):
                link = driver.find_element(By.XPATH,'//*[@id="y-job-list-cards"]/div/div[5]/div['+str(k)+']/div/div/div[3]/div[1]/a')
                print(link.get_attribute('href'))
                my_dict['job_url'].append(link.get_attribute('href'))
        except:
            pass
    Data=pd.DataFrame.from_dict(my_dict,orient='index').T
    Data['job_title']
    Data.to_csv('yourator_test.csv',encoding='utf-8-sig')
#%%
#test    
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
driver = webdriver.Chrome('./chromedriver')
driver.maximize_window()
time.sleep(3)
driver.implicitly_wait(8)

for k in category[0:3]:
    my_dict={}
    job_title=[]
    company_name=[]
    job_category=[]
    job_salary=[]
    job_tag=[]
    job_url=[]
    for n in range(1,5):
        try:
            web_url='https://www.yourator.co/jobs?category[]='+k+'&sort=newest&page='+str(n)
            driver.get(web_url)
            print(driver.title)
            print('Wait...connecting')
            driver.implicitly_wait(10)
            #job_title
            title = driver.find_elements(By.CLASS_NAME,'y-card-content-title')
            for item in title:
                print(item.text)
                job_title.append(item.text)
            time.sleep(5)
            #company_name
            company = driver.find_elements(By.CLASS_NAME,'y-card-content-subtitle')
            for item in company:
                print(item.text)
                company_name.append(item.text)
            time.sleep(5)
            #job_category
            for i in range(1,21):
                category = driver.find_element(By.XPATH,'//*[@id="y-job-list-cards"]/div/div[5]/div['+str(i)+']/div/div/div[3]/div[3]/a[1]')
                job_category.append(category.text)
            time.sleep(5)
            #job_salary
            salary = driver.find_elements(By.CLASS_NAME,'salary-description')
            for item in salary:
                print(item.text)
                job_salary.append(item.text)
            time.sleep(5)
            #tag
            for i in range(1,21):
                tag = driver.find_element(By.XPATH,'//*[@id="y-job-list-cards"]/div/div[5]/div['+str(i)+']/div/div/div[3]/div[3]/a[2]')
                job_tag.append(tag.text)
            time.sleep(5)
            #url
            for n in range(1,21):
                link = driver.find_element(By.XPATH,'//*[@id="y-job-list-cards"]/div/div[5]/div['+str(n)+']/div/div/div[3]/div[1]/a')
                print(link.get_attribute('href'))
                job_url.append(link.get_attribute('href'))
        except:
            pass
    data=pd.DataFrame(data=job_title,columns=['job_title'])
    data['company_name']=company_name
    data['job_category']=job_category
    data['job_salary']=job_salary
    data['job_tag']=job_tag
    data['job_url']=job_url
    data.to_csv('yourator'+k+'.csv',encoding='utf-8-sig')    
#%%
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
driver = webdriver.Chrome('./chromedriver')
driver.maximize_window()
wait = WebDriverWait(driver, 10)

for k in category[4:38]: #跑不同職缺分類
    my_dict={}
    job_title=[]
    company_name=[]
    job_category=[]
    job_salary=[]
    job_tag=[]
    job_url=[]
    for n in range(1,6): #先抓每個職缺分頁的前五頁
        try:
            web_url='https://www.yourator.co/jobs?category[]='+k+'&sort=newest&page='+str(n)
            driver.get(web_url)
            print(driver.title)
            print('Wait...connecting')
            
            wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'y-card-content-title')))
            ###job_title
            title = driver.find_elements(By.CLASS_NAME, 'y-card-content-title')
            for item in title:
                if item.text!='':
                    print(item.text)
                    job_title.append(item.text)
                else:
                    job_title.append('')

            wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'y-card-content-subtitle')))
            ###company_name
            company = driver.find_elements(By.CLASS_NAME, 'y-card-content-subtitle')
            for item in company:
                if item.text !='':
                    print(item.text)
                    company_name.append(item.text)
                else:
                    company_name.append('')
            ###job_category
            for i in range(1,21):
                wait.until(EC.presence_of_element_located((By.XPATH, f'//*[@id="y-job-list-cards"]/div/div[5]/div[{i}]/div/div/div[3]/div[3]/a[1]')))
                category_elem = driver.find_element(By.XPATH, f'//*[@id="y-job-list-cards"]/div/div[5]/div[{i}]/div/div/div[3]/div[3]/a[1]')
                if category_elem.text !='':
                    job_category.append(category_elem.text)
                else:
                    job_category.append('')

            wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'salary-description')))
            ###job_salary
            salary = driver.find_elements(By.CLASS_NAME, 'salary-description')
            for item in salary:
                if salary.count() != category_elem.count():
                    print('數量不一致')
                    break
                else:
                    print(item.text)
                    job_salary.append(item.text)
            ###tag
            for i in range(1,21):
                wait.until(EC.presence_of_element_located((By.XPATH, f'//*[@id="y-job-list-cards"]/div/div[5]/div[{i}]/div/div/div[3]/div[3]/a[2]')))
                tag = driver.find_element(By.XPATH, f'//*[@id="y-job-list-cards"]/div/div[5]/div[{i}]/div/div/div[3]/div[3]/a[2]')
                if tag.text != '':
                    job_tag.append(tag.text)
                else:
                    job_tag.append('')
            ###link   
            for n in range(1,21):
                link = driver.find_element(By.XPATH,'//*[@id="y-job-list-cards"]/div/div[5]/div['+str(n)+']/div/div/div[3]/div[1]/a')
                if link.get_attribute('href')!='':
                    print(link.get_attribute('href'))
                    job_url.append(link.get_attribute('href'))
                else:
                    job_url.append('')
        except:
            job_salary.append('')
            job_tag.append('')
            job_url.append('')
            pass
    data=pd.DataFrame(data=job_title,columns=['job_title'])
    data['company_name']=company_name
    data['job_category']=job_category
    data['job_salary']=job_salary
    data['job_tag']=job_tag
    data['job_url']=job_url
    data.to_csv('yourator'+k+'.csv',encoding='utf-8-sig')

#%%
#內頁
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
driver = webdriver.Chrome('./chromedriver')
driver.maximize_window()
time.sleep(3)
driver.implicitly_wait(8)
for url in data['url']:
    driver.get(url)
    print(driver.title)
    print('Wait...connecting')
    driver.implicitly_wait(10)

    #Click on cancel button
    cancelBtn = driver.find_element(By.XPATH, '//*[@id="headlessui-dialog-1"]/div[2]/div[4]/div/label/span[1]')
    cancelBtn.click()
    driver.implicitly_wait(5)
    cancelBtn = driver.find_element(By.XPATH,'//*[@id="headlessui-dialog-1"]/div[2]/button')
    ActionChains(driver).move_to_element(cancelBtn).click(cancelBtn).perform()
    #標題&內容
    header=[]
    head = driver.find_elements(By.CLASS_NAME,'job-heading')
    for item in head:
        print(item.text)
        header.append(item.text)
    context=[]
    for i in range(1,7):
        content = driver.find_element(By.XPATH,'/html/body/div[6]/section[3]/div/div/div[1]/section['+str(i)+']')
        print(content.text)
        context.append(content.text)
    dic={header[0]:context[0],
         header[1]:context[1],
         header[2]:context[2],
         header[3]:context[3],
         header[4]:context[4],
         header[5]:context[5]}
    detailed_data=pd.DataFrame.from_dict(dic,orient='index').T
