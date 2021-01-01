import requests
from bs4 import BeautifulSoup

headers = {
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'en-US,en;q=0.8',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
}

def get_pagination(term):
  url= f"https://stackoverflow.com/jobs?q={term}&r=true"
  r = requests.get(url, headers=headers)
  soup = BeautifulSoup(r.text, "html.parser")
  p_soup = soup.find_all("a",{"class":"s-pagination--item"})
  pages=[]
  for page in p_soup:
    a_page = page.find("span").string
    pages.append(a_page)
  return pages
pages=get_pagination("python")

def get_stack_jobs(term):
  pages = get_pagination(term)
  stack_jobs=[]
  for page in pages[:-1]:
    url=f"https://stackoverflow.com/jobs?r=true&q={term}&pg={page}"
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, "html.parser")
    jobs = soup.find_all("div",{"class":"fl1"})
    for job in jobs[2:]:
      each_job={}
      link = job.find("a")['href']
      title = job.find("h2").text
      company = job.find("h3").find("span").text
      each_job['link']=f"https://stackoverflow.com/{link}"
      each_job['title']=title
      each_job['company']=company
      stack_jobs.append(each_job)
  return stack_jobs

def get_wework_jobs(term):
  url=f"https://weworkremotely.com/remote-jobs/search?term={term}"
  r= requests.get(url)
  soup = BeautifulSoup(r.text, "html.parser")
  article = soup.find("article")
  lists = article.find_all("li")
  wework_jobs=[]
  for job in lists[:-1]:
    each_job={}
    links = job.find_all("a")
    if len(links) == 1:
      link = f"https://weworkremotely.com{links[0]['href']}"
      each_job['link']=link
    else:
      link = f"https://weworkremotely.com{links[1]['href']}"
      each_job['link']=link
    title = job.find("span",{"class":"title"}).text
    company = job.find("span",{"class":"company"}).text
    each_job['title'] = title
    each_job['company'] = company
    wework_jobs.append(each_job)
  return wework_jobs 
def get_remoteok_jobs(term):
  url=f"https://remoteok.io/remote-dev+{term}-jobs"
  r = requests.get(url, headers=headers)
  soup = BeautifulSoup(r.text, "html.parser")
  table = soup.find("table", {"id":"jobsboard"})
  tds = table.find_all("td",{"class":"company position company_and_position_mobile"})
  remote_jobs=[]
  for td in tds[1:]:
    each_job={}
    try:
      total_a = td.find_all("a",{"class":"preventLink"})
      link=f"https://remoteok.io{total_a[0]['href']}"
      each_job['link']=link
      title = total_a[0].string
      if not title:
        title="No exist"
        each_job['title']=title
      else:
        each_job['title']=title
      company = total_a[1].string
      if not company:
        company="No exist"
        each_job['company']=company
      else:
        each_job['company']=company
      each_job['link']=link
      remote_jobs.append(each_job)
    except:
      print("can't load the page")
  return remote_jobs

  
