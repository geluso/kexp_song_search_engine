#!/usr/local/bin/python

import argparse
import sqlite3
import re
from subprocess import call
from bs4 import BeautifulSoup
from collections import namedtuple

from datetime import datetime
from datetime import timedelta
 
parser = argparse.ArgumentParser(description="Looks up songs played before and after a given song.")
parser.add_argument("--db", type=str, default="kexp.db", help="the location of the sqlite database")
parser.add_argument("--song", type=str, help="Song to look up.")
parser.add_argument("--artist", type=str, help="Artist to look up.")
parser.add_argument("--original", type=bool, default=False, help="If true then original song will show up in search results. If False then only other songs will be shown.")
parser.add_argument("--nearness", type=int, default=6, help="Proximity of other songs to be included in search results measured by number of minutes before and after target song is played.")
parser.add_argument("--comments", type=bool, default=False, help="Show DJ comments?")

def time_to_datetime(timestamp):
  # obtain the date from the filename
  match = re.match(r".*(....)-(..)-(..) (..):(..).*", timestamp)
  year = match.group(1)
  month = match.group(2)
  day = match.group(3)
  hour = match.group(4)
  minute = match.group(5)

  year = int(year)
  month = int(month)
  day = int(day)
  hour = int(hour)
  minute = int(minute)

  date = datetime(year=year, month=month, day=day, hour=hour, minute=minute)
  return date

def try_execute(db, sql, args):
  try:
    db.execute(sql, args)
  except sqlite3.IntegrityError:
    pass

def get_plays_by_artist(db, artist):
  sql = 'SELECT * FROM plays WHERE artist LIKE ? ORDER BY date ASC;'
  db.execute(sql, ["%"+artist+"%"])
  rows = db.fetchall()
  return rows

def get_plays_by_song(db, song):
  sql = 'SELECT * FROM plays WHERE song LIKE ? ORDER BY date ASC;'
  db.execute(sql, ["%"+song+"%"])
  rows = db.fetchall()
  return rows

def get_plays_by_artist_and_song(db, artist, song):
  sql = 'SELECT * FROM plays WHERE artist LIKE ? AND song LIKE ? ORDER BY date ASC;'
  db.execute(sql, ["%" + artist + "%", "%"+song+"%"])
  rows = db.fetchall()
  return rows

def plays_to_timestamps(rows):
  timestamps = []
  for row in rows:
    time = row[0]
    time = time_to_datetime(time)
    timestamps.append(time)
  return timestamps

def songs_around(play, original, nearness):
  before = play - timedelta(minutes=nearness)
  after = play + timedelta(minutes=nearness)

  # prevent original plays from being included by default
  if original:
    sql = 'SELECT * FROM plays WHERE date BETWEEN ? AND ? ORDER BY date ASC;'
    db.execute(sql, (before, after))
  else:
    sql = 'SELECT * FROM plays WHERE date BETWEEN ? AND ? AND date != ? ORDER BY date ASC;'
    db.execute(sql, (before, after, play))

  rows = db.fetchall()
  rows = set(tuple(rows))
  return rows

args = parser.parse_args()
db = sqlite3.connect(args.db)
db = db.cursor()
song = args.song

if (args.artist and args.song):
  message = 'Searching for "%s" by %s' % (args.song, args.artist)
  plays = get_plays_by_artist_and_song(db, args.artist, args.song)
elif(args.artist):
  message = 'Searching for Artist: "%s"' % (args.artist)
  plays = get_plays_by_artist(db, args.artist)
elif(args.song):
  message = 'Searching for Song: "%s"' % (args.song,)
  plays = get_plays_by_song(db, args.song)
print message
print "=" * len(message)

# dedupe the plays
deduped = []
for play in plays:
  if play not in deduped:
    deduped.append(play)
plays = deduped

timestamps = plays_to_timestamps(plays)

for timestamp in timestamps:
  near = songs_around(timestamp, args.original, args.nearness)
  for song in near:
    if args.comments and song[3] != "null":
      print song[0][:-3], song[1], '- "'+song[2]+'"', song[3]
    else:
      print song[0][:-3], song[1], '- "'+song[2]+'"'

db.close()
