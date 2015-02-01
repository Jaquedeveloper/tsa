#!/bin/sh

cd ~
cp /webapps/tsa/tsa/install/gunicorn_start.sh /webapps/tsa/bin/gunicorn_start.sh
chmod +x /webapps/tsa/bin/gunicorn_start.sh
cp /webapps/tsa/tsa/install/celery_start.sh /webapps/tsa/bin/celery_start.sh
chmod +x /webapps/tsa/bin/celery_start.sh
cp /webapps/tsa/tsa/install/tsa.supervisor.conf /etc/supervisor/conf.d/tsa.supervisor.conf
cp /webapps/tsa/tsa/install/tsa_celery.supervisor.conf /etc/supervisor/conf.d/tsa_celery.supervisor.conf
cp /webapps/tsa/tsa/install/tsa.nginx.conf /etc/nginx/sites-available/tsa.nginx.conf
sudo ln -s /etc/nginx/sites-available/tsa.nginx.conf /etc/nginx/sites-enabled/tsa.nginx.conf
sudo rm /etc/nginx/sites-enabled/default
sudo service nginx restart
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl restart tsa
sudo supervisorctl restart tsa_celery
