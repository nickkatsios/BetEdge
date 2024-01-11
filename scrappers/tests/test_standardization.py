import pytest
import datetime
from standardizers.date_standardizer import Date_standardizer

@pytest.fixture(scope="module")
def date_standardizer():
    return Date_standardizer()
    
def test_standardize_date(date_standardizer):
    datestr = "Sunday, 20 August 2023 22:00"
    bookmaker = "stoiximan"
    result = date_standardizer.standardize_date(datestr, bookmaker)
    assert result == datetime.datetime(2023, 8, 20, 22, 0)