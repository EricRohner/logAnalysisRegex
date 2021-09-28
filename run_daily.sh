#!/bin/bash

./ticky_check.py syslog.log
./csv_to_html.py Errors.csv ~/gcert/logAnalysisRegex/www/Errors.html
./csv_to_html.py Users.csv ~/gcert/logAnalysisRegex/www/Users.html
