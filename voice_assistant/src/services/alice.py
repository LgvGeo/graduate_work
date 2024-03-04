from typing import Literal

from fastapi import Depends

from services.api_handler import CinemaApi, get_cinema_api
from services.message_pattenrs import (FILM_DESCRIPTION_MESSAGE_PATTERN,
                                       FILMS_FOR_PERSON_PATTERN,
                                       NOT_FOUND_MESSAGE_PATTERN,
                                       ROLE_TRANSLATION)


class AliceService:

    def __init__(self, cinema_api):
        self.cinema_api: CinemaApi = cinema_api

    def parse_slots(self, intents, id_key):
        result = {}
        slots = intents[id_key]['slots']
        for slot_name, slot_description in slots.items():
            value = slot_description['value']
            result[slot_name] = value
        return result

    def process_intents(self, intents: dict):
        txt = None
        if 'film_description' in intents:
            slots = self.parse_slots(intents, 'film_description')
            film_name = slots['film']
            txt = self.get_film_by_name(film_name)
        elif 'best_films_by_rating_and_genre' in intents:
            slots = self.parse_slots(intents, 'best_films_by_rating_and_genre')
            genre = slots.get('genre')
            sort = '-imdb_rating'
            txt = self.get_films(genre, sort)
        elif 'worst_films_by_rating_and_genre' in intents:
            slots = self.parse_slots(
                intents, 'worst_films_by_rating_and_genre')
            genre = slots.get('genre')
            sort = 'imdb_rating'
            txt = self.get_films(genre, sort)
        elif 'films_for_actor' in intents:
            slots = self.parse_slots(intents, 'films_for_actor')
            name = slots.get('name')
            txt = self.get_films_for_person(name, 'actor')
        elif 'films_for_director' in intents:
            slots = self.parse_slots(intents, 'films_for_director')
            name = slots.get('name')
            txt = self.get_films_for_person(name, 'director')
        return txt

    def get_film_by_name(self, name):
        film = self.cinema_api.get_film_by_name(name)
        if not film:
            return NOT_FOUND_MESSAGE_PATTERN.format(object=f'фильм {name}')
        description = film.description or ''
        title = film.title
        return FILM_DESCRIPTION_MESSAGE_PATTERN.format(
            title=title, description=description)

    def get_films(
            self, genre: str | None,
            sort: Literal['imdb_rating', '-imdb_rating']
    ):
        films = self.cinema_api.get_films(genre, sort)
        if not films:
            suffix = 'фильмы'
            if genre:
                suffix += f' с жанром {genre}'
            return NOT_FOUND_MESSAGE_PATTERN.format(object=suffix)
        return '\n'.join(x.title for x in films)

    def get_films_for_person(self, name, role):
        person = self.cinema_api.get_person_by_name(name)
        if not person:
            return NOT_FOUND_MESSAGE_PATTERN.format(object=name)
        films = [x.title for x in person.films if role in x.roles]
        films = '\n'.join(films)
        return FILMS_FOR_PERSON_PATTERN.format(
            role=ROLE_TRANSLATION[role],
            name=person.name, films=films
        )


def get_alice_service(
    cinema_api: CinemaApi = Depends(get_cinema_api)
) -> AliceService:
    return AliceService(cinema_api)
