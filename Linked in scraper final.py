#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# install all the needed packages
get_ipython().system('pip install selenium')
from selenium import webdriver
import time
from selenium.webdriver import Chrome
from selenium.webdriver.common.keys import Keys
import pandas as pd

# initialize webdriver and access the linked in page
driver = webdriver.Chrome()
driver.get("https://www.linkedin.com/jobs/search/?keywords=analyst")

# scroll down using the end key (to load more jobs) 1000 times till it stops loading more jobs
i=0
while i<1000:
    scroll = driver.find_element_by_tag_name('body').send_keys(Keys.END)
    i+=1

# gather all the links present on the page using xpath
link_list=[]
elems = driver.find_elements_by_xpath("//a[@href]")
for elem in elems:
    link=elem.get_attribute("href")
    link_list.append(link)
driver.close()

# get rid of non-job links by using the structure of the links and make a new list 
links=[]
for link in link_list:
    if 'https://www.linkedin.com/jobs/view/' in link:
        links.append(link)
        
# initialize all the lists to store the data corresponding to the particular variable
Pay=[]
Place=[]
Position=[]
Company=[]
Seniority=[]
Employment_Type=[]
Job_Function=[]
Industry=[]
elements=[]
Linklist=[]

# collect data by going to each link in the list 'links'
for link in links:
    driver = webdriver.Chrome()
    driver.get(link)
    # Extracts the job post link
    Linklist.append(link)
    # Extracts the job position/ title
    # try and except block
    try:
        # this identifies the element and appends it if it exists
        element = driver.find_element_by_xpath("/html/body/main/section[1]/section[2]/div/div[1]/div/h1").text
        Position.append(element)
    except NoSuchElementException:
        # NoSuchElementException is thrown if element is not present here we fill value as '-'
        Position.append('-')
    # Extracts the job place
    try:
        element1 = driver.find_element_by_xpath("/html/body/main/section[1]/section[2]/div/div[1]/div/h4/div[1]/span[2]").text
        Place.append(element1)
    except NoSuchElementException:
        Place.append('-')
    # Extracts the estimated job pay
    try :
        element3 = driver.find_element_by_xpath("/html/body/main/section[1]/section[3]/div/div").text
        if len(element3)< 37:
            Pay.append(element3)
        else :
            Pay.append('-')
    except NoSuchElementException:
        Pay.append('-')
    # Extracts the job seniority, employment type, industry and job function (they all have same xpath)
    # we will sort and assign them later
    try:
        element4 = driver.find_element_by_xpath("/html/body/main/section[1]/section[4]/ul").text
        elements.append(element4)            
    except NoSuchElementException:
        elements.append('-')
    # Extracts the Company
    try:
        element5=driver.find_element_by_xpath("/html/body/main/section[1]/section[2]/div/div[1]/div/h4/div[1]/span[1]/a").text
        Company.append(element5)
    except NoSuchElementException:
        Company.append('-')
    driver.close()

# Sort and assign the seniority, employment type, industry and job function from elements
for e in elements:
    #if element exists
    if len(e)>1:
        e=e.splitlines()
        if len(e)>7:            
            Seniority.append(e[1])
            Employment_Type.append(e[3])
            Job_Function.append(e[5])
            Industry.append(e[7])
        else:
            Seniority.append('-')
            Employment_Type.append('-')
            Job_Function.append('-')
            Industry.append('-')
    #if element does not exist
    else:
        Seniority.append('-')
        Employment_Type.append('-')
        Job_Function.append('-')
        Industry.append('-')
        
# make dictionary
data={}
data['Position']=Position
data['Company']=Company
data['Place']=Place
data['Pay']=Pay
data['Seniority']=Seniority
data['Employment_Type']=Employment_Type
data['Job_Function']=Job_Function
data['Industry']=Industry
data['Links']=Linklist

# convery dataframe to excel file
data=pd.DataFrame(data)
data.to_excel("datalinked.xlsx")

