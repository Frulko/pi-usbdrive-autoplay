#!/bin/bash

echo 'pi-usbdrive-autoplay - installation...'
# check if running as root
[ `whoami` = root ] || { echo >&2 "Installation script require run as root"; exit 1; }

# check if pip installed
hash pip 2>/dev/null || { echo >&2 "I require pip but it's not installed. Aborting."; exit 1; }

echo '-- step 1: install python dependencies'
pip install -r requirements.txt

echo '-- step 2: install boot service'

SERVICE='pi-usbdrive-autoplay'
CURRENT_PATH=$(pwd)
VAR_TO_FIND='\[PWD\]'
VAR_TO_REPLACE="${CURRENT_PATH//\//\\/}"

cp install/${SERVICE} /etc/init.d/.

sed -i -e "s/$VAR_TO_FIND/$VAR_TO_REPLACE/g" /etc/init.d/${SERVICE}

chmod 0755 /etc/init.d/${SERVICE}
chmod +x /etc/init.d/${SERVICE}

systemctl daemon-reload
systemctl enable ${SERVICE}

echo '-- step 3: check service'

checkSys=$(systemctl status ${SERVICE} | grep loaded)
if [[ $string == *"loaded"* ]]; then
  echo "-- [GOOD] Everything is ok !"
else
  echo "-- [ERROR] The service seems to be not working..."
fi

echo '-- end'