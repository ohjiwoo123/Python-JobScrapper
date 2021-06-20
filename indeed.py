import requests
from bs4 import BeautifulSoup

LIMIT = 50
URL = f"https://www.indeed.com/jobs?q=python&limit={LIMIT}"

def extract_pages():
    start = 0
# start_int_list = [0]
    result = requests.get(URL)

    soup = BeautifulSoup(result.text, 'html.parser')

    next_button = soup.find("a", {"aria-label":"Next"})

    while next_button:
        indeed_url_updated = f"https://www.indeed.com/jobs?q=python&limit=50&start={str(start*50)}"
        result_updated = requests.get(indeed_url_updated)
        soup_upadted = BeautifulSoup(result_updated.text, 'html.parser')
        next_button = soup_upadted.find("a", {"aria-label":"Next"})
        if next_button == None:
            break
        start = int(start) + 1
# start_int_list.append(start)
# print(f"start_int_list:{start_int_list}")

    return int(start) + 1


# html = soup object 
def extract_job(html):
    title = html.find("h2",{"class":"title"}).find("a")["title"]
    company = html.find("span",{"class":"company"})
    if company :
        company_anchor = company.find("a")
        if company_anchor is not None:
            company = str(company_anchor.string)
        else:
            company = str(company.string)
    else:
        company = None 
    company = company.strip()
    location = html.find("div",{"class":"recJobLoc"})["data-rc-loc"]
    job_id = html["data-jk"]
    return {'title': title, 'company': company, 'location':location, "link": f"https://www.indeed.com/viewjob?jk={job_id}"} 



def extract_jobs(last_page):
    jobs = []
    for page in range(last_page):
        print(f"Scrapping Indeed Page {page}")
        result = requests.get(f"{URL}&start={page*LIMIT}")
        soup = BeautifulSoup(result.text, "html.parser")
        results = soup.find_all("div",{"class":"jobsearch-SerpJobCard"})
    for result in results:
        job = extract_job(result)
        jobs.append(job)
    return jobs 

def get_jobs():

    last_page = extract_pages()

    jobs = extract_jobs(last_page)
    
    return jobs
