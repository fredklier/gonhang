#!/usr/bin/python3
import sys
import os

if len(sys.argv) == 1:
    print('Please, specify the version from command line!')
    sys.exit(0)

version = sys.argv[1]
cmd = f'copr-cli build gonhang /root/rpmbuild/SRPMS/gonhang-{version}-1.fc32.src.rpm'
os.system(cmd)
