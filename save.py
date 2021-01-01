import csv

def save_job(jobs, term):
  file = open(f"{term}.csv", mode="w")
  writer = csv.writer(file)
  writer.writerow(["link","title","company"])
  for job in jobs:
    writer.writerow(list(job.values()))
  return