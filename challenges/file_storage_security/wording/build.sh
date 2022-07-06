#!/usr/bin/env bash
for i in $(seq -f %02g 10)
do
    for file in $(eval echo src/task$i/main.md)
    do
        DESTINATION=$(dirname $(echo $file | sd "src" "target"))
        csplit --prefix='task' --suffix-format='%03d.md' $file /\#\#/ "{*}"  
        mv task000.md  $DESTINATION/title
        sd "# Task" "FSS Task" $DESTINATION/title
        pandoc --wrap=preserve task001.md > $DESTINATION/description
        pandoc --wrap=preserve task002.md > $DESTINATION/details
        pandoc --wrap=preserve task003.md > $DESTINATION/notes
        pandoc --wrap=preserve task004.md > $DESTINATION/scoring
        cat task005.md task006.md task007.md task008.md > $DESTINATION/hints
        sd "</*p>" "" $DESTINATION/*
        sed -i "1d" $DESTINATION/{description,details,notes,scoring}
        rm task*.md
    done
done
