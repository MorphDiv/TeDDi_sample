# clc

import argparse
import pathlib

PACKAGE_DIR = pathlib.Path(__file__).parent

TEST_ROOT = PACKAGE_DIR.parent / 'tests' / 'Corpus'

CORPUS_ROOT = PACKAGE_DIR.parent.parent.parent / '100LC' / 'Corpus'

CONFIG = PACKAGE_DIR / 'config.ini'

from .texts import Text
from .bodies import Body
from . import models

__all__ = ['Text', 'Body', 'load']


def load(args=None):
    parser = argparse.ArgumentParser('Loads the test database. Use -f for full database.')
    parser.add_argument('-f', '--full', help='Load the full database', action='store_true')

    args = parser.parse_args(args)

    args = [CORPUS_ROOT] if args.full else [TEST_ROOT]
    models.load(*args)

    return None
