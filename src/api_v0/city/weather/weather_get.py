from fastapi import HTTPException, status

from src.api_v0.city.check_exist_city import check_existing_city
from src.api_v0.city.dependences import get_current_temperature


def get_weather(city: str) -> str:
    """
    Функция принимает город(str) и возвращает погоду в этом городе
    на данный момент.
    :param city:
    :return: Current temperature(str) | raise Exception(404)
    """
    city_response = check_existing_city(city)
    if city_response.status_code == 200:
        return get_current_temperature(city_response)
    else:
        HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Can't find city! Try again"
        )
