#!/usr/local/bin/python

import argparse
import datetime
from subprocess import call
 
parser = argparse.ArgumentParser(description="Downloads an entire year of KEXP playlist data, one hour at a time.")
parser.add_argument("year", type=int, help="The year to scrape.")
parser.add_argument("--outdir", type=str, help="The directory to place the scrape in.")

URL = "http://kexp.org/playlist/"
date_format = "%d/%d/%d/%s"
file_format = "%d-%02d-%02d-%02d.html"

args = parser.parse_args()

def scrape_year(year):
  for month in range(1, 13):
    for day in range(1, 32):
      #morning
      for hour in range(1, 13):
        scrape(year, month, day, hour, "am")
        scrape(year, month, day, hour, "pm")

def scrape(year, month, day, hour, pm):
  time = str(hour) + pm
  timestamp = date_format % (year, month, day, time)
  url = URL + timestamp

  if hour == 12 and pm == "am":
    hour = 0
  elif pm == "pm" and hour < 12:
    hour += 12

  filename = file_format % (year, month, day, hour)

  if args.outdir:
    cmd = "curl %s > %s/%s" % (url, args.outdir, filename)
  else:
    cmd = "curl %s > %s" % (url, filename)
  print cmd
  call(cmd, shell=True)

print "scraping", args.year
scrape_year(args.year)
