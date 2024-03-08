def generate_request_data(
        intent_id: str = '',
        slots: dict | None = None,
        is_new_session: bool = False
):
    slots = slots or {}
    result_slots = {}
    for slot_name, slot_value in slots.items():
        result_slots[slot_name] = {'value': slot_value}
    res = {
        'session': {
            'new': is_new_session,
        },
        'request': {
            'nlu': {
                'intents': {
                    intent_id: {
                        "slots": result_slots
                    }
                }
            },
        },
    }
    return res
