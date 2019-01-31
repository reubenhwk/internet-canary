#!/usr/bin/env gnuplot

set term png medium
set output "output.png"
set style data lines
set datafile separator "|"
plot "< sqlite3 /var/lib/internet-canary/internet-canary.db \"select (time - strftime('%s', 'now', '-2 hours')) / 60 as minute, result from results where minute > 0 and target = 'http://www.google.com' order by time desc limit 25;\""
