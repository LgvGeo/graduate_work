from http import HTTPStatus
from typing import Literal

import requests

from models.response_models.film import MovieResponse, MoviesListResponse
from models.response_models.genre import GenreListResponse
from models.response_models.person import PersonResponse
from settings.config import CommonSettings


class APIHandlerBase:

    def __init__(self, api_url):
        self.url = api_url
        self.session = requests.Session()
        self.headers = {'Content-type': 'application/json',
                        'Accept': 'application/json'}

    def get(self, entrypoint, params=None):
        r = self.session.get(
            f'{self.url}{entrypoint}',
            params=params,
            headers=self.headers,
            verify=False
        )
        if r.status_code == HTTPStatus.OK:
            return r.json()

    def close(self):
        return self.session.close()


class CinemaApi(APIHandlerBase):

    def __init__(self, base_url):
        super().__init__(base_url)

    def get_film_by_name(self, name) -> MovieResponse | None:
        content = self.get(f'/films/search?query={name}')
        if not content:
            return
        film_id = content[0]['id']
        content = self.get(f'/films/{film_id}')
        return MovieResponse(**content)

    def get_genres(self):
        content = self.get('/genres')
        if not content:
            return
        return [GenreListResponse(**x) for x in content]

    def get_genre_id_by_name(self, name: str):
        if not name:
            return
        genres = self.get_genres()
        for genre in genres:
            if genre.name.upper() == name.upper():
                return genre.id

    def get_films(
            self, genre_name: str | None,
            sort: Literal['imdb_rating', '-imdb_rating']
    ) -> list[MoviesListResponse] | None:
        params = {}
        genre = self.get_genre_id_by_name(genre_name)
        if sort:
            params['sort'] = sort
        if genre:
            params['genre'] = genre
        content = self.get('/films', params=params)
        if not content:
            return
        films = [MoviesListResponse(**x) for x in content]
        return films

    def get_person_by_name(self, name: str):
        content = self.get(f'/persons/search?name={name}')
        if not content:
            return
        person_id = content[0]['id']
        for res in content:
            if res['name'].upper() == name.upper():
                person_id = res['id']
        content = self.get(f'/persons/{person_id}')
        return PersonResponse(**content)


def get_cinema_api():
    config = CommonSettings()
    return CinemaApi(config.cinema_api_url)
