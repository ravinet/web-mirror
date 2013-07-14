#! /bin/bash
if [ $# -lt 2 ]; then
  echo "Usage : Enter site to mirror and mirror destination folder"
  exit 5
fi;
PHANTOMJS=/home/skype-alpha/July3rdGoogleMeeting/phantomjs/
site=$1
folder=$2
rm -rf $folder
rm -rf /var/www/$folder
mkdir /var/www/$folder

# Clean up Mininet
sudo ./clean_up_mn.sh

# kill apache
sudo service apache2 stop
sudo killall -s9 apache2
sudo killall -s9 /usr/bin/python

Modify root folder
cd /etc/apache2/sites-available
sed s/"DocumentRoot \/var\/www"/"DocumentRoot \/var\/www\/$folder"/g default.backup > default
cd -


##run phantomjs get_info to create file for website with urls+ips
$PHANTOMJS/bin/phantomjs $PHANTOMJS/examples/get_info.js $site > tempgets.txt
#
##run script to create file to add to /etc/hosts (ips.txt) and create directories according to url paths and fill them with wget objects
python web_mirror_record.py tempgets.txt $folder `pwd`
#sleep 1
#run mininet
python web_mirror_replay.py $folder `pwd` $site $PHANTOMJS

# restore
cd /etc/apache2/sites-available
cp default.backup default
cd -
