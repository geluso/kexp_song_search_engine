#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import argparse

import sys
import codecs
sys.stdout=codecs.getwriter('utf-8')(sys.stdout)

parser = argparse.ArgumentParser(description="Detect internationalizatins in words in line-separated a file")
parser.add_argument("filename", type=str, help="the file to be processed.")

args = parser.parse_args()

simple_chars = "‐µÁÂÄÅÆÉÑÓÖ×ØÚÜàáâãäåæçèéêëìíîïðñòóôõöøùúûüýÿāăćęğģİıļłńŌōőœśşšżž".decode("utf-8")
replacements = {}

def add_replacement(askii, foreign):
  foreign = foreign.decode("utf-8")
  for letter in foreign:
    replacements[letter] = askii

add_replacement("0", "Ø")
add_replacement("-", "‐")
add_replacement("a", "ÁÂÄÅàáâãäåāă")
add_replacement("ae", "Ææ")
add_replacement("c", "ćç")
add_replacement("e", "Éèéêëę")
add_replacement("g", "ğģ")
add_replacement("l", "ıļł")
add_replacement("n", "Ñńñ")
add_replacement("i", "İìíîï")
add_replacement("o", "ÓÖŌōőðòóôõöø")
add_replacement("oe", "œ")
add_replacement("s", "śşš")
add_replacement("u", "µùúûüÚÜ")
add_replacement("x", "×")
add_replacement("y", "ýÿ")
add_replacement("z", "żž")

def replace_foreign_chars(name):
  new_name = ""
  for letter in name:
    if letter in simple_chars:
      letter = replacements[letter]
    new_name += letter
  return new_name

names = open(args.filename).readlines()

ascii_to_unicode = {}

for name in names:
  name = name.strip().decode("utf-8")
  added = False
  for letter in name:
    if letter in simple_chars or letter == ".":
      if not added:
        ascii_name = replace_foreign_chars(name)
        ascii_name = ascii_name.lower()

        no_period_name = ascii_name.replace(".", "")
        space_dash_name = ascii_name.replace("-", " ")
        space_dash_no_period = no_period_name.replace("-", " ")

        ascii_to_unicode[ascii_name] = name
        ascii_to_unicode[no_period_name] = name
        ascii_to_unicode[space_dash_name] = name
        ascii_to_unicode[space_dash_no_period] = name
        added = True

for ascii_name in ascii_to_unicode:
  unicode_name = ascii_to_unicode[ascii_name]
  unicode_name = unicode_name.replace("\"", "\\\"")

  ascii_name = ascii_name.replace("\"", "\\\"")

  code = 'known_names["%s"] = "%s"' % (ascii_name, unicode_name)
  print code
