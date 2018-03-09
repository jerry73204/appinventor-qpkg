#!/usr/bin/env python2
import os
import sys
import atexit

# init
qpkg_root = os.path.realpath(sys.argv[1])
pid_file = os.path.realpath(sys.argv[2])
cmd = os.path.join(qpkg_root, 'appengine-java-sdk', 'bin', 'dev_appserver.sh')
war_path = os.path.join(qpkg_root, 'appinventor-bin', 'appengine', 'build', 'war')

# first fork
try:
    pid = os.fork()
except OSError:
    exit(1)

if pid > 0:
    exit()

os.setsid()
os.umask(0)

# second fork
try:
    pid = os.fork()
except OSError:
    exit(1)

if pid > 0:
    exit()

sys.stdout.flush()
sys.stderr.flush()

with open(pid_file, 'w+') as f:
    f.write(str(os.getpgid(os.getpid())))

os.execl('/bin/sh', '-c', cmd, '--address=0.0.0.0', '--port=7777', war_path) # run shell to avoid appengine bugs
