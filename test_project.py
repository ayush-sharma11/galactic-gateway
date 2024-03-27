from project import read_api_key, apod, search
import requests

def read_api_key():
    with open("api_key.txt", "r") as file:
        api_key = file.read().strip()
    return api_key

API_KEY = read_api_key()

def test_read_api_key():
    # Assuming api_key.txt contains a valid API key
    assert read_api_key() != ""

def test_apod():
    # Assuming API_KEY is valid
    response = requests.get(f"https://api.nasa.gov/planetary/apod?api_key={API_KEY}")
    assert response.status_code == 200
    assert apod() is None

def test_search():
    # Assuming API_KEY is valid
    response = requests.get(f"https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos?api_key={API_KEY}")
    assert response.status_code == 200
    assert search() is None
