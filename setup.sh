sudo apt-get update
sudo apt install python3-pip unzip chromium-browser xvfb -y

export LC_ALL=C

pip3 install virtualenv
pip3 install awscli --upgrade --user

git clone https://github.com/pranet/projectZ.git
cd projectZ
cd resources
wget https://chromedriver.storage.googleapis.com/2.38/chromedriver_linux64.zip
unzip chromedriver_linux64.zip
rm chromedriver_linux64.zip
aws s3 cp s3://pranet-projectz/resources/application.properties .
cd ..

virtualenv -p python3 venv
source venv/bin/activate
pip install -r requirements.txt
export ENVIRONMENT=PRODUCTION
tmux
python entry_point.py