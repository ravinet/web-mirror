#! /bin/bash
site=$1

#run script to create file to add to /etc/hosts (ips.txt) and create directories according to url paths and fill them with wget objects
python reset_mirror.py $site

#run mininet
python web_mirror_replay.py $site
