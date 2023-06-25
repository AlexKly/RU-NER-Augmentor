import os, marisa_trie

from src.utils.load_txt import load_txt

_ROOT = os.path.dirname(__file__)
DIR_VOCABS = f'{_ROOT}/vocabs'

COUNTRIES = marisa_trie.Trie(load_txt(path=f'{DIR_VOCABS}/countries.txt'))
REGIONS = marisa_trie.Trie(load_txt(path=f'{DIR_VOCABS}/regions.txt'))
CITIES = marisa_trie.Trie(load_txt(path=f'{DIR_VOCABS}/cities.txt'))
DISTRICTS = marisa_trie.Trie(load_txt(path=f'{DIR_VOCABS}/districts.txt'))
