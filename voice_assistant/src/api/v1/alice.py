from fastapi import APIRouter, Depends
from fastapi.responses import ORJSONResponse

from services.alice import AliceService, get_alice_service

router = APIRouter()


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
    txt = alice_service.process_request(request)
    response_pattern['response']['text'] = txt
    return ORJSONResponse(response_pattern)
