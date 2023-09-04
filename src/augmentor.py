import typing, random, pymorphy2

from src import COUNTRIES, REGIONS, CITIES, DISTRICTS, STREETS, LAST_NAMES_MALE, LAST_NAMES_FEMALE, FIRST_NAMES_MALE, \
    FIRST_NAMES_FEMALE, MIDDLE_NAMES_MALE, MIDDLE_NAMES_FEMALE
from src.attrs.attributes import INPUT_TAG_MAP, TAG_MAP, NOT_NER_TAG, REPLACEMENT_MAP

ANCHORS = [anchor for k in NOT_NER_TAG for anchor in NOT_NER_TAG[k]]


class RUNERAugmentor:
    """ RU-NER Augmentor performs augmentation for input pair text-token and helps to dilute your dataset various
    russian constructions for training NER-model (or with additional transformations for different task, for example,
    text classification).\n\n
    This class can return augmented tokens and tagging with settings preset in file configurations (attrs).\n\n
    You can specify tagging format for class. It's possible BIOLU, BIO and single-token tagging format.\n\n
    Class supports only two NER-tag for augmentation: PER and LOC.\n\n
    PER tag splits into following sub-tags for generation: LAST_NAME, FIRST_NAME and MIDDLE_NAME.\n\n
    LOC tag splits into following sub-tags for generation: COUNTRY, REGION, CITY, DISTRICT, STREET and HOUSE.\n\n
    Usage example:\n
    aug = RUNERAugmentor()\n
    print(aug.augment(s=['Иванов'], tag='PER'))\n
    >>> ([], [])
    print(aug.augment(s=['Москве'], tag='LOC'))\n
    >>> ([], [])
    """
    def __init__(self, tagging_format: str = 'BIOLU') -> None:
        """ Create 'RUNERAugmentor' object class.

        :param tagging_format: Tagging format for output DataFrame: 'BIOLU', 'BIO', 'single-token'
        :return:
        """
        self.morph = pymorphy2.MorphAnalyzer(lang='ru')
        self.tagging_format = tagging_format

    def detect_case(self, s: str) -> typing.Tuple[str, str, str, str]:
        """ Detect input string (word) case (for pymorphy2 lib.) for correct transformation.

        :param s: Input string (word).
        :return: Detected case tags for transformation.
        """
        cases = {
            'pos': 'NOUN',
            'case': random.choice(seq=['nomn', 'gent', 'datv', 'accs', 'ablt']),
            'gender': random.choice(seq=['masc', 'femn']),
            'number': random.choice(seq=['sing', 'plur']),
        }
        p = self.morph.parse(word=s)[0]
        tags = (
            p.tag.POS if p.tag.POS is not None else cases['pos'],
            p.tag.case if p.tag.case is not None else cases['case'],
            p.tag.gender if p.tag.gender is not None and p.tag.gender in ['masc', 'femn'] else cases['gender'],
            p.tag.number if p.tag.number is not None else cases['number'],
        )
        return tags

    def inflect(self, s: str, tags: typing.Set[str], casing: bool = True) -> str:
        """ Do inflection for input string according right form in text.
        If string has more than 1 word function tries to match common inflection to all words in string.

        :param s: Input string.
        :param tags: Set of parameters for input string inflecting.
        :param casing:
        :return: Inflected string.
        """
        tags = {tag for tag in tags if tag is not None}
        inflected_s = list()
        s = ' '.join(list(filter(None, s.split(' '))))
        for token in s.split(' '):
            try:
                inflected_s += [self.morph.parse(word=token)[0].inflect(required_grammemes=tags).word]
            except AttributeError:
                inflected_s += [token]
        if casing:
            inflected_s = [f'{w[0].upper()}{w[1:]}' if w not in ANCHORS else w for w in inflected_s]
        return ' '.join(inflected_s)

    @staticmethod
    def tagging(s: list, t: list) -> typing.Tuple[list, list]:
        """ NER-Tagging for input string.

        :param s: Input string.
        :param t: Original tags.
        :return: Tokens and NER-tags.
        """
        tokens, tags = list(), list()
        for p in zip(s, t):
            cnt = 0
            tokens_tmp = p[0].split(' ')
            for i in range(len(tokens_tmp)):
                tokens += [tokens_tmp[i]]
                if p[1] == 'O':
                    tags += ['O']
                else:
                    if tokens_tmp[i].lower() in NOT_NER_TAG[p[1]]:
                        tags += ['O']
                        cnt = 0
                    else:
                        if len(tokens_tmp) < 2:
                            tags += [f'U-{p[1]}']
                            cnt += 1
                        else:
                            if i < len(tokens_tmp) - 1:
                                if tokens_tmp[i + 1].lower() in NOT_NER_TAG[p[1]]:
                                    if cnt == 0:
                                        tags += [f'U-{p[1]}']
                                    else:
                                        tags += [f'L-{p[1]}']
                                    cnt = 0
                                else:
                                    if cnt == 0:
                                        tags += [f'B-{p[1]}']
                                    else:
                                        tags += [f'I-{p[1]}']
                                    cnt += 1
                            else:
                                if cnt == 0:
                                    tags += [f'U-{p[1]}']
                                else:
                                    tags += [f'L-{p[1]}']
        return tokens, tags

    def generate_augmentation(
            self,
            entity: str,
            inflecting_tags: typing.Tuple[str, str, str, str]
    ) -> typing.Tuple[list, list]:
        """ Generate new augmentation (string) based on tags got the input word/collocation.

        :param entity: Augmentation type.
        :param inflecting_tags: inflecting tags/cases for transforming string according to rule of the input string. (was got after 'pymorphy2' parsing).
        :return: Generated and inflected tokens and tags.
        """
        if entity == 'full_name':
            if inflecting_tags[2] == 'masc':
                ln = random.choice(seq=LAST_NAMES_MALE.keys())
                fn = random.choice(seq=FIRST_NAMES_MALE.keys())
                md = random.choice(seq=MIDDLE_NAMES_MALE.keys())
            if inflecting_tags[2] == 'femn':
                ln = random.choice(seq=LAST_NAMES_FEMALE.keys())
                fn = random.choice(seq=FIRST_NAMES_FEMALE.keys())
                md = random.choice(seq=MIDDLE_NAMES_FEMALE.keys())
            c = random.randint(a=0, b=6)
            if c == 0:
                value = [
                    (self.inflect(s=ln, tags=set(inflecting_tags), casing=True), 'LAST_NAME'),
                    (self.inflect(s=fn, tags=set(inflecting_tags), casing=True), 'FIRST_NAME'),
                    (self.inflect(s=md, tags=set(inflecting_tags), casing=True), 'MIDDLE_NAME'),
                ]
            if c == 1:
                value = [
                    (self.inflect(s=ln, tags=set(inflecting_tags), casing=True), 'LAST_NAME'),
                    (self.inflect(s=fn, tags=set(inflecting_tags), casing=True), 'FIRST_NAME'),
                ]
            if c == 2:
                value = [
                    (self.inflect(s=fn, tags=set(inflecting_tags), casing=True), 'FIRST_NAME'),
                    (self.inflect(s=md, tags=set(inflecting_tags), casing=True), 'MIDDLE_NAME'),
                ]
            if c == 3:
                value = [
                    (self.inflect(s=ln, tags=set(inflecting_tags), casing=True), 'LAST_NAME'),
                    (self.inflect(s=md, tags=set(inflecting_tags), casing=True), 'MIDDLE_NAME'),
                ]
            if c == 4:
                value = [(self.inflect(s=ln, tags=set(inflecting_tags), casing=True), 'LAST_NAME')]
            if c == 5:
                value = [(self.inflect(s=fn, tags=set(inflecting_tags), casing=True), 'FIRST_NAME')]
            if c == 6:
                value = [(self.inflect(s=md, tags=set(inflecting_tags), casing=True), 'MIDDLE_NAME')]
            random.shuffle(x=value)
        if entity in ['country', 'region', 'city', 'street', 'district', 'address']:
            # General:
            country = random.choice(seq=COUNTRIES.keys())
            region = random.choice(seq=REGIONS.keys())
            city = random.choice(seq=CITIES.keys())
            district = random.choice(seq=DISTRICTS.keys())
            street = random.choice(seq=STREETS.keys())
            # Additional:
            postcode = '{0:04}'.format(random.randint(a=0, b=999999))
            prefix_house = ''.join([
                random.choice(seq=['д', 'д.', 'д,', 'Д', 'Д.', 'Д,', 'дом', 'дом,', 'Дом', 'Дом,', 'стр', 'стр.',
                                   'стр.', 'строение', ''])
            ])
            # д25 кв 61
            num_house_1 = random.randint(a=1, b=999)
            num_house_2 = random.randint(a=1, b=99)
            num_house = random.choice(seq=[
                num_house_1,
                f'{num_house_1}/{num_house_2}'
            ])
            extra_num_house = f'{random.choice(seq=["офис", "оф.", "о.", "кв.", "квартира"])} {random.randint(a=1, b=999)}'
            house = f'{prefix_house} {num_house} {random.choice(seq=["", extra_num_house])}'.strip()
            cc = random.choice(seq=[0, 1, 2])
            if cc == 1:
                for anchor in NOT_NER_TAG['STREET']:
                    street = street.replace(anchor, '')
                street = street.strip()
            if cc == 2:
                for rplcmnt in REPLACEMENT_MAP['STREET']:
                    street = street.replace(rplcmnt[0], rplcmnt[1])
                street = street.strip()
            if entity == 'country':
                value = [(self.inflect(s=country, tags=set(inflecting_tags), casing=True), 'COUNTRY')]
            if entity == 'region':
                value = [(self.inflect(s=region, tags=set(inflecting_tags), casing=True), 'REGION')]
            if entity == 'city':
                value = [(self.inflect(s=city, tags=set(inflecting_tags), casing=True), 'CITY')]
            if entity == 'district':
                value = [(self.inflect(s=district, tags=set(inflecting_tags), casing=True), 'DISTRICT')]
            if entity == 'street':
                c = random.randint(a=0, b=1)
                if c == 0:
                    value = [(self.inflect(s=street, tags=set(inflecting_tags), casing=True), 'STREET')]
                if c == 1:
                    value = [
                        (self.inflect(s=street, tags=set(inflecting_tags), casing=True), 'STREET'),
                        (self.inflect(s=house, tags=set(inflecting_tags), casing=True), 'HOUSE'),
                    ]
            if entity == 'address':
                c = random.randint(a=0, b=4)
                if c == 0:
                    value = [
                        (postcode, 'O'),
                        (random.choice(seq=['Россия', 'РФ', 'Российская Федерация']), 'COUNTRY'),
                        (region, 'REGION'),
                        (district, 'DISTRICT'),
                        (city, 'CITY'),
                        (street, 'STREET'),
                        (house, 'HOUSE'),
                    ]
                if c == 1:
                    value = [
                        (street, 'STREET'),
                        (house, 'HOUSE'),
                        (city, 'CITY'),
                        (postcode, 'O'),
                    ]
                if c == 2:
                    value = [
                        (street, 'STREET'),
                        (house, 'HOUSE'),
                        (city, 'CITY'),
                    ]
                if c == 3:
                    value = [
                        (street, 'STREET'),
                        (house, 'HOUSE'),
                        (city, 'CITY'),
                        (region, 'REGION'),
                        (postcode, 'O'),
                    ]
                if c == 4:
                    value = [
                        (street, 'STREET'),
                        (house, 'HOUSE'),
                        (city, 'CITY'),
                        (district, 'DISTRICT'),
                        (region, 'REGION'),
                        (postcode, 'O'),
                    ]
        return self.tagging(s=[p[0] for p in value], t=[p[1] for p in value])

    @staticmethod
    def biolu2bio(tags: list) -> list:
        """ Relabel tags to BIO-format. Where:\n
        * 'B' - begging token,
        * 'I' - inner token.

        Which transformation need be apllied:\n
        * 'U' --> 'B'
        * 'L' --> 'I'

        :param tags: NER-tags for text tokens.
        :return: Relabeled NER-tokens.
        """
        return [f'B-{tag.split("-")[-1]}' if tag.split('-')[0] == 'U' else
                f'I-{tag.split("-")[-1]}' if tag.split('-')[0] == 'L' else
                tag for tag in tags]

    @staticmethod
    def biolu2single_token(tags: list) -> list:
        """ Relabel tags to single token format. Here just needs to cut any token's prefixes.\n
            Example:\n
            * ['B-COUNTRY', 'L-COUNTRY'] --> ['COUNTRY', 'COUNTRY']

            :param tags: NER-tags for text tokens.
            :return: Relabeled NER-tokens.
            """
        return [tag.split('-')[-1] for tag in tags]

    def augment(self, s: str, tag: str) -> typing.Tuple[list, list]:
        """ Generate string based on old string rules and NER-tag.\n
        Transformation pipeline:\n
        * detect sub-tag (randomly)
        * define inflecting tags and cases (pymorphy2)
        * generate new string based in sub-tag and inflecting tags (vocabs)
        * relabelling tagging format (bilio, bio, single-token)

        :param s: Input string.
        :param tag: Input NER-tag.
        :return: Return split into tokens generated new string and tokens.
        """
        # Chose what type it needs to generate based on input ner-tag:
        if tag == INPUT_TAG_MAP['PERSON']:
            tag = 'full_name'
        if tag == INPUT_TAG_MAP['LOCATION']:
            tag = random.choice(seq=['address', 'country', 'region', 'city', 'district', 'street'])
        # Define tags and cases for input word/collocation which needs to be replaced:
        inflecting_tags = self.detect_case(s=s)
        # Generate new word/collocation:
        tokens, tags = self.generate_augmentation(entity=tag, inflecting_tags=inflecting_tags)
        # Change tagging:
        if self.tagging_format == 'BIO':
            tags = self.biolu2bio(tags=tags)
        if self.tagging_format == 'single_token':
            tags = self.biolu2single_token(tags=tags)
        # Last formatting:
        tags = ['O' if tag == 'O' else f'{tag.split("-")[0]}-{TAG_MAP[tag.split("-")[-1]]}' for tag in tags]
        return tokens, tags
