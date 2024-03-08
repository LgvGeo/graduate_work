from http import HTTPStatus

from tests.utils.generate_request_data import generate_request_data


class TestGettingFilmsWithDescription:
    async def test_worst_flims_without_genre(self, post_data):
        data = generate_request_data(
            intent_id='worst_films_by_rating_and_genre'
        )
        response = await post_data('/alice_api/v1/alice', data=data)
        assert response.status == HTTPStatus.OK
        ans_text = 'The Star 0\nThe Star 1\nThe Star 2\nZmurki'
        assert response.body['response']['text'] == ans_text

    async def test_worst_flims_with_genre(self, post_data):
        data = generate_request_data(
            intent_id='worst_films_by_rating_and_genre',
            slots={'genre': 'Action'}
        )
        response = await post_data('/alice_api/v1/alice', data=data)
        assert response.status == HTTPStatus.OK
        ans_text = 'The Star 0\nThe Star 1\nThe Star 2'
        assert response.body['response']['text'] == ans_text
