import pandas as pd
import os
import requests
    


def join_zillow_to_svi(zillow_path, svi_path):
    zillow = pd.read_csv(zillow_path)
    svi = pd.read_csv(svi_path)
    zillow.join(how="inner", on)
    return 