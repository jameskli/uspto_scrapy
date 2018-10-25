#!/bin/bash
for filename in data/urls*; do
    echo $filename
    base_name=$(basename -- "$filename")
    scrapy crawl uspto -a filename=$filename
    if [ $? -eq 0 ]
    then
        mv results/results.csv "results/result_$base_name"
        mv $filename "data-finished/$base_name"
    else
        echo "Error with $filename"
        mv results/results.csv "results/error_$base_name"
        mv $filename "data-error/$base_name"
    fi

done