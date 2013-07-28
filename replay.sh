#! /bin/bash
# Replay script for mininet

if [ $# -ne 5 ]; then
  echo "Enter hostmapping file, and mirror folder, mininet cfg phantomjs, automation script"
  exit 5;
fi

# Exterminate old versions of Mininet
./clean_up_mn.sh

# Kill old residues
sudo killall -s9 /usr/bin/python
sudo killall -s9 quic_server
sudo killall -s9 Xvfb
sudo killall -s9 dnsmasq
sudo service apache2 stop
sudo killall -s9 apache2

# cmdline args
hostmapping=$1
mirror_folder=$2
server_ips=$3
phantomjs=$4
automatn_script=$5

site_to_fetch="http://$mirror_folder"

# Rewrite /etc/hosts
scp $hostmapping /etc/hosts

# Copy mirrored folder to resting place
scp -r $mirror_folder /var/www

# Modify Apache Root
sed s/"DocumentRoot \/var\/www"/"DocumentRoot \/var\/www\/$folder"/g default.backup > /etc/apache2/sites-available/default

# Run Mininet
scp $server_ips server_ips.txt
python web_mirror_replay.py server_ips.txt `pwd` $site_to_fetch $phantomjs $automatn_script

# Restore etc hosts
cp hosts_default /etc/hosts

# Restore apache default file
cp default.backup /etc/apache2/sites-available/default
