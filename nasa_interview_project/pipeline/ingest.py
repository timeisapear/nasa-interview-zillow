import requests
import pandas as pd
import os
from requests.exceptions import RequestException
import traceback

ZILLOW_NEW_HOME_SALES_URL = "https://files.zillowstatic.com/research/public_csvs/new_con_sales_count_raw/Metro_new_con_sales_count_raw_uc_sfrcondo_month.csv"
ZILLOW_FILE_NAME = "zillow_new_home.csv"
ZIP_TO_COUNTY_FILE_NAME = "zip_to_county.csv"
HUD_TOKEN = os.getenv("HUD_TOKEN")
HUD_BASE_URL = "https://www.huduser.gov/hudapi/public/usps"
ZILLOW_CROSSWALK = "http://files.zillowstatic.com/research/public/CountyCrossWalk_Zillow.csv"  # filepath found in https://commercedataservice.github.io/tutorial_zillow_acs/


def gather_zillow():
    new_home_sales = pd.read_csv(ZILLOW_NEW_HOME_SALES_URL)
    zillow_out = os.path.abspath(
        os.path.join(os.path.dirname(__file__), f"../data/{ZILLOW_FILE_NAME}")
    )
    new_home_sales.to_csv(zillow_out)
    return zillow_out


def gather_cdc_svi():
    # This is hard-coded for now until the URL path is found (had to click button, could use Selenium etc. if no other option)
    pass


def gather_zillow_county_crosswalk():
    crosswalk_county_metro = pd.read_csv(ZILLOW_CROSSWALK, encoding="us-ascii", encoding_errors="replace")
    crosswalk_out = os.path.abspath(
        os.path.join(os.path.dirname(__file__), f"../data/{ZILLOW_CROSSWALK.split("/")[-1]}")
    )
    crosswalk_county_metro.to_csv(crosswalk_out)
    return crosswalk_out


def construct_zip_to_county_crosswalk() -> str:
    params = {
        "type": "2",  # zip-county, 7 county to zip from https://www.huduser.gov/portal/dataset/uspszip-api.html
        "query": "All",
    }

    headers = {"Authorization": f"Bearer {HUD_TOKEN}"}
    try:
        resp = requests.get(HUD_BASE_URL, headers=headers, params=params)
        zip_to_county_path = os.path.abspath(
            os.path.join(
                os.path.dirname(__file__), f"../data/{ZIP_TO_COUNTY_FILE_NAME}"
            )
        )
        pd.DataFrame(resp.json()["data"]["results"]).to_csv(zip_to_county_path)
        return zip_to_county_path
    except RequestException as e:
        print(traceback.format_exc(e))

if __name__ == "__main__":
    print("Running ingest...")
    zillow_path = gather_zillow()
    # The Zillow-native crosswalk was found to be a better resource than using the HUD crosswalk
    crosswalk_path = gather_zillow_county_crosswalk()
    print("Ingest complete!")
