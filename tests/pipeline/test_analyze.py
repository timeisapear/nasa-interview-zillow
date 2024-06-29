from nasa_interview_project.pipeline.analyze import join_zillow_to_svi
import pytest
import os

BASE_PATH = "nasa_interview_project/data/"


def make_file_path(filename):
    return os.path.join(BASE_PATH, filename)


def test_join_zillow_to_svi():
    status = join_zillow_to_svi(
        zillow_path=make_file_path("zillow_new_home.csv"),
        svi_path=make_file_path("SVI_2022_US_county.csv"),
        zip_to_county_path=make_file_path("zip_to_county.csv"),
    )

    assert status == "success"
