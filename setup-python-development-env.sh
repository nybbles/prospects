#!/usr/bin/env bash
curl -O https://raw.github.com/pypa/virtualenv/master/virtualenv.py
if [ ! -e  ~/.virtualenvs ]
then
    mkdir ~/.virtualenvs
fi
python virtualenv.py ~/.virtualenvs/prospects
. ~/.virtualenvs/prospects/bin/activate
rm virtualenv.py virtualenv.pyc

