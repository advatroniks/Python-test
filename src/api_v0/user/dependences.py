from typing import Annotated

from fastapi import Query, HTTPException, status


def validate_age_for_add(age: int):
    """
    Функция для проверки возраста при создании пользователя.
    :param age: Int,
    :returns: age, если удовлетворяет условиям.
    :raises HTTPException: 400 BAD REQUEST, если возраст не в рамках 0 < age < 100
    """
    if 0 < age < 100:
        return age
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Check age!! And try again!"
    )


def validate_age_parameter(
        min_age: Annotated[int, Query()] | None = None,
        max_age: Annotated[int, Query()] | None = None
) -> dict[str, int] | None:
    """
    Функция для указания проверки параметров в запросе на выборку по
    возрасту юзеров.
    :param min_age: Параметр минимального возраста из запроса Query
    :param max_age: Параметр максимального возраста из запроса Query.
    :returns: Словарь с минимальным и максимальным возрастом(в рамках 0 < age < 100).
    :raises HTTPException: Если возраст не входит 0 < age < 100.
    """
    for age in (min_age, max_age):
        if age is not None:
            if not 0 <= age <= 100:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Check age!! And try again!"
                )
    result = {
        "min_age": min_age,
        "max_age": max_age
    }

    return result
