import requests
from bs4 import BeautifulSoup

URL = f"https://stackoverflow.com/jobs?q=python&sort=i"
headers = {"User-Agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.106 Safari/537.36"}
response = requests.get(URL,headers=headers)


def get_last_page():
    result= requests.get(URL)
    soup = BeautifulSoup(result.text, "html.parser")
    pages = soup.find("div", {"class":"s-pagination"}).find_all("a")
    last_page = pages[-2].get_text(strip=True)
    return int(last_page)

def extract_job(html):
    title= html.find("h2",{"class": "mb4"}).find("a")["title"]
    print(title)
    company, location = html.find("h3",{"class":"fc-black-700"}).find_all("span", recursive = False)
    company = company.get_text(strip=True)
    location = location.get_text(strip=True).strip("-").strip(" \r").strip("\n")
    job_id = html['data-jobid']
    return {"title" : title, "company" : company, "location" : location, "applyl-ink" : f"https://stackoverflow.com/jobs/{job_id}"}

def extract_jobs(last_page):
    jobs=[]
    for page in range(last_page):
        print(f"Scrapping SO: Page: {page}")
        result =requests.get(f"{URL}&pg={page+1}")
        soup = BeautifulSoup(result.text, "html.parser")
        results = soup.find_all("div", {"class":"-job"})
        for result in results:
            job = extract_job(result)
            jobs.append(job)
    return jobs



def get_jobs():
    last_page = get_last_page()
    jobs = extract_jobs(last_page)
    return jobs

