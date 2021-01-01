"""
These are the URLs that will give you remote jobs for the word 'python'

https://stackoverflow.com/jobs?r=true&q=python
https://weworkremotely.com/remote-jobs/search?term=python
https://remoteok.io/remote-dev+python-jobs

Good luck!
"""
from save import save_job
from flask import Flask, render_template, request, redirect, send_file
from scrapper import get_stack_jobs, get_wework_jobs, get_remoteok_jobs
app = Flask("Jobs")
db={}

@app.route("/")
def home():
  return render_template("jobs.html")
@app.route("/search")
def search():
  term = request.args.get("term")
  if term:
    term = term.lower()
    total_jobs=[]
    fromDb = db.get(term)
    if fromDb:
      total_jobs = fromDb
    else:
      stack_jobs = get_stack_jobs(term)
      wework_jobs = get_wework_jobs(term)
      remote_jobs=get_remoteok_jobs(term)
      for job in stack_jobs:
        total_jobs.append(job)
      for job in wework_jobs:
        total_jobs.append(job)
      for job in remote_jobs:
        total_jobs.append(job)
      db[term]=total_jobs
  number = len(total_jobs)
  return render_template("detail.html", term=term, jobs=total_jobs, number=number)


@app.route("/export")
def export():
  try:
    term = request.args.get('term')
    if not term:
      raise Exception()
    term = term.lower()
    jobs = db.get(term)
    if not jobs:
      raise Exception()
    save_job(jobs, term)
    return send_file(f"{term}.csv", as_attachment= True)
  except:
    return redirect("/")
app.run(host="0.0.0.0")