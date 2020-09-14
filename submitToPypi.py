#!/usr/bin/python3

import sys
import os

package = 'gonhang'

if len(sys.argv) == 1:
    print('Please, specify the version from command line!')
    sys.exit(0)

version = sys.argv[1]


def removeFiles():
    os.system('rm -rfv dist/')
    os.system('rm -rfv build/')
    os.system(f'rm -rfv {package}.egg-info/')


print('Remove unnecessary files...')
removeFiles()

print('Update README.me....')
os.system('pandoc -r markdown -w plain -o README.me README.md')

print('Update man files...')
os.system('cp gonhang.man gonhang.1')
os.system('gzip -f gonhang.1')

print('Packaging...')
os.system('python3 setup.py sdist bdist_wheel')
print(f'Upload package: {package} version: {version} to pypi.org...')
os.system('python3 -m twine upload dist/*')

print('Clear unnecessary files...')
removeFiles()

print('All right !!!')
