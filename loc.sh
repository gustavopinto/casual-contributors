#!/bin/bash

locs=()

for dir in */
do
  cloc $dir > $dir.loc
  loc=$(cat $dir.loc | grep SUM | awk '{print $5}')
  locs+=($loc)
done

echo ${locs[@]} | tr ' ' ', ' > loc.csv
