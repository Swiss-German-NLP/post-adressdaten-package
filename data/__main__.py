#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
import os.path

logger = logging.getLogger(__name__)

# Version of the package.
__version__ = '0.1'

BASE_DIR = os.path.dirname(os.path.realpath(__file__))
RAW_FILENAME = 'adressdaten_raw.csv'
TARGET_FILENAME = 'adressdaten.csv'
ABSOLUTE_RAW_FILENAME = '{}/{}'.format(BASE_DIR, RAW_FILENAME)
ABSOLUTE_TARGET_FILENAME = '{}/{}'.format(BASE_DIR, TARGET_FILENAME)
TABLE_BLACKLIST = ['00', '08', '12']


def build_resource():
    linestring = open(ABSOLUTE_RAW_FILENAME, 'r', encoding='ISO-8859-1').read()
    final_resource = []
    lines = linestring.split('\n')
    for line in lines:
        contin = True
        for table in TABLE_BLACKLIST:
            if line.startswith(table):
                contin = False
        if contin and line != '':
            final_resource.append(line)

    with open(ABSOLUTE_TARGET_FILENAME, 'w') as file:
        for line in final_resource:
            file.write(line + '\n')


def main():
    """
    This script build the resource from the raw resource.
    """
    logger.info("Started")
    if os.path.exists(ABSOLUTE_RAW_FILENAME):
        build_resource()
    else:
        logging.error('The file %s was not found.' % RAW_FILENAME)


if __name__ == '__main__':
    main()
