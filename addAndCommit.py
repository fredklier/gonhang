#!/usr/bin/python3

import os
import sys


if len(sys.argv) == 1:
    print('Please, specify the message to commit!')
    sys.exit(0)

print('Add all files...')
os.system('git add --all')
print(f'Comiting changes with message: [{sys.argv[1]}]')
os.system(f'git commit -m "{sys.argv[1]}"')
print('Pushing...')
os.system('git push')
print('OK!')
