from prefect import flow, task
from prefect.blocks.system import Secret
import requests

@task()
def get_api_key():
    secret_block = Secret.load("alphavantageapikey")
    api_key = secret_block.get()
    return api_key

@task()
def get_alphavantage_data(api_key):
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=IBM&interval=5min&apikey={api_key}'
    r = requests.get(url)
    data = r.json()
    return data

@flow
def alphavantage_data(name:str = "matt"):
    api_key = get_api_key()
    data = get_alphavantage_data(api_key)