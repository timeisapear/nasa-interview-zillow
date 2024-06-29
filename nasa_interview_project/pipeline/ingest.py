import requests
import pandas as pd
import os

ZILLOW_NEW_HOME_SALES_URL = "https://files.zillowstatic.com/research/public_csvs/new_con_sales_count_raw/Metro_new_con_sales_count_raw_uc_sfrcondo_month.csv"

def gather_zillow():
    new_home_sales = pd.read_csv(ZILLOW_NEW_HOME_SALES_URL)
    zillow_out = os.path.abspath(os.path.join(os.path.dirname(__file__), '../data/zillow_new_home.csv'))
    new_home_sales.to_csv(zillow_out)
    return zillow_out


def gather_cdc_svi():
    # This is hard-coded for now until the URL path is found
    pass
