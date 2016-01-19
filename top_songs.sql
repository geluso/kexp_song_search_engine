.mode html
SELECT count(song), song, artist FROM plays WHERE song != "" GROUP BY song, artist ORDER BY count(song) DESC LIMIT 20;
