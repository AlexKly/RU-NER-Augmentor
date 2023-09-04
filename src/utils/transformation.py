import numpy as np
import transliterate

from src.attrs.attributes import TRANSFORMATION_CASES


def transform(tokens: list, transformation_case: str = None) -> list:
    """ Transform input tokens to:
        * original (no transformations)
        * lowercase
        * uppercase
        * transliterating
        * transliterating + lowercase
        * transliterating + uppercase

    :param tokens: Input tokens.
    :param transformation_case: Type of transformations (can be None, then it will be chosen random).
    :return: Transformed tokens.
    """
    if transformation_case is None or transformation_case not in TRANSFORMATION_CASES[0]:
        case = np.random.choice(a=TRANSFORMATION_CASES[0], p=TRANSFORMATION_CASES[1])
    else:
        case = transformation_case
    if case == 'orig_lowercase':
        tokens = [token.lower() for token in tokens]
    if case == 'orig_uppercase':
        tokens = [token.upper() for token in tokens]
    if case == 'transliterated':
        tokens = [transliterate.translit(value=token, language_code='ru', reversed=True) for token in tokens]
    if case == 'transliterated_lowercase':
        tokens = [transliterate.translit(value=token.lower(), language_code='ru', reversed=True) for token in tokens]
    if case == 'transliterated_uppercase':
        tokens = [transliterate.translit(value=token.upper(), language_code='ru', reversed=True) for token in tokens]
    return tokens
