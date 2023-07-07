from src.utils.load_txt import load_txt
from src import DIR_VOCABS, COUNTRIES, REGIONS, CITIES, DISTRICTS, STREETS, LAST_NAMES_MALE, LAST_NAMES_FEMALE, \
    FIRST_NAMES_MALE, FIRST_NAMES_FEMALE, MIDDLE_NAMES_MALE, MIDDLE_NAMES_FEMALE


def test_load_txt_file():
    assert sorted(set(load_txt(path=f'{DIR_VOCABS}/location/countries.txt'))) == sorted(COUNTRIES.keys())
    assert sorted(set(load_txt(path=f'{DIR_VOCABS}/location/regions.txt'))) == sorted(REGIONS.keys())
    assert sorted(set(load_txt(path=f'{DIR_VOCABS}/location/cities.txt'))) == sorted(CITIES.keys())
    assert sorted(set(load_txt(path=f'{DIR_VOCABS}/location/districts.txt'))) == sorted(DISTRICTS.keys())
    assert sorted(set(load_txt(path=f'{DIR_VOCABS}/location/streets.txt'))) == sorted(STREETS.keys())
    assert sorted(set(load_txt(path=f'{DIR_VOCABS}/names/last_names_male.txt'))) == sorted(LAST_NAMES_MALE.keys())
    assert sorted(set(load_txt(path=f'{DIR_VOCABS}/names/last_names_female.txt'))) == sorted(LAST_NAMES_FEMALE.keys())
    assert sorted(set(load_txt(path=f'{DIR_VOCABS}/names/first_names_male.txt'))) == sorted(FIRST_NAMES_MALE.keys())
    assert sorted(set(load_txt(path=f'{DIR_VOCABS}/names/first_names_female.txt'))) == sorted(FIRST_NAMES_FEMALE.keys())
    assert sorted(set(load_txt(path=f'{DIR_VOCABS}/names/middle_names_male.txt'))) == sorted(MIDDLE_NAMES_MALE.keys())
    assert sorted(set(load_txt(path=f'{DIR_VOCABS}/names/middle_names_female.txt'))) == sorted(MIDDLE_NAMES_FEMALE.keys())
    assert sorted(set(load_txt(path=f'{DIR_VOCABS}/location/countries.txt'))) == sorted(COUNTRIES.keys())
