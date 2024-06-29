import pandas as pd


def join_zillow_to_svi(zillow_path, svi_path, zip_to_county_path):
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
    return joined
