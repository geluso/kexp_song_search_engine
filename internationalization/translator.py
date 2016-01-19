#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import argparse

parser = argparse.ArgumentParser(description="Detect internationalizatins in words in line-separated a file")
parser.add_argument("filename", type=str, help="the file to be processed.")

args = parser.parse_args()

english = "`1234567890-=qwertyuiop[]\\asdfghjkl;'zxcvbnm,./~!@#$%^&*()_+QWERTYUIOP{}|ASDFGHJKL:\"ZXCVBNM<>? "
names = open(args.filename).readlines()

international_characters = ""

for name in names:
  name = name.strip().decode("utf-8")
  printed = False
  for letter in name:
    if letter not in english:
      if letter not in international_characters:
        international_characters += letter
      if not printed:
        print name
        printed = True

print international_characters
print "".join(sorted(international_characters))
