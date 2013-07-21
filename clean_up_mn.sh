#! /bin/bash
# Clean up mininet
sudo killall -s9 ovsdb-server
sudo killall -s9 ovs-controller
sudo killall -s9 ovs-vsctl
sudo killall -s9 controller
sudo service openvswitch-switch start
