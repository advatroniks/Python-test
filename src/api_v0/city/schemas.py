import uuid

from pydantic import BaseModel, Field, computed_field

from src.api_v0.city.weather.weather_get import get_weather


class BaseCity(BaseModel):
    name: str = Field(..., max_length=20)


class CreateCity(BaseCity):
    @computed_field                 # Метод computed_field(с pydantic v2), работает как @property
    def weather(self) -> str:
        return get_weather(self.name)


class ResponseCity(BaseCity):
    weather: str

