import pandas as pd
from pipeline.helpers import make_file_path, MONTHS_COLUMNS, HSTARTS_COL_NAME
import numpy as np


def join_zillow_to_svi(
    zillow_path, svi_path, zip_to_county_path, save=False
) -> pd.DataFrame:
    # Gather crosswalk
    zip_to_county = pd.read_csv(zip_to_county_path)

    # Gather dataset tables
    zillow = pd.read_csv(zillow_path)  # join key MetroRegionID_Zillow
    svi = pd.read_csv(svi_path)  # join key FIPS

    # Join
    hydrated = pd.merge(
        zillow, zip_to_county, left_on="RegionID", right_on="MetroRegionID_Zillow"
    )
    joined = pd.merge(hydrated, svi, on="FIPS")  # FIPS = STCNTY
    if save:
        joined.to_csv(make_file_path("joined_zillow_svi.csv"))
    return joined
