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

echo "title"
cat title | pbcopy
if read_confirm
    echo "description"
    cat description | pbcopy
end
if read_confirm
    echo "details"
    cat details | pbcopy
end
if read_confirm
    echo "notes"
    cat notes | pbcopy
end
if read_confirm
    echo "scoring"
    cat scoring | pbcopy
end
if read_confirm
    echo "hints"
    cat hints
end