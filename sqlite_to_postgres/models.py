import uuid
from datetime import datetime
from typing import Optional

import dateutil.parser
from pydantic import (AliasChoices, BaseModel, ConfigDict, Field,
                      field_validator)


class CustomBaseModel(BaseModel):
    id: uuid.UUID

    @field_validator(
            'created', 'modified',
            'creation_date',
            mode='before', check_fields=False)
    @classmethod
    def str2datetime(cls, date) -> datetime:
        if date is None:
            return date
        return dateutil.parser.isoparse(str(date))


class CreatedModifiedMixin(BaseModel):
    created: Optional[datetime] = Field(
        validation_alias=AliasChoices('created_at', 'created')
    )
    modified: Optional[datetime] = Field(
        validation_alias=AliasChoices('updated_at', 'modified')
    )


class FilmWork(CustomBaseModel, CreatedModifiedMixin):
    model_config = ConfigDict(title='film_work')

    title: str
    description: Optional[str]
    creation_date: Optional[datetime]
    rating: Optional[float]
    type: str


class Person(CustomBaseModel, CreatedModifiedMixin):
    model_config = ConfigDict(title='person')

    full_name: str


class Genre(CustomBaseModel, CreatedModifiedMixin):
    model_config = ConfigDict(title='genre')

    name: str
    description: Optional[str]


class GenreFilmWork(CustomBaseModel):
    model_config = ConfigDict(title='genre_film_work')

    genre_id: uuid.UUID
    film_work_id: uuid.UUID
    created: Optional[datetime] = Field(
        validation_alias=AliasChoices('created_at')
    )


class PersonFilmWork(CustomBaseModel):
    model_config = ConfigDict(title='person_film_work')

    person_id: uuid.UUID
    film_work_id: uuid.UUID
    role: str
    created: Optional[datetime] = Field(
        validation_alias=AliasChoices('created_at')
    )
