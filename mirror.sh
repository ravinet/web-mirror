#! /bin/bash
set -x
set -v
site=$1
folder=$2
rm -rf $folder
rm -rf /var/www/$folder
mkdir /var/www/$folder

# kill apache
sudo service apache2 stop
sudo killall -s9 apache

# Modify root folder
cd /etc/apache2/sites-available
sed s/"DocumentRoot \/var\/www"/"DocumentRoot \/var\/www\/$folder"/g default.backup > default
cd -


##run phantomjs get_info to create file for website with urls+ips
/home/ravinet/testphantomJS/phantomjs/bin/phantomjs /home/ravinet/testphantomJS/phantomjs/examples/get_info.js $site > tempgets.txt
#
##run script to create file to add to /etc/hosts (ips.txt) and create directories according to url paths and fill them with wget objects
python web_mirror_record.py tempgets.txt $folder
#sleep 1
#run mininet
python web_mirror.py $folder

# restore
cp default.backup default
