#!/usr/bin/python3
import sys
import os

package = 'gonhang'


def removeFiles():
    os.system('rm -rfv ~/rpmbuild')


if len(sys.argv) == 1:
    print('Please, specify the version from command line!')
    sys.exit(0)

version = sys.argv[1]

print('Remove unnecessary files....')
removeFiles()

print(f'Download package {package} version: {version}')
os.system('pyp2rpm -srpm gonhang')

print('Build RPM....')
cmdToBuild = f'rpmbuild -ba --sign rpmbuild/{package}.spec'
os.system(cmdToBuild)

print('Upload to Copr....')
cmd = f'copr-cli build gonhang /root/rpmbuild/SRPMS/{package}-{version}-1.fc32.src.rpm'
os.system(cmd)

removeFiles()

print('Update Repository.....')
os.system('git add --all')
msg = f'copr package {package} version: {version} was released!'
print(f'Comiting changes with message: {msg}')
os.system(f'git commit -m "{msg}"')
print('Pushing...')
os.system('git push')
print('OK!')
