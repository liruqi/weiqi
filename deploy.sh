#!/bin/bash

set -e

if [ $# -ne 2 ]; then
    echo "Usage: $0 <target-host> <target-path>"
    exit 1
fi

HOST=$1
PATH=$2

echo "Deploying weiqi.gs ..."

/usr/bin/ssh -t ${HOST} <<EOF
cd ${PATH}
sudo supervisorctl stop weiqi
git fetch --all
git reset --hard origin/master
python3 -m venv venv
source venv/bin/activate
pip install --upgrade -r requirements.txt
npm install
node_modules/.bin/gulp build --production
export WEIQI_SETTINGS=\$HOME/settings.py
alembic upgrade head
sudo supervisorctl start weiqi
EOF
