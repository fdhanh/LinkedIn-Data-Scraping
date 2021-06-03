# LinkedIn Data Scraping and Short Analytics

## Data Scraping

This repository is intended to share my script for pulling data from LinkedIn job portal.
From my experience for a couple of days since I pull data from that web page I have so many tricky problems which is different view if you have login and not log in.
This scraping script will pull the data such as:
1. Job Title
2. Company Name
3. Posted Date
4. Number of Applicants
5. Size of Employee
6. Seniority Level
7. Employment Type
8. Job Function
9. Detail Description*

For detail description will be in different output file. 

### Installation

Use git to clone this repository `https://github.com/fdhanh/LinkedIn-Data-Scraping.git`

### Prerequisite

Make sure you have python 3.6 installed on your machine <br>
`python --version`

To run the script in this repository, you need to install the prerequisite library from requirements.txt <br>
`pip install -r requirements.txt`

You need to download and put Selenium webdriver app for Chrome in the same folder with script file. Download it <a href="https://chromedriver.chromium.org/downloads"> here </a> and dont forget to fit your Chrome version.

### Usage
Run `scraping/main.py`

## Data Visualization

![alt text](https://github.com/fdhanh/LinkedIn_Data_Scraping/blob/main/added_file/DASHBOARD.jpeg?raw=true)
For best experience for interactive dashboard you can go to <a href="https://public.tableau.com/views/LinkedInDataVisualization/Dashboard1?:language=en-GB&:display_count=y&:origin=viz_share_link">my tableau dashboard</a>
