#!/bin/sh
# launch_env.sh
# navigate to home directory, then to this directory, then execute python script, then back home

#sudo su
#cd /var/www/TA_AdminLTE
#. $env_name/bin/activate
while true; do
  /var/www/TA_AdminLTE/bin/python /var/www/TA_AdminLTE/env_log.py >/dev/null 2>&1
  sleep 5;
done
#echo "I have broken out of the interminably long for loop"
#trap - INT
#sleep 1
#echo "END."
#cd /
