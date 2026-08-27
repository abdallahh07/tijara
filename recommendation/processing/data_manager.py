import pandas as pd 
from config import settings

def load_user_events():
    path = settings["data"]["user_events_path"]
    data = pd.read_csv(path)
    return data

def load_products():
    path = settings["data"]["products_path"]
    data = pd.read_csv(path)
    return data