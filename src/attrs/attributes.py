INPUT_TAG_MAP = {
    'LOCATION': 'LOC',
    'PERSON': 'PER',
}

TAG_MAP = {
    'COUNTRY': 'DMN_COUNTRY',
    'REGION': 'DMN_REGION',
    'CITY': 'DMN_CITY',
    'DISTRICT': 'DMN_DISTRICT',
    'STREET': 'DMN_STREET',
    'HOUSE': 'DMN_HOUSE',
    'LAST_NAME': 'DMN_LAST_NAME',
    'FIRST_NAME': 'DMN_FIRST_NAME',
    'MIDDLE_NAME': 'DMN_MIDDLE_NAME',
}

NOT_NER_TAG = {
    'LAST_NAME': [],
    'FIRST_NAME': [],
    'MIDDLE_NAME': [],
    'COUNTRY': [],
    'REGION': ['республика', 'область', 'ао', 'автономная', 'область', 'автономный', 'округ', 'край', 'народная'],
    'CITY': ['г.'],
    'DISTRICT': ['район'],
    'STREET': ['алл.', 'ш.', 'пр.', 'наб.', 'бул.', 'пер.', 'ул.'],
    'HOUSE': [],
    'O': [],
}
