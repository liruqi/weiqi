#!/bin/bash

set -e

if [ $# -ne 2 ]; then
    echo "Usage: $0 <target-host> <target-path>"
    exit 1
fi

HOST=$1
PATH=$2

echo "Runnng tests ..."
venv/bin/py.test --benchmark-skip -n8 weiqi || exit 1

echo "Merging to production branch ..."
export GIT_SSH=/usr/bin/ssh
/usr/bin/git checkout prod
/usr/bin/git merge master
/usr/bin/git push
/usr/bin/git checkout master

echo "Deploying weiqi.gs ..."

/usr/bin/ssh -t ${HOST} <<EOF
cd ${PATH}
git fetch --all
git reset --hard origin/prod

python3 -m venv venv
source venv/bin/activate
pip install --upgrade -r requirements.txt
npm install

node_modules/.bin/gulp build --production

sudo supervisorctl stop weiqi:\*

export WEIQI_SETTINGS=\$HOME/settings.py
alembic upgrade head
./main.py --prepare-startup

sudo supervisorctl start weiqi:\*
EOF
