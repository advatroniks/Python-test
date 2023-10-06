from requests import Session

from src.api_v0.city.dependences import get_weather_url

WEATHER_API_KEY = '47bb7070504db821c960ddf739c5f340'


def check_existing_city(
        city: str
):
    session = Session()

    url = get_weather_url(city)
    print("before")
    response = session.get(url=url)
    print(response)
    if response.status_code == 200:
        return response
    else:
        print(f"Some error with code {response.status_code}")
        return False


