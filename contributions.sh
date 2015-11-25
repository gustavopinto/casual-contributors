#!/bin/bash

for dir in */
do

  > ${dir%/}_ccs.csv
  cd $dir; cp ../contributions.sh .

  git shortlog -sn | grep "     1" | tr " 1 " " " | sed -e 's/^[[:space:]]*//' -e 's/[[:space:]]*$//' > committers.txt
  cat committers.txt | while read line
  do
    #echo $line
    git log -E --author="^${line}\s<(.+)>$" --pretty=format:"%h,%an,%ae,%ai" --shortstat >> ../${dir%/}_ccs.csv
  done

  echo "done with $dir"
  rm committers.txt contributions.sh
  cd ..
done

echo "done!"
