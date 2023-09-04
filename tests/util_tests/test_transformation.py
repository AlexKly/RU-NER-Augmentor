import pytest

from src.utils.transformation import transform

test_sample = 'Задача NLP - извлечении именованных сущностей (NER)'


def test_transform_original():
    assert transform(
        tokens=test_sample.split(' '),
        transformation_case='orig'
    ) == ['Задача', 'NLP', '-', 'извлечении', 'именованных', 'сущностей', '(NER)']


def test_transform_lowercase():
    assert transform(
        tokens=test_sample.split(' '),
        transformation_case='orig_lowercase'
    ) == ['задача', 'nlp', '-', 'извлечении', 'именованных', 'сущностей', '(ner)']


def test_transform_uppercase():
    assert transform(
        tokens=test_sample.split(' '),
        transformation_case='orig_uppercase'
    ) == ['ЗАДАЧА', 'NLP', '-', 'ИЗВЛЕЧЕНИИ', 'ИМЕНОВАННЫХ', 'СУЩНОСТЕЙ', '(NER)']


def test_transform_transliterating():
    assert transform(
        tokens=test_sample.split(' '),
        transformation_case='transliterated'
    ) == ['Zadacha', 'NLP', '-', 'izvlechenii', 'imenovannyh', 'suschnostej', '(NER)']


def test_transform_transliterated_and_lowercase():
    assert transform(
        tokens=test_sample.split(' '),
        transformation_case='transliterated_lowercase'
    ) == ['zadacha', 'nlp', '-', 'izvlechenii', 'imenovannyh', 'suschnostej', '(ner)']


def test_transform_transliterated_and_uppercase():
    assert transform(
        tokens=test_sample.split(' '),
        transformation_case='transliterated_uppercase'
    ) == ['ZADAChA', 'NLP', '-', 'IZVLEChENII', 'IMENOVANNYH', 'SUSchNOSTEJ', '(NER)']
