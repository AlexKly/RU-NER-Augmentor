import typing, pathlib


def load_txt(path: typing.Union[str, pathlib.Path], encoding: str = 'utf-8') -> list:
    """ Load vocab from txt file.

    :param path: Path to txt file.
    :param encoding: File encoding type (default: utf-8).
    :return: Vocab (list of strings).
    """
    with open(str(path), 'r', encoding=encoding) as reader:
        content = list(filter(None, set([el.replace('\n', '').strip() for el in reader.readlines()])))
    return content
