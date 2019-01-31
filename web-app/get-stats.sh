#!/bin/bash

sqlite3 $1 "select (time - strftime('%s', 'now', '-2 hours')) / 60 as minute, result from results where minute > 0 and target = '$2' order by time desc limit 25;"
