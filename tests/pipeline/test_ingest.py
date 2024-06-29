import pytest 
import pandas as pd

from nasa_interview_project.pipeline.ingest import gather_zillow

def test_run_zillow():
    zillow_path = gather_zillow()
    assert len(pd.read_csv(zillow_path)) > 0
