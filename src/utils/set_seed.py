import random
import numpy as np


def set_seed(seed: int) -> None:
    """ Set unite seed for all project.

    :param seed: Seed value.
    :return:
    """
    random.seed(a=seed)
    np.random.seed(seed=seed)
