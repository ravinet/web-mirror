import sys
import os
import shutil
#apac = open('etc/apache2/apache2.conf', 'a')
# file name with gets and ips
getinfo = sys.argv[1]
print getinfo

# root folder to save in
mirror_root = sys.argv[2]

# working directory
working_dir = sys.argv[3]

# keep track of distinct IPs in gets file for etc/hosts
ips = []
host_mapping = open('ips.txt', 'w')

# File with list of IPs for Mininet setup
mininet_cfg  = open('serverips.txt','w')

# Number of distinct IPs
count = 0

mirror_path = '/var/www/' + str(mirror_root)

# remove old vestiges
os.system("rm -rf "+mirror_path);

# Parse gets.txt
for line in open(getinfo):
  records          = line.split(' ')
  scheme_plus_url  = records[0]
  ip = records[1]

  domain_name     = ''
  resource_folder = ''
  if 'https' in scheme_plus_url:
    domain_name      = scheme_plus_url.split('https://')[1].split('/')[0]
    resource_folders = scheme_plus_url.split('https://')[1].split('/')
  elif 'http' in scheme_plus_url:
    domain_name      = scheme_plus_url.split('http://')[1].split('/')[0]
    resource_folders = scheme_plus_url.split('http://')[1].split('/')
  else :
    print "Die here. Found non HTTP/HTTPS"
    exit(5)

  print "Domain name", domain_name
  print "resource_folders", resource_folders

  if ip not in ips:
    # Saw distinct IP
    ips.append(ip)

    # Add to host mapping file for DNS
    host_mapping.write(str(ip.strip()) + ' ' + domain_name + '\n')

    # Add to list of IPs for Mininet
    mininet_cfg.write(str(ip.strip()) + '\n')

    # Create conf file for sharded server
    apache_conf_filename = '/etc/apache2/apache2' + str(count) + '.conf'
    shutil.copy('/etc/apache2/apache2.conf', apache_conf_filename)
    count = count + 1
    apache_conf_fh = open(apache_conf_filename, 'a')
    apache_conf_fh.write('\nListen ' + str(ip.strip()) + ':80')
    apache_conf_fh.close()

  #directories to be made for wget
  resource_directory = mirror_path
  for i in range(1, len(resource_folders)-1):
    # start from 1 because 0 is hostname
    # end at -1 because the last entry is the file itself
    resource_directory = resource_directory + '/' + resource_folders[i]

  print "resource_directory",resource_directory

  # Create directory for resource if it doesn't exist
  if not os.path.exists(resource_directory):
    os.makedirs(resource_directory)

  # Change directory to copy resource into it's final resting place
  os.chdir(resource_directory)

  # Get name of resource
  resource_name = resource_folders[-1]

  # Get rid of query parameters
  resource_name = resource_name.split('?')[0]
  print "resource_name",resource_name

  # Reconstruct URL for fetching
  url_records = scheme_plus_url.split('/')
  
  # Concatenate all except the last record
  fetch_url = ''
  for record in url_records[:-1] :
    fetch_url += record+'/'
  fetch_url += resource_name

  print "fetch_url",fetch_url,"\n"

  # Finally, fetch resource using wget
  os.system("wget \"" + str(fetch_url) + "\"")

  # Change directory back to original directory
  os.chdir(working_dir)

# Close Mininet Config 
mininet_cfg.close()
host_mapping.close()

# Concatenate to /etc/hosts
dns_mapping = open('/etc/hosts', 'w')
dns_mapping.write('127.0.0.1       localhost\n128.30.76.203   copley.csail.mit.edu    copley\n 127.0.1.1 skypealpha-ThinkCentre-M91p \n')
for entry in open('ips.txt'):
  dns_mapping.write(entry)

dns_mapping.write('\n\n# The following lines are desirable for IPv6 capable hosts\n::1     ip6-localhost ip6-loopback\nfe00::0 ip6-localnet\nff00::0 ip6-mcastprefix\nff02::1 ip6-allnodes\nff02::2 ip6-allrouters')
dns_mapping.close()

# Save mirror setup for posterity
os.system("rm -rf "+mirror_root);
os.makedirs(mirror_root)
saveip = mirror_root + '/' + mirror_root + 'ips.txt'
savegets = mirror_root + '/' + mirror_root + 'gets.txt'
saveserverips = mirror_root + '/' + mirror_root + 'serverips.txt'
shutil.copy('ips.txt', saveip)
shutil.copy('tempgets.txt', savegets)
shutil.copy('serverips.txt', saveserverips)
