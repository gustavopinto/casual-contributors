#!/bin/bash

ROOT=`pwd`

for dir in */
do
    cd "$dir"
    git shortlog -s > temp #--since=1.year
    output=$ROOT/${dir%/}.csv
    cat temp | awk '{print $1}' ORS=',' > $output
    rm temp
    echo "done with $ROOT/$dir"
    cd ..
done

rm alltogether.csv
cat *.csv > alltogether.csv

echo "Done!"
