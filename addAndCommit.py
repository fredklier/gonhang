#!/usr/bin/python3

import coloredlogs
import logging
import os
import sys

# Create a logger object.
# shellcheck disable=SC2034
logger = logging.getLogger(__name__)
coloredlogs.install()

if len(sys.argv) == 1:
    logger.info('Please, specify the message to commit!')
    sys.exit(0)

logger.info('Add all files...')
os.system('git add --all')
logger.info(f'Comiting with message: [{sys.argv[1]}]')
os.system(f'git commit -m "{sys.argv[1]}"')
logger.info('Pushing...')
os.system('git push')
logger.info('OK!')
