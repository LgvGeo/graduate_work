from http import HTTPStatus

from tests.utils.generate_request_data import generate_request_data


class TestNewSession:
    async def test_request_with_new_session(self, post_data):
        data = generate_request_data(is_new_session=True)
        response = await post_data('/alice_api/v1/alice', data=data)
        assert response.status == HTTPStatus.OK
        assert response.body['response']['text'] == 'Привет'

    async def test_request_with_not_new_session(self, post_data):
        data = generate_request_data()
        response = await post_data('/alice_api/v1/alice', data=data)
        assert response.status == HTTPStatus.OK
        assert response.body['response']['text'] != 'Привет'
