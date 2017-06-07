#!/usr/bin/python
# -*- coding: utf-8 -*-
import os

import click
import logging

CANTONS = {
    'ZH': 'Zürich',
    'BE': 'Bern',
    'LU': 'Luzern',
    'UR': 'Uri',
    'SZ': 'Schwyz',
    'OW': 'Obwalden',
    'NW': 'Nidwalden',
    'GL': 'Glarus',
    'ZG': 'Zug',
    'FR': 'Freiburg',
    'SO': 'Solothurn',
    'BS': 'Basel-Stadt',
    'BL': 'Basel-Land',
    'SH': 'Schaffhausen',
    'AR': 'Appenzell Ausserrhoden',
    'AI': 'Appenzell Innerrhoden',
    'SG': 'St. Gallen',
    'GR': 'Graubünden',
    'AG': 'Aargau',
    'TG': 'Thurgau',
    'TI': 'Tessin',
    'VD': 'Waadt',
    'VS': 'Wallis',
    'NE': 'Neuenburg',
    'GE': 'Genf',
    'JU': 'Jura'
}

BASE_BLACKLIST = [
    '+',
    '-',
    '&',
    'A ',
    'A.',
    'ABB',
    'ABC',
    'ABM',
    'AMP',
    'AWEL',
    'z.',
    'Z.',
    'Z '
]

PLZ_BLACKLIST = [
    'SP',
    'BZ',
    'PF',
    'LZB',
    'Dist',
    'HUB',
    'DE',
    'IMPCA',
    'GK',
    'PL',
    'VZ',
    'CZ',
    'SC',
    'IM',
    'Zustellung',
    'CALL',
    'PV',
    'PS',
    'FL',
    'CS',
    'Kaserne',
    'Altstadt',
    'Post',
    'Verwaltung',
    'Marktplatz',
    'Paketzentrum',
    'Briefzentrum',
    'Asendia',
    'Corona',
    'Helsana',
    'Abg.',
    'ETH',
    'IBRS',
    'strasse',
    'Glattzentrum N. Wint.str.',  # Need more Information about this.
    'Presse',
    'Versand',
    'Versicherung',
    'Voice',
    'Triemli',
    'Sonder',
    'Digest',
    'Kanton',
    'via',
    'an ',
    'am ',
    'im ',
    'zum ',
    'ob ',
    'der ',
    'da ',
    'à',
    'Öa',
    'z',
    's',
    'i'
] + BASE_BLACKLIST

STR_BLACKLIST = [
    'A.',
    'Ant.',
    'Autobahnrastst.',
    'Begegnungszen.',
    'Bergrest.',
    'C.',
    'Dr.',
    'E.',
    'F.',
    'Forsch.',
    'G.',
    'Gebr.',
    'Gen.',
    'Gottl.',
    'Gottl.',
    'H.',
    'Haup.',
    'Hint.',
    'J.',
    'Johs.',
    'K.',
    'Kath.',
    'L.',
    'Landw.',
    'Lerchenfeldstr.',
    'Matzingerstr.',
    'O.',
    'Ottenbacherstr.',
    'Rest.'
    'Parc.',
    'Parschientschstr.',
    'R.',
    'Reg.',
    'Rest.',
    'Richtstrahlst.',
    'S.',
    'Sek.',
    'Stockerenstr.',
    'Talst.',
    'V.',
    'Vord.',
    'W.',
    'Waldparkstr.',
    'X.',
    'u.',
    'uf',
] + BASE_BLACKLIST

logger = logging.getLogger(__name__)

# Version of the package.
__version__ = '0.1'

BASE_DIR = os.path.dirname(os.path.realpath(__file__))
RESOURCE = '{}/data/{}'.format(BASE_DIR, 'adressdaten.csv')

# Constant strings to mitigate typos.
BUILD_WORDLIST = 'wordlist'
BUILD_POS = 'POS'
BUILD_NER = 'NER'
BUILD_ALL = 'all'
BUILDS = [BUILD_WORDLIST, BUILD_POS, BUILD_NER]

# TODO: Add the builds that this package supports.
SUPPORTED_BUILDS = [BUILD_WORDLIST, BUILD_ALL]


def print_version(context, parameter, value):
    if not value or context.resilient_parsing:
        return
    click.echo(__version__)
    context.exit()


def is_trustworthy_str(str_text):
    """
    The text will be checked for suspicious characters. And after, it will be sanitized.

    :param str_text: 
    :return: 
    """
    if any(char.isdigit() for char in str_text):
        # If name contains numbers, it is not relevant.
        return
    if '/' in str_text or '(' in str_text or ')' in str_text:
        return
    if any(x in str_text for x in CANTONS) or any(x in str_text for x in STR_BLACKLIST):
        # Contains a canton.
        return

    if 'b.' in str_text:
        str_text = str_text.replace('b.', 'bei')
    if 'St.' in str_text:
        str_text = str_text.replace('St.', 'Sankt')
    if 'a. A.' in str_text:
        str_text = str_text.replace('a. A.', 'an der Aare')
    if 'S. ' in str_text:
        str_text = str_text.replace('S.', 'Sogn')
    if 'Sta. ' in str_text:
        str_text = str_text.replace('Sta.', 'Santa')
    if ',' in str_text:
        str_text = str_text.replace(',', '')
    if '\'' in str_text:
        chunks = str_text.split('\'')
        str_text = chunks[1]

    return str_text


def is_trustworthy_plz(plz_text):
    """
    The text will be checked for suspicious characters. And after, it will be sanitized.
    
    :param plz_text: 
    :return: 
    """
    if any(char.isdigit() for char in plz_text):
        # If name contains numbers, it is not relevant.
        return
    if '/' in plz_text or '(' in plz_text or ')' in plz_text:
        return
    if any(x in plz_text for x in CANTONS) or any(x in plz_text for x in PLZ_BLACKLIST):
        # Contains a canton.
        return

    if 'b.' in plz_text:
        plz_text = plz_text.replace('b.', 'bei')
    if 'St.' in plz_text:
        plz_text = plz_text.replace('St.', 'Sankt')
    if 'a. A.' in plz_text:
        plz_text = plz_text.replace('a. A.', 'an der Aare')
    if 'S. ' in plz_text:
        plz_text = plz_text.replace('S.', 'Sogn')
    if 'Sta. ' in plz_text:
        plz_text = plz_text.replace('Sta.', 'Santa')
    if '\'' in plz_text:
        chunks = plz_text.split('\'')
        plz_text = chunks[1]

    return plz_text


def wordlist():
    linestring = open(RESOURCE, 'r').read()
    words = []
    lines = linestring.split('\n')
    for line in lines:
        table = line.split(';')
        if table[0] == '01':
            """
            NEW_PLZ1
            """
            if table[10] == '1':
                # Dataset is german
                text = is_trustworthy_plz(table[8])
                if text:
                    chunks = text.split(' ')
                    for chunk in chunks:
                        if chunk != chunk.lower():
                            # if the word is uppercased.
                            words.append(chunk)
            continue

        if table[0] == '02':
            """
            NEW_PLZ2
            """
            if table[4] == '1':
                # Dataset is german
                text = is_trustworthy_plz(table[6])
                if text:
                    chunks = text.split(' ')
                    for chunk in chunks:
                        if chunk != chunk.lower():
                            # if the word is uppercased.
                            words.append(chunk)
            continue

        # TODO: Include when found a method to filter for language.
        #  if table[0] == '03':
        #     """
        #     NEW_COM
        #     """
        #     text = is_trustworthy_plz(table[2])
        #     if text:
        #         chunks = text.split(' ')
        #         for chunk in chunks:
        #             words.append(chunk)

        if table[0] == '04':
            """
            NEW_STR
            """
            if table[8] == '1':
                # Dataset is german
                text = is_trustworthy_str(table[4])
                if text:
                    chunks = text.split(' ')  # STRBEZL
                    for chunk in chunks:
                        if chunk != chunk.lower():
                            # if the word is uppercased.
                            words.append(chunk)
            continue

        if table[0] == '05':
            """
            NEW_STRA
            """
            if table[9] == '1':
                # Dataset is german
                text = is_trustworthy_str(table[4])
                if text:
                    chunks = text.split(' ')  # STRBEZL
                    for chunk in chunks:
                        if chunk != chunk.lower():
                            # if the word is uppercased.
                            words.append(chunk)
            continue

    with open('wordlist.txt', 'w') as file:
        for word in sorted(set(words)):
            file.write(word + '\n')


# TODO: When your resource supports a POS-tagging, do so here.
def pos():
    pass


# TODO: When your resource supports a NER-tagging, do so here.
def ner():
    pass


@click.command()
@click.option('--build', '-b', type=click.Choice(SUPPORTED_BUILDS), help='What build you want to make.')
@click.option('--version', is_flag=True, help='Displays the version of this package.', callback=print_version,
              expose_value=False, is_eager=True)
def main(build):
    """
    This is a build script for swiss-german nlp tools.
    """
    logger.info("Started")

    if build not in SUPPORTED_BUILDS:
        click.echo("This build is not supported with this package.")
        exit()

    if build == BUILD_WORDLIST or build == BUILD_ALL:
        wordlist()
    if build == BUILD_NER or build == BUILD_ALL:
        ner()
    if build == BUILD_POS or build == BUILD_ALL:
        pos()


if __name__ == '__main__':
    main()
