from typing import Annotated

from fastapi import Query, HTTPException, status


def validate_age_for_add(
        age: Annotated[
            int, Query(
                ...,
                title="Check age",
                description="Age can t exceed 100 years and age can t less 0"
                )
        ]
):
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

