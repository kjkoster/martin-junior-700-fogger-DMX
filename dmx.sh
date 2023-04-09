#!/usr/bin/env bash
### BEGIN INIT INFO
# Provides:          dmx
# Required-Start:    $all
# Required-Stop:
# Default-Start:     2 3 4 5
# Default-Stop:
# Short-Description: Controls goffer via DMX
### END INIT INFO

# Quick start-stop-daemon example, derived from Debian /etc/init.d/ssh
set -e

# Must be a valid filename
NAME=dmx
PIDFILE=/var/run/$NAME.pid
#This is the command to be run, give the full pathname
DAEMON=/home/dmx/martin-junior-700-fogger-DMX/rookmachine.py

case "$1" in
  start)
        echo -n "Starting daemon: "$NAME
    start-stop-daemon --start --quiet --pidfile $PIDFILE --exec $DAEMON -- $DAEMON_OPTS
        echo "."
    ;;
  stop)
        echo -n "Stopping daemon: "$NAME
    start-stop-daemon --stop --quiet --oknodo --pidfile $PIDFILE
        echo "."
    ;;
  restart)
        echo -n "Restarting daemon: "$NAME
    start-stop-daemon --stop --quiet --oknodo --retry 30 --pidfile $PIDFILE
    start-stop-daemon --start --quiet --pidfile $PIDFILE --exec $DAEMON -- $DAEMON_OPTS
    echo "."
    ;;

  *)
    echo "Usage: "$1" {start|stop|restart}"
    exit 1
esac

exit 0

