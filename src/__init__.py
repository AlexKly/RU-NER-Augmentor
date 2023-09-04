import os, yaml, pathlib, marisa_trie

from src.utils.set_seed import set_seed
from src.utils.load_txt import load_txt

_ROOT = pathlib.Path(os.path.dirname(__file__)).parent
DIR_SRC = _ROOT/'src'
DIR_UTILS = DIR_SRC/'utils'
DIR_VOCABS = DIR_SRC/'vocabs'


# Load configs:
with (_ROOT/'configs.yml').open('r') as f:
    CONFIGS = yaml.safe_load(stream=f)

# Load vocabs:
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

# Set unite seed for all project:
set_seed(seed=CONFIGS['seed'])
