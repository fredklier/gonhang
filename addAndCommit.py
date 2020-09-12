#!/usr/bin/python3

import os
import sys


if len(sys.argv) == 1:
    logger.info('Please, specify the message to commit!')
    sys.exit(0)

print('Add all files...')
os.system('git add --all')
print(f'Comiting with message: [{sys.argv[1]}]')
os.system(f'git commit -m "{sys.argv[1]}"')
print('Pushing...')
os.system('git push')
print('OK!')
