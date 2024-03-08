from http import HTTPStatus

from tests.utils.generate_request_data import generate_request_data


class TestGettingFilmsWithDescription:
    async def test_get_film_with_descr(self, post_data):
        data = generate_request_data(
            intent_id='film_description',
            slots={'film': 'Zmurki'}
        )
        response = await post_data('/alice_api/v1/alice', data=data)
        assert response.status == HTTPStatus.OK
        ans_text = 'Название Zmurki \n Опиание: New World'
        assert response.body['response']['text'] == ans_text

    async def test_get_film_with_descr_not_exist(self, post_data):
        data = generate_request_data(
            intent_id='film_description',
            slots={'film': 'njnj'}
        )
        response = await post_data('/alice_api/v1/alice', data=data)
        assert response.status == HTTPStatus.OK
        ans_text = 'Не найдено ничего про фильм njnj'
        assert response.body['response']['text'] == ans_text
