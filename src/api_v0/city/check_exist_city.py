from requests import Session, Response

from src.api_v0.city.dependences import get_weather_url


def check_existing_city(
        city: str
) -> Response | bool:
    """
    Функция проверяет есть ли город на стороне API OpenWeather.
    Создается сессия, делается запрос, при 200 >> ответ от API.
    Если же код отличный от 200, возвращается False.
    :param city:
    :return: Response | False
    """
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


