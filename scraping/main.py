import numpy as np
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys 
import json
import time

path = 'chromedriver.exe'

driver = webdriver.Chrome(path)
signinpage = 'https://www.linkedin.com/login?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin'

#account sign in
email = input('linkedin email: ')
password = input('linkedin password: ')

driver.get(signinpage)
time.sleep(1)
driver.find_element_by_id("username").send_keys(email)
driver.find_element_by_id("password").send_keys(password)
driver.find_element_by_id("password").send_keys(Keys.RETURN)
input("press enter if nothing happend with your account")

jobs_keyword = []
for _ in range(int(input("how many keywords: "))):
    jobs_keyword.append(input("Input job keyword: ").lower())
               
loc = input("location: ")
entity = []

for job in jobs_keyword:
    print("Job keyword on process:", job)
    pageJobSearch = 'https://www.linkedin.com/jobs/'
    driver.get(pageJobSearch)

    #input search keyword and location
    searchEngine = driver.find_elements_by_tag_name("input")

    searchEngine[1].send_keys(job)
    searchEngine[4].send_keys(loc)
    searchEngine[4].send_keys(Keys.RETURN)
    time.sleep(2)

    url = driver.current_url

    #maximal page in job
    while True:
        try:
            npages = int(driver.find_element_by_class_name("artdeco-pagination__pages.artdeco-pagination__pages--number").find_elements_by_tag_name("li")[-1].text)
            break
        except:
            pass
        
    for page in range(0, npages*25, 25):
        print("Page:",int(page/25),"of",npages)
        driver.get(url+"&start="+str(page))
        time.sleep(1)
        
        loop = 0 #looping for card list untill end
        while True: 
            try:
                card_list = driver.find_elements_by_class_name('.'.join("disabled ember-view job-card-container__link job-card-list__title".split()))
                current_card = card_list[loop]
                loop+=1
                current_card.click() 
                time.sleep(3)
                try:
                    #info in top_card: job title, company name, company location, posted date, views
                    top_card = driver.find_element_by_class_name("jobs-details-top-card__content-container").text.split('\n')
                    jobTitle = top_card[0]
                    for i in range(len(top_card)):
                        if "Company Name" == top_card[i]:
                            companyName = top_card[i+1]
                        elif "Posted Date" == top_card[i]:
                            postedDate = top_card[i+1]
                            break
                    numOfApplicants = driver.find_element_by_class_name("jobs-details-job-summary__text--ellipsis").text
                    companyInfo = driver.find_element_by_class_name("artdeco-list__item.jobs-details-job-summary__section.jobs-details-job-summary__section--center").text
                    sizeOfEmployee = np.nan if "employees" not in companyInfo else companyInfo.split('\n')[1]
                    jobDescDetail = driver.find_element_by_class_name("jobs-description-details.pt4").find_elements_by_tag_name("div")
                    dataHead = ["seniority level", "employment type", "job functions", "industry"]
                    dataHeadInDetail = [x.text.lower().split('\n')[0] for x in jobDescDetail]
                    for desc in jobDescDetail:
                        head = desc.text.lower().split('\n')[0]
                        if len(desc.find_elements_by_tag_name("li")) == 0:
                            value = desc.text.split('\n')[1]
                        else:
                            value = []
                            for x in desc.find_elements_by_tag_name("li"):
                                value.append(x.text)
                            value = value[0] if len(value) == 1 else value
                        if head == dataHead[0]:
                            seniorityLevel = value
                        elif head == dataHead[1]:
                            employmentType = value
                        elif head == dataHead[2]:
                            jobFunction = value
                        elif head == dataHead[3]:
                            companyIndustry = value 
                    headNotFound = list(set(dataHead)-set(dataHeadInDetail))
                    if len(headNotFound) > 0:
                        for head in headNotFound:
                            if head == dataHead[0]:
                                seniorityLevel = np.nan
                            elif head == dataHead[1]:
                                employmentType = np.nan 
                            elif head == dataHead[2]:
                                jobFunction = np.nan 
                            elif head == dataHead[3]:
                                companyIndustry = np.nan
                    detailDescription = driver.find_element_by_id("job-details").find_element_by_tag_name("span").text

                    entity.append([jobTitle,
                                   companyName,
                                   postedDate,
                                   numOfApplicants,
                                   sizeOfEmployee,
                                   seniorityLevel,
                                   employmentType,
                                   jobFunction,
                                   companyIndustry,
                                   detailDescription])
                except:
                    pass
            except:
                break

df = pd.DataFrame(entity, columns = ['jobTitle','companyName','postedDate','numOfApplicants','sizeOfEmployee','seniorityLevel','employmentType','jobFunction','companyIndustry','detailDescription'])
df = df.loc[df.astype(str).drop_duplicates().index]
df.reset_index(drop = True, inplace = True)
df_idx = pd.DataFrame(range(len(df)), columns = ['Id'])
df = pd.concat([df_idx, df], axis = 1)
df.drop("detailDescription", axis = 1).to_csv("data_output.csv", index = False)
df.drop("detailDescription", axis = 1).to_excel("data_output.xlsx", index = False)
df[['Id', 'detailDescription']].to_json("data_output.json")
