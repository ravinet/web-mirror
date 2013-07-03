#! /bin/bash
if [ $# -lt 1 ]; then
  echo "Print server number"
  exit
fi;

server_num=$1
APACHE_LOG_DIR='' /usr/sbin/apache2 -f /etc/apache2/apache2$server_num.conf
