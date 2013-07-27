import sys
import os
import shutil

# check cmd line
if (len(sys.argv) < 5):
  print "Usage: Enter getinfo, mirror_root, working_dir, and hostname\n"
  exit(5)

# file name with gets and ips
getinfo = sys.argv[1]

# root folder to save in
mirror_root = sys.argv[2]

# working directory
working_dir = sys.argv[3]

# hostname
hostname= sys.argv[4]

# keep track of distinct IPs in gets file for etc/hosts in VM
ips = []
host_mapping = open('dns-mappings.txt', 'w')

# keep track of domain names to determine unique domain names
domain_names = []

# File with list of IPs for Mininet setup
mininet_cfg  = open('serverips.txt','w')

# Number of distinct IPs
count = 0

mirror_path = 'mirror-folder/' + str(mirror_root)

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

  # Add to host mapping file for DNS, if domain_name isn't in file
  if domain_name not in domain_names:
    domain_names.append(domain_name)
    host_mapping.write(str(ip.strip()) + ' ' + domain_name + '\n')

  if ip not in ips:
    # Saw distinct IP
    ips.append(ip)

    # Add to list of IPs for Mininet
    mininet_cfg.write(str(ip.strip()) + '\n')
    count = count + 1

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
dns_mapping = open('mapping.expt', 'w')
dns_mapping.write('127.0.0.1       localhost\n127.0.1.1 '+str(hostname)+'\n')
for entry in open('dns-mappings.txt'):
  dns_mapping.write(entry)
