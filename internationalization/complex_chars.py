#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import argparse

import sys
import codecs
sys.stdout=codecs.getwriter('utf-8')(sys.stdout)

parser = argparse.ArgumentParser(description="Detect internationalizatins in words in line-separated a file")
parser.add_argument("filename", type=str, help="the file to be processed.")

args = parser.parse_args()

simple_chars = ",'!/+*:=\"$?&(-) 1234567890qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNMµÁÂÄÅÆÉÑÓÖ×ØÚÜàáâãäåæçèéêëìíîïðñòóôõöøùúûüýÿāăćęğģİıļłńŌōőœśşšżž".decode("utf-8")
replacements = {}

names = open(args.filename).readlines()

for name in names:
  name = name.strip().decode("utf-8")
  added = False
  if "." in name:
    for letter in name:
      if letter not in simple_chars:
        if not added:
          no_period_name = name.replace(".", "")
          code = 'known_names["%s"] = "%s"' % (no_period_name, name)
          print code
          added = True
