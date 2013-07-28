#! /bin/bash
# Replay script for mininet

if [ $# -ne 5 ]; then
  echo "Enter hostmapping file, and mirror folder, mininet cfg phantomjs, automation script"
  exit 5;
fi

# Exterminate old versions of Mininet
./clean_up_mn.sh

# cmdline args
hostmapping=$1
mirror_folder=$2
server_ips=$3
phantomjs=$4
automatn_script=$5

site_to_fetch="http://$mirror_folder"

# Rewrite /etc/hosts
cp $hostmapping /etc/hosts

# Copy mirrored folder to resting place
cp -r $mirror_folder /var/www

# Modify Apache Root
sed s/"DocumentRoot \/var\/www"/"DocumentRoot \/var\/www\/$folder"/g default.backup > /etc/apache2/sites-available/default

# Run Mininet
python web_mirror_replay.py $server_ips `pwd` $site_to_fetch $phantomjs $automatn_script

# Restore etc hosts
cp hosts_default /etc/hosts

# Restore apache default file
cp default.backup /etc/apache2/sites-available/default
