#!/usr/bin/python

from mininet.cli import CLI
from mininet.log import lg
from mininet.node import Node
from mininet.topolib import TreeNet
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Host
from mininet.link import Link
from mininet.node import OVSController
import os
import sys

ifile = sys.argv[1]
ip_addr=[]
for f in open(ifile):
  ip_addr.append(f.strip())

current_working_dir=sys.argv[2]
site_to_fetch=sys.argv[3]
phantomjs_root=sys.argv[4]
automatn_script=sys.argv[5]
#################################
class ProtoTester(Topo):
    def __init__(self):
        # Initialise topology
        Topo.__init__(self)

        # Create switch
        s1 = self.addSwitch('s1')

        # IP for client
        client = self.addHost('client', ip='10.0.1.1', mac='00:00:00:00:00:01')
        self.addLink(client, s1)

        # IPs for sharded servers
        server_list = []
        for i in range(0,len(ip_addr)):
          if i < 8:
            server_list.append(self.addHost('server'+str(i), ip=ip_addr[i], mac='00:00:00:00:00:0'+str(i+2)))
          if i > 7:
            server_list.append(self.addHost('server'+str(i), ip=ip_addr[i], mac='00:00:00:00:00:'+str(i+2)))

          # Add links
          self.addLink(s1, server_list[i])

if __name__ == '__main__':
    lg.setLogLevel( 'info')
    # Configure and start NATted connectivity
    os.system( "killall -q controller" )
    os.system( "killall -q phantomjs" )
    os.system( "/etc/init.d/apache2 stop" )
    os.system( "killall -s9 apache2" )
    topo = ProtoTester()
    net = Mininet(topo=topo, host=Host, link=Link, controller=OVSController)
    net.start()

    # Set /32 netmask and route for client
    client = net.getNodeByName('client')
    client.sendCmd('ifconfig client-eth0 10.0.1.1 netmask 0.0.0.0')
    client.waitOutput()
    client.sendCmd('route add default dev client-eth0')
    client.waitOutput()
   
    # Set /32 netmask and route for all servers
    server_names = ['']*len(ip_addr)
    for i in range(0,len(ip_addr)):
      server_names[i] = net.getNodeByName('server'+str(i))
      server_names[i].sendCmd('ifconfig server'+str(i)+'-eth0 '+ip_addr[i]+' netmask 0.0.0.0');
      server_names[i].waitOutput()
      server_names[i].sendCmd('route add default dev server'+str(i)+'-eth0')   
      server_names[i].waitOutput()
      server_names[i].cmdPrint('apache2ctl -f /etc/apache2/apache2.conf ')
      server_names[i].waitOutput()

    print "*** Hosts are running and can talk to each other"
    print "*** Type 'exit' or control-D to shut down network"

    client.cmdPrint('/usr/sbin/dnsmasq -x /var/run/dnsmasq.pid -7 /etc/dnsmasq.d,.dpkg-dist,.dpkg-old,.dpkg-new -8 /var/dnsmasq.log -k --log-queries --except-interface eth1 &')
    client.waitOutput()
    client.cmdPrint(phantomjs_root+'/phantomjs '+automatn_script+" "+site_to_fetch);
    client.waitOutput()
    CLI( net )
