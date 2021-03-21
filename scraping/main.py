import numpy as np
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys 
import json
import time

homepage = 'https://www.linkedin.com/jobs?trk=homepage-basic_directory_jobsHomeUrl'
path = 'chromedriver.exe'

driver = webdriver.Chrome(path)

jobs_keyword = ['data engineer', 'data scientist', 'data analyst', 'business intelligence']
loc = 'indonesia'
email = input('linkedin email: ')
password = input('linkedin password: ')

companyLink = {}
jobTitle = []
detailDescription = []
companyName = []
jobPostingTime = []
numberOfApplicants = []
seniorityLevel = []
sizeOfEmployee = []
companyIndustry = []
employmentType = []
jobFunction = []

for job in range(len(jobs_keyword)):
    driver.get(homepage)
    driver.find_element_by_xpath('//*[@id="JOBS"]/section[2]/button').click()
    search = driver.find_element_by_id('JOBS').find_elements_by_class_name('dismissable-input__input')
    search[0].send_keys(jobs_keyword[job])
    search[1].send_keys(loc)
    search[1].send_keys(Keys.RETURN)

    #scroll the page from search keyword values
    loop = 0
    limit = 50
    while loop < limit:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        try:
            driver.find_element_by_xpath('//*[@id="main-content"]/div/section[2]/button').click()
            loop+=1
        except:
           pass

    card_list = driver.find_elements_by_class_name("result-card.job-result-card.result-card--with-hover-state")
    links = [link.find_element_by_tag_name("a").get_attribute("href") for link in card_list]
    
    for link_idx in range(len(links)):
        try:
            driver.get(links[link_idx])
            time.sleep(0.8) #time to load page estimation
            
            topcard_section = driver.find_element_by_class_name("topcard") 
            job_title = topcard_section.find_element_by_class_name("topcard__title").text
            jobTitle.append(job_title)
            company = driver.find_element_by_class_name("topcard__flavor")
            companyName.append(company.text)
            
            jobPostingTime.append(driver.find_element_by_class_name("topcard__flavor--metadata.posted-time-ago__text").text)
            numberOfApplicants.append(driver.find_element_by_class_name("num-applicants__caption").text)

            criteria = driver.find_elements_by_class_name("job-criteria__item")
            criteria_head = ["Seniority level", "Industries", "Employment type", "Job function"]
            criteria_list = []
            for value in criteria:
                key = value.find_element_by_tag_name("h3").text
                criteria_list.append(key)
                values = value.find_elements_by_tag_name("span")
                if len(values) == 1:
                    value = values[0].text
                else:
                    value = []
                    for i in values:
                        value.append(i.text)
                
                if key == criteria_head[0]:
                    seniorityLevel.append(value)
                elif key == criteria_head[1]:
                    companyIndustry.append(value)
                elif key == criteria_head[2]:
                    employmentType.append(value)
                elif key == criteria_head[3]:
                    jobFunction.append(value)
                    
            criteria_not_exist = list(set(criteria_head)-set(criteria_list))
            for x in criteria_not_exist:
                if x == criteria_head[0]:
                    seniorityLevel.append(np.nan)
                elif x == criteria_head[1]:
                    companyIndustry.append(np.nan)
                elif x == criteria_head[2]:
                    employmentType.append(np.nan)
                elif x == criteria_head[3]:
                    jobFunction.append(np.nan)
            try:
                driver.find_element_by_xpath("//*[contains(text(), 'Show more')]").click()
            except:
                pass

            detailDescription.append(driver.find_element_by_class_name("show-more-less-html__markup").text)
            ##
            try:
                company_link = company.find_element_by_tag_name('a').get_attribute('href')
                companyLink[company.text] = company_link
            except:
                pass
            time.sleep(1) 
        except:
            pass

signinpage = 'https://www.linkedin.com/login?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin'
#account sign in
driver.get(signinpage)

driver.find_element_by_id("email").send_keys(username)
driver.find_element_by_id("password").send_keys(password)
driver.find_element_by_id("password").send_keys(Keys.RETURN)
time.sleep(2)

## sizeofemployee data pulling from company link
sizeOfEmployee = []
for compName in companyLink:
    driver.get(companyLink[compName])
    loop = False
    while loop == False:
        try:
            driver.find_elements_by_class_name("org-page-navigation__item.m0")[1].click()
            loop = True
        except:
            pass
    loop = False
    while loop == False:
        try:
            text = driver.find_element_by_class_name("overflow-hidden").text.split('\n')
            loop = True
        except:
            pass
    for i in range(len(text)):
        if 'Company size' in text[i]:
            compsize = text[i+1] 
            break
    sizeOfEmployee.append([compName, compsize])
        
data_output = {
        'jobTitle': jobTitle,
	'companyName': companyName,
	'jobPostingTime': jobPostingTime,
	'numberOfApplicants': numberOfApplicants,
	'seniorityLevel': seniorityLevel, 
        'companyIndustry': companyIndustry,
        'employmentType': employmentType,
        'jobFunction': jobFunction,
        'detailDescription': detailDescription
        }

df = pd.DataFrame(data_output)
dfSizeofEmployee = pd.DataFrame(sizeOfEmployee, columns = ['companyName', 'sizeOfEmployee'])
df = df.join(dfSizeofEmployee.set_index('companyName'), on='companyName')
df.drop_duplicates(inplace = True)
df.drop('detailDescription', axis = 1).to_csv('output_file.csv')
df['detailDescription'].to_json('output_detail.json')


