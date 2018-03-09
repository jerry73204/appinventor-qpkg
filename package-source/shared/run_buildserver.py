#!/usr/bin/env python2
import os
import sys
import atexit

qpkg_root = os.path.realpath(sys.argv[1])
pid_file = os.path.realpath(sys.argv[2])
appinventor_path = os.path.join(qpkg_root, 'appinventor-bin')

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

libs = ['buildserver/build/run/lib/BuildServer.jar',
        'buildserver/build/run/lib/CommonUtils.jar',
        'buildserver/build/run/lib/CommonVersion.jar',
        'buildserver/build/run/lib/FastInfoset-1.2.2.jar',
        'buildserver/build/run/lib/activation-1.1.jar',
        'buildserver/build/run/lib/args4j-2.0.18.jar',
        'buildserver/build/run/lib/asm-3.1.jar',
        'buildserver/build/run/lib/bcpkix-jdk15on-149.jar',
        'buildserver/build/run/lib/bcprov-jdk15on-149.jar',
        'buildserver/build/run/lib/commons-io-2.0.1.jar',
        'buildserver/build/run/lib/grizzly-servlet-webserver-1.9.18-i.jar',
        'buildserver/build/run/lib/guava-14.0.1.jar',
        'buildserver/build/run/lib/http-20070405.jar',
        'buildserver/build/run/lib/jackson-core-asl-1.9.4.jar',
        'buildserver/build/run/lib/jaxb-api-2.1.jar',
        'buildserver/build/run/lib/jaxb-impl-2.1.10.jar',
        'buildserver/build/run/lib/jaxb-xjc.jar',
        'buildserver/build/run/lib/jdom-1.0.jar',
        'buildserver/build/run/lib/jersey-bundle-1.3.jar',
        'buildserver/build/run/lib/jersey-multipart-1.3.jar',
        'buildserver/build/run/lib/jettison-1.1.jar',
        'buildserver/build/run/lib/json.jar',
        'buildserver/build/run/lib/jsr311-api-1.1.1.jar',
        'buildserver/build/run/lib/localizer.jar',
        'buildserver/build/run/lib/mail-1.4.jar',
        'buildserver/build/run/lib/rome-0.9.jar',
        'buildserver/build/run/lib/sdklib.jar',
        'buildserver/build/run/lib/stax-api-1.0-2.jar',
        'buildserver/build/run/lib/wadl-cmdline.jar',
        'buildserver/build/run/lib/wadl-core.jar',
        'buildserver/build/run/lib/wadl2java.jar']

classpath = ':'.join(os.path.join(qpkg_root, 'appinventor-bin', path) for path in libs)

cmd = ['java',
       '-Dfile.encoding=UTF-8',
       '-classpath',
       classpath,
       'com.google.appinventor.buildserver.BuildServer',
       '--dexCacheDir',
       os.path.join(qpkg_root, 'appinventor-bin', 'build/buildserver/dexCache'),
       '--shutdownToken',
       'token']

os.execlp(*cmd)
