from datetime import datetime

from fastapi import HTTPException, status


def check_actual_date(time: datetime):
    """
    Функция для проверки актуальности даты. Если дата старше чем сегодня,
    то exception.
    :param time: Datetime, время для проверки
    :raises HTTPException: 400 если время в параметре функции в прошлом.
    :returns: None
    """
    if datetime.now() > time:
        HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Picnic date is not actual, pls check date! "
        )

