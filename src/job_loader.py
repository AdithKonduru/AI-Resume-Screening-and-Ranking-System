import pandas as pd

def load_jobs(csv_path):
    jobs = pd.read_csv(csv_path)
    return jobs