tsa
===

Twitter live capture and Sentiment Analysis

Installation

apt-get git supervisor nginx nano python-virtualenv<br/>
sudo groupadd --system webapps
sudo mkdir -p /webapps/tsa
sudo useradd --system --gid webapps --shell /bin/bash --home /webapps/tsa tsa
sudo chown tsa /webapps/tsa
sudo su - tsa
virtualenv ve
source ve/bin/activate
git clone https://github.com/joker-ace/tsa.git
pip install -r tsa/requirements.txt
mkdir logs
touch /webapps/tsa/logs/gunicorn_supervisor.log