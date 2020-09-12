#!/bin/bash

rm -rfv dist/
rm -rfv build/
rm -rfv gonhang.egg-info/

pandoc -r markdown -w plain -o README.me README.md
cp gonhang.man gonhang.1
gzip -f gonhang.1

python3 setup.py sdist bdist_wheel
python3 -m twine upload dist/*


rm -rfv dist/
rm -rfv build/
rm -rfv gonhang.egg-info/
