
from prefect import flow,task
from prefect.task_runners import SequentialTaskRunner
import requests


@task()
def extract(table_name):
    r = requests.get(f'https://cloudprovider.com/db/{table_name}/')
    return r

@task()
def transform(table):
    table = "table_but_transformed"
    return table

@task()
def load(table):
    r = requests.post(f'https://cloudprovider.com/db/{table}/')
    return r.status_code


@flow(name="ETL")
def flow():
    table = extract("Prefect")
    transformed = transformed(table)
    loaded = load(transformed)
    
    



