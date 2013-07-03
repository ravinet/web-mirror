import shutil
import sys
fold = str(sys.argv[1])
f = open('/etc/hosts', 'w')
f.write('127.0.0.1       localhost\n128.30.76.203   copley.csail.mit.edu    copley\n \n')
val = fold+'/' + fold + 'ips.txt'
apacval = fold + '/' + fold + 'serverips.txt'
for entry in open(val):
  f.write(entry)
f.write('\n\n# The following lines are desirable for IPv6 capable hosts\n::1     ip6-localhost ip6-loopback\nfe00::0 ip6-localnet\nff00::0 ip6-mcastprefix\nff02::1 ip6-allnodes\nff02::2 ip6-allrouters')
f.close()
count = 0
for entry in open(apacval):
  fname = '/etc/apache2/apache2' + str(count) + '.conf'
  #t = open('/etc/apache2/apache2' + str(count) + 'conf', 'w')
  #t.close()
  shutil.copy('/etc/apache2/apache2.conf', fname)
  count = count + 1
  apac = open(fname, 'a')
  apac.write('\nListen ' + str(entry.strip()) + ':80')
  apac.close()

