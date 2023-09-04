import ast
import numpy as np
import pandas as pd
from tqdm import tqdm

from src.augmentor import RUNERAugmentor
from src.utils.transformation import transform
from src.attrs.attributes import TRANSFORMATION_CASES

aug = RUNERAugmentor()


def example() -> None:
    # Load and preprocess input data:
    df = pd.read_csv('ner_samples.csv').iloc[:100]
    df['tokens'] = df['tokens'].apply(ast.literal_eval)
    df['ner_tags'] = df['ner_tags'].apply(ast.literal_eval)
    tokens, ner_tags = list(), list()
    for i in tqdm(range(df.shape[0])):
        # Choose transformation type randomly:
        t_type = np.random.choice(a=TRANSFORMATION_CASES[0], p=TRANSFORMATION_CASES[1])
        tokens_tmp, ner_tags_tmp = list(), list()
        for p in zip(df['tokens'].iloc[i], df['ner_tags'].iloc[i]):
            tag, ner_tag = [p[0]], ['O']
            orig_tag = p[1].split('-')[-1]
            # To augment if token is person or location:
            if orig_tag in ['PER', 'LOC']:
                tag, ner_tag = aug.augment(s=p[0], tag=orig_tag)
            tokens_tmp += [t for t in tag]
            ner_tags_tmp += [nt for nt in ner_tag]
        # Transform all sentence like augmented token:
        tokens += [transform(tokens=tokens_tmp, transformation_case=t_type)]
        ner_tags += [ner_tags_tmp]
    # Form and save augmented samples to DataFrame:
    df_augmented = pd.DataFrame({'tokens': tokens, 'ner_tags': ner_tags})
    df_augmented.to_csv('ner_samples_augmented.csv')


if __name__ == '__main__':
    example()
