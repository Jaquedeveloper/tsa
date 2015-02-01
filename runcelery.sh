#!/bin/sh
celery --app=tsa.celery_app:app worker --loglevel=INFO
