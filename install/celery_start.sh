#!/bin/bash

DJANGODIR=/webapps/tsa/tsa              # Django project directory
# Activate the virtual environment
cd $DJANGODIR
source ../bin/activate
exec celery --app=tsa.celery_app:app worker --loglevel=INFO