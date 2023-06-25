from faker import Faker
import typing, random, pymorphy2

from src.attrs.attributes import INPUT_TAG_MAP, TAG_MAP, NOT_NER_TAG
from src import COUNTRIES, REGIONS, CITIES, DISTRICTS


class RUNERAugmentor:
    """

    """
    def __init__(self, tagging_format: str = 'BIOLU') -> None:
        """ Create 'RUNERAugmentor' object class.

        :param tagging_format: Tagging format for output DataFrame: 'BIOLU', 'BIO', 'single-token'
        :return:
        """
        self.morph = pymorphy2.MorphAnalyzer(lang='ru')
        self.fake = Faker(locale='ru')
        self.tagging_format = tagging_format

    def detect_case(self, s: str) -> typing.Tuple[str, str, str, str]:
        """

        :param s:
        :return:
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
        for token in s.split(' '):
            try:
                inflected_s += [self.morph.parse(word=token)[0].inflect(required_grammemes=tags).word]
            except AttributeError:
                inflected_s += [token]
        if casing:
            inflected_s = [f'{w[0].upper()}{w[1:]}' for w in inflected_s]
        return ' '.join(inflected_s)

    @staticmethod
    def tagging(s: list, t: list) -> typing.Tuple[list, list]:
        """ NER-Tagging for input string.

        :param s: Input string.
        :param t: Original tags.
        :return: NER-
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
                value = [
                    (self.inflect(s=self.fake.last_name_male(), tags=set(inflecting_tags), casing=True), 'LAST_NAME'),
                    (self.inflect(s=self.fake.first_name_male(), tags=set(inflecting_tags), casing=True), 'FIRST_NAME'),
                    (self.inflect(s=self.fake.middle_name_male(), tags=set(inflecting_tags), casing=True), 'MIDDLE_NAME'),
                ]
            if inflecting_tags[2] == 'femn':
                value = [
                    (self.inflect(s=self.fake.last_name_female(), tags=set(inflecting_tags), casing=True), 'LAST_NAME'),
                    (self.inflect(s=self.fake.first_name_female(), tags=set(inflecting_tags), casing=True), 'FIRST_NAME'),
                    (self.inflect(s=self.fake.middle_name_female(), tags=set(inflecting_tags), casing=True), 'MIDDLE_NAME'),
                ]
            random.shuffle(x=value)
        if entity == 'last_name':
            if inflecting_tags[2] == 'masc':
                value = [(self.inflect(s=self.fake.last_name_male(), tags=set(inflecting_tags), casing=True), 'LAST_NAME')]
            if inflecting_tags[2] == 'femn':
                value = [(self.inflect(s=self.fake.last_name_female(), tags=set(inflecting_tags), casing=True), 'LAST_NAME')]
        if entity == 'first_name':
            if inflecting_tags[2] == 'masc':
                value = [(self.inflect(s=self.fake.first_name_male(), tags=set(inflecting_tags), casing=True), 'FIRST_NAME')]
            if inflecting_tags[2] == 'femn':
                value = [(self.inflect(s=self.fake.first_name_female(), tags=set(inflecting_tags), casing=True), 'FIRST_NAME')]
        if entity == 'middle_name':
            if inflecting_tags[2] == 'masc':
                value = [(self.inflect(s=self.fake.middle_name_male(), tags=set(inflecting_tags), casing=True), 'MIDDLE_NAME')]
            if inflecting_tags[2] == 'femn':
                value = [(self.inflect(s=self.fake.middle_name_female(), tags=set(inflecting_tags), casing=True), 'MIDDLE_NAME')]
        if entity == 'address':
            street = self.fake.street_address()
            value = [
                (random.choice(seq=[
                    f'г. {random.choice(seq=CITIES.keys())}',
                    f'г.{random.choice(seq=CITIES.keys())}',
                    random.choice(seq=CITIES.keys())
                ]), 'CITY'),
                (street.split(',')[0].strip(), 'STREET'),
                (street.split(',')[1].strip(), 'HOUSE'),
                (self.fake.postcode(), 'O'),
            ]
        if entity == 'country':
            value = [(self.inflect(s=random.choice(seq=COUNTRIES.keys()), tags=set(inflecting_tags), casing=True), 'COUNTRY')]
        if entity == 'region':
            value = [(self.inflect(s=random.choice(seq=REGIONS.keys()), tags=set(inflecting_tags), casing=True), 'REGION')]
        if entity == 'city':
            value = [(self.inflect(s=random.choice(seq=CITIES.keys()), tags=set(inflecting_tags), casing=True), 'CITY')]
        if entity == 'district':
            value = [(self.inflect(s=random.choice(seq=DISTRICTS.keys()), tags=set(inflecting_tags), casing=True), 'DISTRICT')]
        if entity == 'street':
            street = self.fake.street_address()
            value = [
                (f'{street.split(",")[0].strip().split(" ")[0].strip()} {self.inflect(s=street.split(",")[0].strip().split(" ")[-1].strip(), tags=set(inflecting_tags), casing=True)}', 'STREET'),
                (street.split(',')[1].strip(), 'HOUSE')
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
        * generate new string based in sub-tag and inflecting tags (faker/vocabs)
        * relabelling tagging format (bilio, bio, single-token)

        :param s: Input string.
        :param tag: Input NER-tag.
        :return: Return split into tokens generated new string and tokens.
        """
        # Chose what type it needs to generate based on input ner-tag:
        if tag == INPUT_TAG_MAP['PERSON']:
            tag = random.choice(seq=['full_name', 'last_name', 'first_name', 'middle_name'])
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
