from http import HTTPStatus

from tests.utils.generate_request_data import generate_request_data


class TestGettingFilmsWithDescription:
    async def test_best_flims_without_genre(self, post_data):
        data = generate_request_data(
            intent_id='best_films_by_rating_and_genre'
        )
        response = await post_data('/alice_api/v1/alice', data=data)
        assert response.status == HTTPStatus.OK
        ans_text = 'Zmurki\nThe Star 2\nThe Star 1\nThe Star 0'
        assert response.body['response']['text'] == ans_text

    async def test_best_flims_with_genre(self, post_data):
        data = generate_request_data(
            intent_id='best_films_by_rating_and_genre',
            slots={'genre': 'Adventure'}
        )
        response = await post_data('/alice_api/v1/alice', data=data)
        assert response.status == HTTPStatus.OK
        ans_text = 'Zmurki'
        assert response.body['response']['text'] == ans_text
