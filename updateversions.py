#!/usr/bin/python3

import re
import sys

package = 'gonhang'

if len(sys.argv) == 1:
    print('Please, specify the version from command line!')
    sys.exit(0)

version = sys.argv[1]


def updateFile(fileToUpdate, regPattern, newString):
    newlines = []
    with open(fileToUpdate, 'r') as f:
        for line in f.readlines():
            if re.search(regPattern, line):
                newlines.append(re.sub(regPattern, newString, line))
            else:
                newlines.append(line)

    with open(fileToUpdate, 'w') as f:
        for line in newlines:
            f.write(line)


newVersion = version
pattern = "([0-9].[0-9].[0-9])"

files = ['setup.py', f'{package}/version.py', 'aur/PKGBUILD']

for file in files:
    print(f'Update version in file [{file}]')
    updateFile(file, pattern, newVersion)

print(f'All files was updated with version [{newVersion}]')
