#! /bin/bash
if [ $# -lt 4 ]; then
  echo "Usage : Enter site to mirror and mirror destination folder, phantomJS, hostname"
  exit 5
fi;
site=$1
folder=$2
PHANTOMJS=$3
hostname=$4

rm -rf $folder
rm -rf /var/www/$folder
mkdir /var/www/$folder

# Disable Apache's tendency to start on port 80 of host machine
cp ports.conf /etc/apache2/

# Tell Network Manager to shut up
service network-manager stop

# Ensure dnsmasq is running
sudo service dnsmasq status
retcode=$?
if [ $retcode -ne 0 ]; then
  echo "dnsmasq is not running. Exiting"
  exit 5
fi;

# Disable ipv6
sysctl net.ipv6.conf.all.disable_ipv6=1
sysctl net.ipv6.conf.default.disable_ipv6=1
sysctl net.ipv6.conf.lo.disable_ipv6=1

# Kill apache
sudo service apache2 stop
sudo killall -s9 apache2

# Clean up Mininet
sudo ./clean_up_mn.sh
sudo killall -s9 /usr/bin/python

# Modify root folder
sed s/"DocumentRoot \/var\/www"/"DocumentRoot \/var\/www\/$folder"/g default.backup > /etc/apache2/sites-available/default

#run phantomjs get_info to create file for website with urls+ips
$PHANTOMJS/bin/phantomjs $PHANTOMJS/examples/get_info.js $site > tempgets.txt

#run script to create file to add to /etc/hosts (ips.txt) and create directories according to url paths and fill them with wget objects
python web_mirror_record.py tempgets.txt $folder `pwd` $hostname

#run mininet
python web_mirror_replay.py $folder `pwd` $site $PHANTOMJS

#restore apache default
cp default.backup /etc/apache2/sites-available/default
