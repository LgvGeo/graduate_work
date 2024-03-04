from fastapi import APIRouter, Depends
from fastapi.responses import ORJSONResponse
from services.alice import AliceService, get_alice_service

router = APIRouter()


def parse_intents(request):
    intents = request.get('request', {}).get('nlu', {}).get('intents', {})
    return intents


def is_new_session(request):
    return request['session']['new'] is True


@router.post(
        '/alice',
        response_class=ORJSONResponse,
        summary="Alice request",
        description="Process Alice Request"
)
async def process_alice_request(
    request: dict,
    alice_service: AliceService = Depends(get_alice_service)
) -> ORJSONResponse:
    response_pattern = {
        'response': {
            'text': 'Ваш вопрос непонятен, повторите еще раз'
        },
        'version': '1.0'
    }
    if is_new_session(request):
        response_pattern['response']['text'] = 'Привет'
        return ORJSONResponse(response_pattern)
    intents = parse_intents(request)
    if not intents:
        return ORJSONResponse(response_pattern)
    txt = alice_service.process_intents(intents)
    response_pattern['response']['text'] = txt
    return ORJSONResponse(response_pattern)
