Post Adressdaten Package
=============

This package was provided by "Die Post" for the public domain.

More information about the license, see [this link](https://www.post.ch/de/geschaeftlich/themen-a-z/adressen-pflegen-und-geodaten-nutzen/adress-und-geodaten).


# How to get the resource

1. Sign-up [here](https://account.post.ch/idp/?login&app=portal-delivery&service=klp)
2. Go to the [download-center](https://service.post.ch/zopa/dlc/app/?lang=de&service=dlc-web#/main)
3. Download the resource.


# Building

Here is how to build this package.

## wordlist:

`python __main__.py --build=wordlist`

## POS

`python __main__.py --build=pos`

## NER

`python __main__.py --build=ner`


# Documentation

The documentation about the resource can be found [here](./Strassenverzeichnis%20mit%20Sortierdaten.pdf).

As we see in the document, we do not need all tables, since we only want to build text-files.

This tables are not needed:
- NEW_HEA (00)
- NEW_BOT_B (08)
- NEW_GEB_COM (12)

To save space, we only include a filtered version in Github.

The original file contains ~4'000'000 lines.
After the removing of the unnecessary tables it contains ~2'000'000 lines.

## Update the repository

Place a current dump of the resources at `data/adressdaten_raw.csv` and run the script `python /data/__main__.py`.

This will create a new `adressdaten.csv`file.


# Author/Contributors

- [Dominik Müller](https://github.com/CoalaJoe)
