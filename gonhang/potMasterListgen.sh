#!/bin/bash

find . -type f \( -name '*.py' \)  -print > list
xgettext --keyword=_  --add-comments --language=Python --sort-output -o gonhang.pot --files-from=list