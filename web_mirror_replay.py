#!/usr/bin/python

from mininet.cli import CLI
from mininet.log import lg
from mininet.node import Node
from mininet.topolib import TreeNet
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Host
from mininet.link import Link

import os
import sys
#TODO: Read from file or use Python's source command
if (len(sys.argv) == 0):
  ifile = 'serverips.txt'
else:
  c = str(sys.argv[1])
  ifile = c + '/' + c + 'serverips.txt'
ip_addr=[]
for f in open(ifile):
  ip_addr.append(f.strip())
#ip_addr = ['']*4
#ip_addr[0] = '128.30.2.155'
#ip_addr[1] = '74.125.228.4'
#ip_addr[2] = '74.125.228.9'
#ip_addr[3] = '74.125.228.1'

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
    net = Mininet(topo=topo, host=Host, link=Link)
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
      server_names[i].sendCmd('/home/ravinet/start_apache.sh ' + str(i))
      server_names[i].waitOutput()


    print "*** Hosts are running and can talk to each other"
    print "*** Type 'exit' or control-D to shut down network"
    CLI( net )
    os.system( "cp /etc/hosts_original /etc/hosts" )
    for u in range(0, len(ip_addr)):
      os.system( "rm /etc/apache2/apache2" + str(u) + ".conf")
