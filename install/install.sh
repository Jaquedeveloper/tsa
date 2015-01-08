#!/bin/sh

cd ~
cp /webapps/tsa/tsa/install/gunicorn_start.sh /webapps/tsa/bin/gunicorn_start.sh
chmod +x /webapps/tsa/bin/gunicorn_start.sh
cp /webapps/tsa/tsa/install/tsa.supervisor.conf /etc/supervisor/conf.d/tsa.supervisor.conf
sudo supervisorctl reread
sudo supervisorctl update
status tsa

cp /webapps/tsa/tsa/install/tsa.nginx.conf /etc/nginx/sites-available/tsa.nginx.conf
sudo ln -s /etc/nginx/sites-available/tsa.nginx.conf /etc/nginx/sites-enabled/tsa.nginx.conf
sudo service nginx restart