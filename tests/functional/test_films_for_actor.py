from http import HTTPStatus

from tests.utils.generate_request_data import generate_request_data


class TestFilmsForActor:
    async def test_get_films_for_actor(self, post_data):
        data = generate_request_data(
            intent_id='films_for_actor',
            slots={'name': 'Gosha'}
        )
        response = await post_data('/alice_api/v1/alice', data=data)
        assert response.status == HTTPStatus.OK
        ans_text = 'Фильмы в которых актер Gosha участвовал:\nFilm 1\nFilm 2'
        assert response.body['response']['text'] == ans_text
