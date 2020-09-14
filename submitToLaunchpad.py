#!/usr/bin/python3
import sys
import os

package = 'gonhang'

if len(sys.argv) == 1:
    print('Please, specify the version from command line!')
    sys.exit(0)

version = sys.argv[1]

print('Building de package....')
os.system('debuild -k97F85643068753880DAA9FAD404BF2FE939FCCE3 -S')

print('Upload to Launchpad....')
dputCmd = f'dput ppa:fredcox-p/{package} ../{package}_{version}_source.changes'
os.system(dputCmd)

print('Clearing unnecessary files....')
os.system(f'rm -rfv ../{package}_{version}*')

print('Update Repository.....')
os.system('git add --all')
msg = f'debian package {package} version: {version} was released!'
print(f'Comiting changes with message: {msg}')
os.system(f'git commit -m "{msg}"')
print('Pushing...')
os.system('git push')
print('OK!')

