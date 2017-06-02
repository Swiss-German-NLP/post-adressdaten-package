#!/usr/bin/python
# -*- coding: utf-8 -*-

import click
import logging

logger = logging.getLogger(__name__)

# Version of the package.
__version__ = '0.1'

# Constant strings to mitigate typos.
BUILD_WORDLIST = 'wordlist'
BUILD_POS = 'POS'
BUILD_NER = 'NER'
BUILD_ALL = 'all'
BUILDS = [BUILD_WORDLIST, BUILD_POS, BUILD_POS]

# TODO: Add the builds that this package supports.
SUPPORTED_BUILDS = [BUILD_ALL]


def print_version(context, parameter, value):
    if not value or context.resilient_parsing:
        return
    click.echo(__version__)
    context.exit()


# TODO: When your resource supports a worlist, do so here.
def wordlist():
    pass


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
