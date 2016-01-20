#!/usr/local/bin/python
# -*- coding: utf-8 -*-

from known_names import translate_artist

artists = ["Sigur Ros", "Bjork", "Motorhead", "Sufjan Stevens"]
for artist in artists:
  print translate_artist(artist)
