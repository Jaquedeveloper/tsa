#!/bin/bash
 
NAME="tsa"                                  			# Name of the application
DJANGODIR=/webapps/tsa/dveri         			# Django project directory
SOCKFILE=/webapps/tsa/run/gunicorn.sock  # we will communicte using this unix socket
LOGFILE=/webapps/tsa/logs/gunicorn.log
USER=tsa 			                                        # the user to run as
GROUP=webapps                                     			# the group to run as
NUM_WORKERS=2                                     			# how many worker processes should Gunicorn spawn
DJANGO_SETTINGS_MODULE=settings             				# which settings file should Django use
DJANGO_WSGI_MODULE=tsa.wsgi                     			# WSGI module name
 
echo "Starting $NAME as `whoami`"
 
# Activate the virtual environment
cd $DJANGODIR
source ../.ve/bin/activate
export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
export PYTHONPATH=$DJANGODIR:$PYTHONPATH

# Create the run directory if it doesn't exist
RUNDIR=$(dirname $SOCKFILE)
test -d $RUNDIR || mkdir -p $RUNDIR

# Create the log directory if it doesn't exist
LOGDIR=$(dirname $LOGFILE)
test -d $LOGDIR || mkdir -p $LOGDIR

# Start your Django Unicorn
# Programs meant to be run under supervisor should not daemonize themselves (do not use --daemon)
exec ../.ve/bin/gunicorn ${DJANGO_WSGI_MODULE}:application \
  --name $NAME \
  --workers $NUM_WORKERS \
  --user=$USER --group=$GROUP \
  --bind=unix:$SOCKFILE \
  --log-level=debug \
  --log-file=$LOGFILE