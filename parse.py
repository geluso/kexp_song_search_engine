#!/usr/local/bin/python

import argparse
import sqlite3
import re
from subprocess import call
from bs4 import BeautifulSoup
from datetime import datetime
 
parser = argparse.ArgumentParser(description="Parses song, artist and playtime information from the KEXP playlist page.")
parser.add_argument("html", type=str, help="the HTML file containing KEXP playlist information for one hour.")
parser.add_argument("db", type=str, nargs="?", default="", help="the location of the sqlite database")

def parse_date(filename):
  # obtain the date from the filename
  match = re.match(r".*(....-..-..)-(..).*", args.html)
  date = match.group(1)
  hour = match.group(2)

  if hour == "00":
    print filename

  return date

def parse_play(play):
  time = parse_airdate(play)
  artist = parse_artist(play).encode("utf-8")
  song = parse_song(play).encode("utf-8")
  comment = parse_comment(play).encode("utf-8")
  return {"time": time, "artist": artist, "song": song, "comment": comment}

def parse_airdate(play):
  date = play.find("div", class_="AirDate").span.text
  time = date.split(" ")[0]
  pm = date.split(" ")[1].upper()

  hour = int(time.split(":")[0])
  minute = int(time.split(":")[1])

  if hour == 12 and pm == "AM":
    hour = 0
  elif hour == 12 and pm == "PM":
    hour = 12
  elif pm =="PM":
    hour += 12

  timestamp = "%02d:%02d" % (hour, minute)
  return timestamp

def parse_artist(play):
  div = play.find("div", class_="ArtistName")
  return div.find("a").text

def parse_song(play):
  div = play.find("div", class_="TrackName")
  return div.text

def parse_comment(play):
  comment = play.find("div", class_="CommentText")
  if (comment):
    comment = comment.text
    comment = comment.strip()
    comment = re.sub("[\r\n\t]", "", comment)
    return comment
  else:
    return ""

def parse(html):
  html = open(html).read()
  soup = BeautifulSoup(html, "html.parser")

  plays = soup.find_all("div", "Play")

  songs = []
  for play in plays:
    song = parse_play(play)
    songs.append(song)
  return songs

def print_songs(songs, date):
  for song in songs:
    print date, song["time"]
    print song["artist"]
    print song["song"]
    print

def songs_to_db(db, date, songs):
  for song in songs:
    insert_db(db, date, song)

def setup_db(db):
  cursor = sqlite3.connect(db)
  cursor.text_factory = str
  cursor.execute("CREATE TABLE IF NOT EXISTS plays (date datetime UNIQUE, artist text, song text, comment text);")
  cursor.execute("CREATE TABLE IF NOT EXISTS artists (artist text UNIQUE);")
  cursor.execute("CREATE TABLE IF NOT EXISTS songs (song text, artist text, UNIQUE(song, artist));")
  cursor.commit()
  return cursor

def try_execute(db, sql, args):
  try:
    db.execute(sql, args)
  except sqlite3.IntegrityError:
    pass

def insert_db(db, date, song):
  # time includes hour and minute. second is always "00"
  timestamp = "%s %s:00" % (date, song["time"])

  # set comment to null if not present.
  comment = song["comment"]
  if not comment:
    comment = "null"

  song_name = song["song"]
  artist = song["artist"]

  add_play_sql = 'INSERT INTO plays VALUES(?, ?, ?, ?);'
  add_artist_sql = 'INSERT INTO artists VALUES(?)'
  add_song_sql = 'INSERT INTO songs VALUES(?, ?)'

  try_execute(db, add_play_sql, (timestamp, artist, song_name, comment))
  try_execute(db, add_artist_sql, (artist, ))
  try_execute(db, add_song_sql, (song_name, artist))

  db.commit()

args = parser.parse_args()
songs = parse(args.html)
date = parse_date(args.html)

if args.db:
  db = setup_db(args.db)
  songs_to_db(db, date, songs)

  db.close()
else:
  print_songs(songs, date)
