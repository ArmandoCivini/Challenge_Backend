import requests


API_URL = "https://restcountries.com/v3.1/all"


def get_data(url):
    response = requests.get(url)
    return response.json()


def get_countries_data():
    return get_data(API_URL)
