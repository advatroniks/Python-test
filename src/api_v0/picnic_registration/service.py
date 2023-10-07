from datetime import datetime

from fastapi import HTTPException, status


def check_actual_date(time: datetime):
    if datetime.now() > time:
        HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Picnic date is not actual, pls check date! "
        )

