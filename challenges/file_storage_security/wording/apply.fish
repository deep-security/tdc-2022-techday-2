#!/usr/bin/env fish
function read_confirm
  while true
    read -l -P 'Do you want to continue? [y/N] ' confirm

    switch $confirm
      case Y y
        return 0
      case '' N n
        return 1
    end
  end
end

function apply
    cd target/$argv
    echo "title"
    cat title | pbcopy
    if read_confirm
        echo "description"
        cat description | pbcopy
    else
        return 1
    end
    if read_confirm
        echo "details"
        cat details | pbcopy
    else
        return 1
    end
    if read_confirm
        echo "notes"
        cat notes | pbcopy
    else
        return 1
    end
    if read_confirm
        echo "scoring"
        cat scoring | pbcopy
    else
        return 1
    end
    if read_confirm
        echo "hints"
        cat hints
    else
        return 1
    end
    cd ../..
end
