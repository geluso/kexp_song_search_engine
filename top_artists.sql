.mode html
SELECT count(artist), artist FROM plays WHERE artist != "" AND artist NOT LIKE "%Various Artist%" GROUP BY artist ORDER BY count(artist) DESC LIMIT 20;
