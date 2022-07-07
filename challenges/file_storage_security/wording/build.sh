#!/usr/bin/env bash
for i in $(seq -f %02g 10)
do
    for file in $(eval echo src/task$i.md)
    do
        DESTINATION=$(echo $file | sd "src" "target" | sd ".md" "")
        csplit --prefix='task' --suffix-format='%03d.md' $file /\#\#/ "{*}"  
        mv task000.md  $DESTINATION/title
        sd "# Task" "FSS Task" $DESTINATION/title
        pandoc --wrap=preserve --to plain task001.md > $DESTINATION/description
        pandoc --wrap=preserve --to plain task002.md > $DESTINATION/details
        pandoc --wrap=preserve --to plain task003.md > $DESTINATION/notes
        pandoc --wrap=preserve --to plain task004.md > $DESTINATION/scoring
        cat task005.md task006.md task007.md task008.md > $DESTINATION/hints
        sed -i "1,2d" $DESTINATION/{description,details,notes,scoring}
        rm task*.md
    done
done
