#! /bin/bash
if [ $# -lt 5 ]; then
  echo "Usage : Enter site, mirror-folder, phantomJS, hostname"
  exit 5
fi;
site=$1
folder=$2
PHANTOMJS=$3
hostname=$4
cc=$5
rm -rf $folder
rm -rf mirror-folder/$folder
mkdir -p mirror-folder/$folder

#run phantomjs get_info to create file for website with urls+ips
$PHANTOMJS/bin/phantomjs $PHANTOMJS/examples/get_info.js $site > tempgets.txt

#run script to create file to add to /etc/hosts (ips.txt) and create directories according to url paths and fill them with wget objects
if [ $cc == "cubic" ]; then
  python web_mirror_record.py tempgets.txt $folder `pwd` $hostname
else
  echo "Unsupported cc algorithm\n";
  exit 5;
fi
