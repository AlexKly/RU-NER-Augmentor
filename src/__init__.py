import os, marisa_trie

from src.utils.load_txt import load_txt

_ROOT = os.path.dirname(__file__)
DIR_VOCABS = f'{_ROOT}/vocabs'

COUNTRIES = marisa_trie.Trie(load_txt(path=f'{DIR_VOCABS}/location/countries.txt'))
REGIONS = marisa_trie.Trie(load_txt(path=f'{DIR_VOCABS}/location/regions.txt'))
CITIES = marisa_trie.Trie(load_txt(path=f'{DIR_VOCABS}/location/cities.txt'))
DISTRICTS = marisa_trie.Trie(load_txt(path=f'{DIR_VOCABS}/location/districts.txt'))
STREETS = marisa_trie.Trie(load_txt(path=f'{DIR_VOCABS}/location/streets.txt'))
LAST_NAMES_MALE = marisa_trie.Trie(load_txt(path=f'{DIR_VOCABS}/names/last_names_male.txt'))
LAST_NAMES_FEMALE = marisa_trie.Trie(load_txt(path=f'{DIR_VOCABS}/names/last_names_female.txt'))
FIRST_NAMES_MALE = marisa_trie.Trie(load_txt(path=f'{DIR_VOCABS}/names/first_names_male.txt'))
FIRST_NAMES_FEMALE = marisa_trie.Trie(load_txt(path=f'{DIR_VOCABS}/names/first_names_female.txt'))
MIDDLE_NAMES_MALE = marisa_trie.Trie(load_txt(path=f'{DIR_VOCABS}/names/middle_names_male.txt'))
MIDDLE_NAMES_FEMALE = marisa_trie.Trie(load_txt(path=f'{DIR_VOCABS}/names/middle_names_female.txt'))
