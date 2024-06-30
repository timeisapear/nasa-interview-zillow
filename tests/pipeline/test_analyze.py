import pytest
import os
from nasa_interview_project.pipeline.analyze import join_zillow_to_svi

BASE_PATH = "nasa_interview_project/data/"


def make_file_path(filename):
    return os.path.join(BASE_PATH, filename)


# @pytest.mark.parametrize(["save", [True, False]])
def test_join_zillow_to_svi(save):
    joined = join_zillow_to_svi(
        zillow_path=make_file_path("zillow_new_home.csv"),
        svi_path=make_file_path("SVI_2022_US_county.csv"),
        zip_to_county_path=make_file_path("CountyCrossWalk_Zillow.csv"),
        save=save,
    )

    assert set(["RegionID", "MetroRegionID_Zillow", "FIPS"]).issubset(
        set(joined.columns)
    )
