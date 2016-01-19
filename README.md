# KSSE: KEXP Song Search Engine
A website dedicated to searching through the entire history of KEXP radio.

See the project live at:
http://5tephen.com/ksse/index.php

This project scrapes the online KEXP hourly playlist and builds a database recording
what songs are played at what time. The project consists of a scraper, parser, and database tool.
Each component of the project is configured to behave like a command line tool and act independantly.

## scraper.py
python scraper.py 2007

The scraper accepts a year as an argument and will use curl to download all hourly playlist pages for all of 2007.
These pages are saved as pure HTML in the current directory.

## parse.py
python parse.py 2007-01-01-00.html kexp.db

The parse utility accepts one HTML page and parses out date, song, artist and DJ comments information.
This information is stored in the database provided as the second argument. This utility only parses one
hourly playlist file at a time. The year shell script can be used to invoke this script for all the files
in a year.

## proximity.py
python proximity.py --db kexp.db --song "Say It Ain't So" --artist "Weezer" --comments True --nearness 5 --limit 30 --original True

This database tool is the core of the search engine. It accepts a database and search paramenters.
Users can search for only a song, only an artist, or both a song and an artist. The search can be
configured to show or hide DJ comments, which are sometimes annotated with a song.

The --limit parameter limits the total number of search results.

The --nearness parameter expands a search to return songs played nearly before and after the song or
artist being searched for. Nearness is measured in minutes. Nearness of zero returns only the
song/artist being searched for. Nearness of 5 returns songs played fives minutes before, and five
minutes after the song being searched for.

The --original parameter either allows or prevents the target search song from being shown. If a user
wants to see when one song has been played --original should be true. If a user is interested in finding
new songs played near a song they know --original should be false. If a user wasnts to see how songs are
played in relation to the song their searching for --original should be true.

