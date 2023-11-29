
from app.weather_app import query_postal_code
import pandas as pd

def test_query_postal_code():
    result = query_postal_code("10001")
    assert isinstance(result, pd.Series), "The result should be a pandas Series"
    assert "latitude" in result and "longitude" in result, "The result should have latitude and longitude keys"
    assert result["latitude"] is not None and result["longitude"] is not None, "Latitude and longitude should not be None"
    