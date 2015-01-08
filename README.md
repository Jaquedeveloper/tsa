tsa
===

Twitter live capture and Sentiment Analysis

Installation

sudo apt-get git supervisor nginx nano python-virtualenv<br/>
sudo groupadd --system webapps<br/>
sudo mkdir -p /webapps/tsa<br/>
sudo useradd --system --gid webapps --shell /bin/bash --home /webapps/tsa tsa<br/>
sudo chown tsa /webapps/tsa<br/>
sudo su - tsa<br/>
virtualenv ve<br/>
source ve/bin/activate<br/>
git clone https://github.com/joker-ace/tsa.git<br/>
pip install -r tsa/requirements.txt<br/>
mkdir logs<br/>
touch /webapps/tsa/logs/gunicorn_supervisor.log<br/>
chmod +x /webapps/tsa/install/install.sh
./webapps/tsa/install/install.sh