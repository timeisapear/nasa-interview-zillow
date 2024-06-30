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

    # hydrate
    hydrated_df = hydrate_zillow_svi_data(joined)
    if save:
        hydrated_df.to_csv(make_file_path("joined_zillow_svi.csv"))
    return hydrated_df


def hydrate_zillow_svi_data(joined_data_source):
    # Add a new column All that is the sum of all the known months so far
    joined_data_source[MONTHS_COLUMNS[0]] = joined_data_source[MONTHS_COLUMNS[1:]].sum(
        axis=1
    )
    return joined_data_source


# This is a live function imported and executed by the Holoviz dashboard
def filter_data_on_dashboard(date_window, source_data):
    group_by_column = "RegionName"

    data = (
        source_data.loc[
            :, [group_by_column, "RPL_THEMES", "E_HU", date_window]
        ]  # E_HU is estimated housing units, M_HU is Margin of Error
        .groupby(group_by_column)
        .apply(
            lambda group: pd.Series(
                {
                    "SVI_INDEX": custom_mean(group["RPL_THEMES"]),
                    HSTARTS_COL_NAME: custom_aggregation(group, date_window),
                }
            )
        )
    )
    # Ensure GroupColumn is set as the index
    # data.index.name = group_by_column
    return data


def custom_mean(x):
    return np.mean(x)


def custom_aggregation(group, date_window):
    return np.sum(group[date_window] / group["E_HU"])


if __name__ == "__main__":
    print("Starting analyze/transform...")
    join_zillow_to_svi(
        zillow_path=make_file_path("zillow_new_home.csv"),
        svi_path=make_file_path("SVI_2022_US_county.csv"),
        zip_to_county_path=make_file_path("CountyCrossWalk_Zillow.csv"),
        save=True,
    )
    print("Analyze/transform complete!")
