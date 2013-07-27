#! /bin/bash
if [ $# -lt 6 ]; then
  echo "Usage : Enter site, mirror-folder, phantomJS, hostname, path_addition, chromepath"
  exit 5
fi;
site=$1
folder=$2
PHANTOMJS=$3
hostname=$4
path_addition=$5
chromepath=$6
cc=$7
rm -rf $folder
rm -rf /var/www/$folder
mkdir /var/www/$folder

# Clean up Mininet
sudo ./clean_up_mn.sh

# Disable Apache's tendency to start on port 80 of host machine
cp ports.conf /etc/apache2/

# Tell Network Manager to shut up
service network-manager stop

#once dnsmasq is running, move nameservers from /etc/resolv.conf to dnsmasq resolv.conf and add 127.0.0.1 to /etc/resolv.conf
cat '/etc/resolv.conf' | while read line; do
  echo $line 
done

# Disable ipv6
sysctl net.ipv6.conf.all.disable_ipv6=1
sysctl net.ipv6.conf.default.disable_ipv6=1
sysctl net.ipv6.conf.lo.disable_ipv6=1

# Kill apache
sudo service apache2 stop
sudo killall -s9 apache2

# kill dnsmasq first
sudo killall -s9 dnsmasq

# Clean up Mininet
sudo ./clean_up_mn.sh
sudo killall -s9 /usr/bin/python
sudo killall -s9 quic_server
sudo killall -s9 Xvfb
sudo rm -rf /tmp/myprofdir
mkdir /tmp/myprofdir
# Modify root folder
sed s/"DocumentRoot \/var\/www"/"DocumentRoot \/var\/www\/$folder"/g default.backup > /etc/apache2/sites-available/default

#run phantomjs get_info to create file for website with urls+ips
$PHANTOMJS/bin/phantomjs $PHANTOMJS/examples/get_info.js $site > tempgets.txt

#run script to create file to add to /etc/hosts (ips.txt) and create directories according to url paths and fill them with wget objects
if [ $cc == "cubic" ]; then
  python web_mirror_record.py tempgets.txt $folder `pwd` $hostname
elif [ $cc == "quic" ]; then
  python web_mirror_record_quic.py tempgets.txt $folder `pwd` $hostname
else
  echo "Unsupported cc algorithm\n";
  exit 5;
fi

#run mininet
if [ $cc == "cubic" ]; then
  python web_mirror_replay.py $folder `pwd` $site $PHANTOMJS $path_addition $chromepath
elif [ $cc == "quic" ]; then
  python web_mirror_replay_quic.py $folder `pwd` $site $PHANTOMJS $path_addition $chromepath
else
  echo "Unsupported cc algorithm\n";
  exit 5;
fi

#restore apache default
cp default.backup /etc/apache2/sites-available/default

#Be nice, and restore original etc_hosts file
echo -e "127.0.0.1 localhost\n127.0.1.1 $hostname" > /etc/hosts
