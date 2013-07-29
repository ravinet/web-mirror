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

sharded_servers = sys.argv[1]
ip_addr=[]
for server in open(sharded_servers):
  ip_addr.append(server.strip())

site_to_fetch=sys.argv[2]
phantomjs=sys.argv[3]
quic_path=sys.argv[4]
cc=sys.argv[5]
browser=sys.argv[6]

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
    os.system( "killall -s9 quic_server" )
    os.system( "rm -rf /home/vagrant/prof" )
    topo = ProtoTester()
    net = Mininet(topo=topo, host=Host, link=Link, controller=OVSController)
    net.start()

    # Set /32 netmask and route for client
    client = net.getNodeByName('client')
    client.sendCmd('ifconfig client-eth0 10.0.1.1 netmask 0.0.0.0')
    client.waitOutput()
    client.sendCmd('route add default dev client-eth0')
    client.waitOutput()
   
    # Set /32 netmask and route for all serversi
    
    server_names = ['']*len(ip_addr)
    for i in range(0,len(ip_addr)):
      server_names[i] = net.getNodeByName('server'+str(i))
      server_names[i].sendCmd('ifconfig server'+str(i)+'-eth0 '+ip_addr[i]+' netmask 0.0.0.0');
      server_names[i].waitOutput()
      server_names[i].sendCmd('route add default dev server'+str(i)+'-eth0')   
      server_names[i].waitOutput()
      if cc == 'cubic':
        server_names[i].cmdPrint('apache2ctl -f /etc/apache2/apache2.conf ')
      elif cc == 'quic':
        server_names[i].cmdPrint('nohup ' + quic_path + ' --quic_in_memory_cache_dir0=' + quic_path + '/' + site_to_fetch + ' --port=80 --ip=' + ip_addr[i] + ' > /tmp/quic_server' + str(i)+'.stdout 2> /tmp/quic_server' + str(i) +'.stderr &')
      else:
        exit(5) 
      server_names[i].waitOutput()        

    print "*** Hosts are running and can talk to each other"
    print "*** Type 'exit' or control-D to shut down network"

    client.cmdPrint('/usr/sbin/dnsmasq -x /var/run/dnsmasq.pid -7 /etc/dnsmasq.d,.dpkg-dist,.dpkg-old,.dpkg-new -8 /var/dnsmasq.log -k --log-queries --except-interface eth1 &')
    client.waitOutput()
    if cc == 'cubic':
      if browser == 'phantomjs':
        client.cmdPrint(phantomjs+'/bin/phantomjs '+ phantomjs_root + "/examples/loadspeed.js " +site_to_fetch);
      elif browser == 'chrome':
        client.cmdPrint('su vagrant -c"python load_google.py"')
      else:
        exit(5)
      client.waitOutput()
    elif cc == 'quic':
      client.cmdPrint('su vagrant -c"python load_google.py"')
    else:
      exit(5)
    CLI( net )
