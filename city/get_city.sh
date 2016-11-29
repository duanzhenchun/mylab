#!/bin/bash

curl  https://raw.githubusercontent.com/eduosi/district/master/district-standard.csv | egrep '\t省\t|\t市\t' > city.csv
cat city.csv|awk '{print $1 $2 $3 $6 $7}'
