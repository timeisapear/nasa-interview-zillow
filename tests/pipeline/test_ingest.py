import pytest 
import pandas as pd

from nasa_interview_project.pipeline.ingest import gather_zillow, construct_zip_to_county_crosswalk

def test_run_zillow():
    zillow_path = gather_zillow()
    assert len(pd.read_csv(zillow_path)) > 0

def test_download_zip_to_county_crosswalk():
    crosswalk_path = construct_zip_to_county_crosswalk()
    assert len(pd.read_csv(crosswalk_path)) > 0
