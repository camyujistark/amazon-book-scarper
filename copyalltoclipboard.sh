#!/bin/bash

query=$1
declare -a array=(".name" ".url" ".author" ".image" ".published" ".product_index");

for element in "${array[@]}"
do
  sleep .3;
  # -r means raw output. remove double quotes
  echo "$query" | /usr/local/bin/jq -r "$element" | pbcopy;
done
