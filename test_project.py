from project import *

def test_read_api_key():
    assert len(read_api_key()) > 0

def test_apod_response():
    assert apod_response() >= 0

def test_mars_pictures_response():
    assert mars_pictures_response() >= 0

def test_earth_image_response():
    assert earth_image_response() >= 0
