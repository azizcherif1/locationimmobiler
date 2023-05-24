"""from bs4 import BeautifulSoup
import requests
html_text=requests.get('https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&from=submit&txtKeywords=python&txtLocation=').text
soup=BeautifulSoup(html_text,'lxml')
jobs=soup.find_all('li',class_='clearfix job-bx wht-shd-bx')
for job in jobs:
   company_name=job.find('h3',class_='joblist-comp-name').text.replace(' ','')
#skills=jobs.find('ul',class_='list-job-dtl clearfix')
   print(company_name)
   job_skills_list = job.find_all('strong', class_= 'blkclor')
   for skill in job_skills_list:
       print(skill.text)
   work_from_home_elem = job.find('span', {'class': 'jobs-status covid-icon clearfix'})
   posted_elem = work_from_home_elem.find_next_sibling('span')
   posted_text = posted_elem.text.strip()
   print(posted_text)    
"""


from bs4 import BeautifulSoup
import requests

html_text = requests.get('https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&from=submit&txtKeywords=python&txtLocation=').text
soup = BeautifulSoup(html_text, 'lxml')
jobs = soup.find_all('li', class_='clearfix job-bx wht-shd-bx')

for job in jobs:
    company_name = job.find('h3', class_='joblist-comp-name').text.replace(' ', '')
    job_skills_list = job.find_all('strong', class_='blkclor')
    print(company_name)
    for skill in job_skills_list:
        print(skill.text)
    posted_elem = job.find('span', class_='sim-posted')
    posted_text = posted_elem.text.strip() if posted_elem else 'Date not available'
    print(posted_text)










"""import requests

html_text=requests.get('https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&from=submit&txtKeywords=python&txtLocation=').text
soup=BeautifulSoup(html_text,'lxml')
jobs=soup.find('li',class_='clearfix job-bx wht-shd-bx')
company_name=jobs.find('h3',class_='joblist-comp-name').text.replace(' ','')
skills=jobs.find('span',class_='srp-skills').text.replace(' ','')
date=jobs.find('span',class_='sim-posted').find('span',class_='jobs-status covid-icon clearfix').find('span').text
#print(f'the job at {company_name} requires these skills : {skills}')
print(date)"""