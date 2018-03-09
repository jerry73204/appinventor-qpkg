#!/bin/sh
CONF=/etc/config/qpkg.conf
QPKG_NAME="appinventor"
QPKG_ROOT=`/sbin/getcfg $QPKG_NAME Install_Path -f ${CONF}`
APACHE_ROOT=/share/`/sbin/getcfg SHARE_DEF defWeb -d Qweb -f /etc/config/def_share.info`
APPINVENTOR_SCRIPT=$QPKG_ROOT/run_appinventor.py
BUILDSERVER_SCRIPT=$QPKG_ROOT/run_buildserver.py
APPINVENTOR_PID_FILE=$QPKG_ROOT/appinventor.pid
BUILDSERVER_PID_FILE=$QPKG_ROOT/buildserver.pid

case "$1" in
    start)
        ENABLED=$(/sbin/getcfg $QPKG_NAME Enable -u -d FALSE -f $CONF)
        if [ "$ENABLED" != "TRUE" ]; then
            echo "$QPKG_NAME is disabled."
            exit 1
        fi

        echo "Starting MIT AppInventor"

        if [ -f $APPINVENTOR_PID_FILE -o -f $BUILDSERVER_PID_FILE ]; then
            echo "Another instance is running. Please stop it first."
            exit 1
        fi

        env PATH=$PATH:/usr/local/jre/bin python2 $APPINVENTOR_SCRIPT $QPKG_ROOT $APPINVENTOR_PID_FILE 2>&1
        env PATH=$PATH:/usr/local/jre/bin python2 $BUILDSERVER_SCRIPT $QPKG_ROOT $BUILDSERVER_PID_FILE 2>&1
        ;;

    stop)
        echo "Shutting down MIT AppInventor service"

        if [ -f $APPINVENTOR_PID_FILE ]; then
            PGID=`cat $APPINVENTOR_PID_FILE`
            python2 -c $'import os\nimport signal\nos.killpg('"$PGID"', signal.SIGTERM)'
            rm $APPINVENTOR_PID_FILE
        fi

        if [ -f $BUILDSERVER_PID_FILE ]; then
            PGID=`cat $BUILDSERVER_PID_FILE`
            python2 -c $'import os\nimport signal\nos.killpg('"$PGID"', signal.SIGTERM)'
            rm $BUILDSERVER_PID_FILE
        fi
        ;;

    restart)
        $0 stop
        $0 start
        ;;

    *)
        echo "Usage: $0 {start|stop|restart}"
        exit 1
esac

exit 0
