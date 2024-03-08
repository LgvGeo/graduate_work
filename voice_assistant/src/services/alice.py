from typing import Literal

from fastapi import Depends

from services.api_handler import CinemaApi, get_cinema_api
from services.message_pattenrs import (FILM_DESCRIPTION_MESSAGE_PATTERN,
                                       FILMS_FOR_PERSON_PATTERN, HELLO_MESSAGE,
                                       NOT_FOUND_MESSAGE_PATTERN,
                                       ROLE_TRANSLATION, UNKNOWN_ANSWER)


class AliceService:

    def __init__(self, cinema_api):
        self.cinema_api: CinemaApi = cinema_api

    handlers = {
        'film_description': (
            ('film',), (None,),
            'get_film_by_name'
        ),
        'best_films_by_rating_and_genre': (
            ('genre', 'sort'), (None, '-imdb_rating'),
            'get_films'
        ),
        'worst_films_by_rating_and_genre': (
            ('genre', 'sort'), (None, 'imdb_rating'),
            'get_films'
        ),
        'films_for_actor': (
            ('name', 'role'), (None, 'actor'),
            'get_films_for_person'
        ),
        'films_for_director': (
            ('name', 'role'), (None, 'director'),
            'get_films_for_person'
        ),
    }

    def process_request(self, request):
        if self.is_new_session(request):
            return HELLO_MESSAGE
        intents = self.parse_intents(request)
        if not intents:
            return UNKNOWN_ANSWER
        txt = self.process_intents(intents)
        return txt

    def parse_intents(self, request):
        intents = request.get('request', {}).get('nlu', {}).get('intents', {})
        return intents

    def is_new_session(self, request):
        return request['session']['new'] is True

    def parse_slots(self, intents, id_key):
        result = {}
        slots = intents[id_key]['slots']
        for slot_name, slot_description in slots.items():
            value = slot_description['value']
            result[slot_name] = value
        return result

    def _process_intent(
            self,
            intents: dict,
            intent_name: str,
            slot_names: list[str],
            default_values: list,
            callback_func_name
    ):
        slots = self.parse_slots(intents, intent_name)
        values = []
        for i, key in enumerate(slot_names):
            default = default_values[i]
            value = slots.get(key, default)
            values.append(value)
        return getattr(self, callback_func_name)(*values)

    def process_intents(self, intents: dict):
        intent_name = list(intents.keys())[0]
        if intent_name not in self.handlers:
            return UNKNOWN_ANSWER
        return self._process_intent(
            intents, intent_name,
            *self.handlers[intent_name]
        )

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
