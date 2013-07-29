#! /bin/bash
if [ $# -lt 5 ]; then
  echo "Usage : Enter site, mirror_folder, phantomjs, vmname, congestion control"
  exit 5
fi;
site=$1
mirror_folder=$2
phantomjs=$3
vmname=$4
cc=$5
rm -rf $mirror_folder
mkdir $mirror_folder

#run phantomjs get_info to create file for website with urls+ips
$phantomjs/bin/phantomjs $phantomjs/examples/get_info.js $site > tempgets.txt

#run script to create directories according to url paths and fill them with wget objects
python web_mirror_record.py tempgets.txt $mirror_folder $vmname $cc
