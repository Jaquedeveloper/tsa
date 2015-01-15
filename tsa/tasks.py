from __future__ import absolute_import

from tsa.celery import app

@app.task
def run_query():
    pass