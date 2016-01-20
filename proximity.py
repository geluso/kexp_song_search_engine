#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import argparse
import ast
import sqlite3
import re

from datetime import datetime
from known_names import translate_artist
 
parser = argparse.ArgumentParser(description="Looks up songs played before and after a given song.")
parser.add_argument("--db", type=str, default="kexp.db", help="the location of the sqlite database")
parser.add_argument("--song", type=str, help="Song to look up.")
parser.add_argument("--artist", type=str, help="Artist to look up.")
parser.add_argument("--original", type=ast.literal_eval, default=True, help="If true then original song will show up in search results. If False then only other songs will be shown.")
parser.add_argument("--neighbors", type=int, default=2, help="The number of songs before and after target song to retrieve.")
parser.add_argument("--comments", type=ast.literal_eval, default=False, help="Show DJ comments?")
parser.add_argument("--limit", type=int, default=None, help="Max number of results to return")

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

def get_plays_by_artist(db, artist, limit):
  if (limit):
    sql = 'SELECT * FROM plays WHERE artist LIKE ? ORDER BY date DESC LIMIT ?;'
    db.execute(sql, ["%"+artist+"%", limit])
  else:
    sql = 'SELECT * FROM plays WHERE artist LIKE ? ORDER BY date DESC;'
    db.execute(sql, ["%"+artist+"%"])
  rows = db.fetchall()
  return rows

def get_plays_by_song(db, song, limit):
  if limit:
    sql = 'SELECT * FROM plays WHERE song LIKE ? ORDER BY date DESC LIMIT ?;'
    db.execute(sql, ["%"+song+"%", limit])
  else:
    sql = 'SELECT * FROM plays WHERE song LIKE ? ORDER BY date DESC;'
    db.execute(sql, ["%"+song+"%"])
  rows = db.fetchall()
  return rows

def get_plays_by_artist_and_song(db, artist, song, limit):
  if limit:
    sql = 'SELECT * FROM plays WHERE artist LIKE ? AND song LIKE ? ORDER BY date DESC LIMIT ?;'
    db.execute(sql, ["%" + artist + "%", "%"+song+"%", limit])
  else:
    sql = 'SELECT * FROM plays WHERE artist LIKE ? AND song LIKE ? ORDER BY date DESC;'
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

def songs_around(play, original, neighbors):
  date = play[0]

  # prevent original plays from being included by default
  before_sql = "SELECT * FROM plays WHERE date < ? ORDER BY date DESC LIMIT ?";
  after_sql = "SELECT * FROM plays WHERE date > ? ORDER BY date ASC LIMIT ?";

  db.execute(before_sql, [date, neighbors])
  before = db.fetchall()

  db.execute(after_sql, [date, neighbors])
  after = db.fetchall()

  if original:
    before.append(play)
  before.extend(after)

  return before

def gather_neighbors(plays, limit, num_neighbors):
  neighbors = []
  for play in plays:
    if limit is None or len(neighbors) < limit:
      near = songs_around(play, args.original, num_neighbors)
      for song in near:
        neighbors.append(song)

  return neighbors

def print_results(results):
  for song in results:
    if args.comments and song[3] != "null":
      print song[0][:-3], song[1], '- "'+song[2]+'"', song[3]
    else:
      print song[0][:-3], song[1], '- "'+song[2]+'"'

def allow_quotes(arg):
  arg = arg.replace("\\'", "'")
  arg = arg.replace("\\\"", "\"")
  return arg

args = parser.parse_args()
db = sqlite3.connect(args.db)
db.text_factory = str
db = db.cursor()

song = args.song
if (song):
  song = allow_quotes(song)

artist = args.artist
if artist:
  artist = allow_quotes(artist)

  # replace popular proper-english spellings
  # with janky-ass internationalizations
  artist = translate_artist(artist)

limit = args.limit

if (artist and song):
  message = 'Searching for "%s" by %s' % (song, artist)
  plays = get_plays_by_artist_and_song(db, artist, song, limit=limit)
elif(artist):
  message = 'Searching for Artist: "%s"' % (artist)
  plays = get_plays_by_artist(db, artist, limit=limit)
elif(song):
  message = 'Searching for Song: "%s"' % (song,)
  plays = get_plays_by_song(db, song, limit=limit)

print message
print "=" * len(message)

results = []
# skip searching for neighbor songs if neighbors is zero
if args.neighbors == 0:
  results = plays
else:
  results = gather_neighbors(plays, limit, args.neighbors)

if len(results) == 0:
  print "No Results."
else:
  print_results(results)
  print
  print "%d Results." % (len(results))

db.close()
