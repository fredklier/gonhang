#!/usr/bin/python3

import os
import re
import hashlib
from bs4 import BeautifulSoup
import requests
import shutil

url = 'https://pypi.org/project/gonhang/#files'


def updateFile(fileToUpdate, regPattern, newString):
    newContent = []
    with open(fileToUpdate, 'r') as fHandle:
        for l in fHandle.readlines():
            if re.search(regPattern, l):
                newContent.append(f'{newString}\n')
            else:
                newContent.append(l)

    with open(fileToUpdate, 'w') as fHandle:
        for l in newContent:
            fHandle.write(l)


def sha256sum(filename):
    h = hashlib.sha256()
    b = bytearray(128 * 1024)
    mv = memoryview(b)
    with open(filename, 'rb', buffering=0) as f:
        for n in iter(lambda: f.readinto(mv), 0):
            h.update(mv[:n])
    return h.hexdigest()


print('Preparing to submit AUR Package...')
os.chdir('aur/')

print('Get current version...')

pattern = "([0-9]+.[0-9]+.[0-9]+)"
newlines = []
setup_filename = '../setup.py'
version = '0.0'
with open(setup_filename, 'r') as f:
    for line in f.readlines():
        group = re.search(pattern, line)
        if group:
            print('I found version =====> {}'.format(group[0]))
            version = group[0]
            break

print('Update the package with new version...')
os.system("sed -i 's/pkgver=[0-9].[0-9].[0-9]/pkgver={}/g' PKGBUILD".format(version))

print('Make downloads...')
os.system('pip3 download --no-deps --no-binary :all: gonhang')

fileName = f'gonhang-{version}.tar.gz'
hash256 = sha256sum(fileName)
print('Hash 256 is =====> {}'.format(hash256))
print('Updating hash256 in PKGBUILD')
os.system('sed -i s/sha256sums=.*/sha256sums=\({}\)/ PKGBUILD'.format(hash256))
os.remove(fileName)

print('Getting tarball url...')
req = requests.get(url)
soup = BeautifulSoup(req.content, 'html.parser')
links = soup.findAll('a')
tarBallURL = ''
for link in links:
    if f'gonhang-{version}.tar.gz' in link.text:
        tarBallURL = link['href']
        break

print(f'Tarball URL is ===========> {tarBallURL}')
print('Updating tarball URL in PKGBUILD...')

newValue = f"source=(\"{fileName}::{tarBallURL}\")"

updateFile('PKGBUILD', 'source=', newValue)

if os.path.isfile('.SRCINFO'):
    os.remove('.SRCINFO')

if os.path.isfile(f'gonhang-${version}.tar.gz'):
    os.system(f'rm -rfv gonhang-${version}.tar.gz')

if os.path.isdir('src/'):
    os.system('git rm -r -f src/')
    shutil.rmtree('src/')

if os.path.isdir('pkg/'):
    os.system('git rm -r -f pkg/')
    shutil.rmtree('pkg/')

print('Printing .SRCINFO...')
os.system('makepkg --printsrcinfo > .SRCINFO')