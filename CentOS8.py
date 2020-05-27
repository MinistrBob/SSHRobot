# Command List file, used for CentOS 8

# DEBUG
c_debug = """echo $%hosthame%
"""

# Get hostname (check)
c_hostname = """hostname
"""

# Check sudo
# echo <password> | sudo -S ls
c_check_sudo = """sudo -S ls
"""

# Rename server
c_rename_server = """sudo hostnamectl set-hostname {hostname}
hostname
"""

# Disable Selinux (check)
c_disable_selinux_check = """cat /etc/selinux/config | grep ^SELINUX=
getenforce
sestatus
"""

# Disable Selinux
c_disable_selinux = """sed -i -- s/=enforcing/=disabled/g /etc/selinux/config
reboot
"""

# DNS settings (check)
c_dns_settings_check = """nmcli connection show ens160 | grep ipv4.dns
cat /etc/resolv.conf
"""

# DNS settings 1
c_dns_settings_1 = """nmcli connection modify eno5 ipv4.dns "10.128.241.101 10.128.241.102"
nmcli connection modify eno5 ipv4.dns-search "dc1.local"
sudo systemctl restart NetworkManager
nmcli connection show eno5 | grep ipv4.dns
cat /etc/resolv.conf
"""

# DNS settings 2
c_dns_settings_2 = """sudo nmcli connection modify ens160 ipv4.dns "172.26.12.80 172.26.12.81 172.28.20.94 8.8.8.8"
sudo nmcli connection modify ens160 ipv4.dns-search "dear.local"
sudo systemctl restart NetworkManager
nmcli connection show ens160 | grep ipv4.dns
cat /etc/resolv.conf
"""

# Time sync (check)
c_tyme_sync_check = """chronyc sourcestats
head -n 10 /etc/chrony.conf
"""

# Time sync
c_tyme_sync = """sudo chmod 777 /etc/chrony.conf
sudo sed -i.bak -e "s/pool 2.centos.pool.ntp.org iburst/# pool 2.centos.pool.ntp.org iburst\\nserver 10.128.1.1 iburst/g" /etc/chrony.conf
sudo chmod 644 /etc/chrony.conf
sudo chmod 644 /etc/chrony.conf.bak
head -5 /etc/chrony.conf
sudo systemctl enable chronyd
sudo systemctl start chronyd
chronyc sourcestats
"""

# Disable cockpit
c_disable_cockpit = """sudo systemctl disable --now cockpit.socket
"""

# Enable desired repositories
c_enable_ropos = """sudo dnf -y install yum-utils
sudo yum-config-manager --enable AppStream
sudo yum-config-manager --enable BaseOS
sudo yum-config-manager --enable extras
"""

# Update OS
c_update_os = """ sudo dnf update -y
"""

# ===============================================
# Disable ipv6
c_disable_ipv6 = """sudo chmod 777 /etc/sysctl.conf
sudo echo net.ipv6.conf.all.disable_ipv6 = 1 >> /etc/sysctl.conf
sudo echo net.ipv6.conf.default.disable_ipv6 = 1 >> /etc/sysctl.conf
sudo chmod 644 /etc/sysctl.conf
cat /etc/sysctl.conf
sudo sysctl -p
sudo systemctl stop NetworkManager.service
sudo systemctl start NetworkManager.service
sudo ifconfig eno5 | grep inet6
sudo netstat -tulnp | grep 'tcp6\|udp6'
"""

# Disable ipv6 for individual services
# Postrges12 (not default database path)
# cat /mnt/database/postgresql/12/data/postgresql.conf | grep listen_addresses
# Httpd
# cat /etc/httpd/conf/httpd.conf | grep ^Listen

# Setting proxy for OS, dnf, yum
c_proxy_check = """sudo cat /etc/environment | wc -l
sudo cat /etc/dnf/dnf.conf | grep -i proxy | wc -l
sudo cat /etc/yum.conf | grep -i proxy | wc -l
"""

####################################################################

# ALL COMMANDS
c_all_commands = """hostname
hostnamectl set-hostname {hostname}
hostname
cat /etc/selinux/config | grep ^SELINUX=
nmcli connection modify eno5 ipv4.dns "10.128.241.101 10.128.241.102"
nmcli connection modify eno5 ipv4.dns-search "dc1.local"
systemctl restart NetworkManager
nmcli connection show eno5 | grep ipv4.dns
cat /etc/resolv.conf
sudo chmod 777 /etc/chrony.conf
sudo sed -i.bak -e "s/pool 2.centos.pool.ntp.org iburst/# pool 2.centos.pool.ntp.org iburst\\nserver 10.128.1.1 iburst/g" /etc/chrony.conf
sudo chmod 644 /etc/chrony.conf
sudo chmod 644 /etc/chrony.conf.bak
head -5 /etc/chrony.conf
sudo systemctl enable chronyd
sudo systemctl start chronyd
chronyc sourcestats
sudo systemctl disable --now cockpit.socket
"""

##################################################
# For Cassandra
##################################################

# Enable firewall
c_enable_firewall = """sudo systemctl start firewalld
sudo systemctl enable firewalld
sudo systemctl status firewalld
sudo systemctl status firewalld | grep Active
sudo firewall-cmd --state
"""

# Configuring firewall port access - https://docs.datastax.com/en/archived/cassandra/3.0/cassandra/configuration/secureFireWall.html
c_firewall_cassandra = """sudo firewall-cmd --zone=public --add-port=7000/tcp --add-port=7001/tcp --add-port=7199/tcp --add-port=9042/tcp --add-port=9160/tcp --add-port=9142/tcp --add-port=61619-61621/tcp --permanent
sudo firewall-cmd --reload
sudo firewall-cmd --zone=public --list-all
"""

# Disable cassandra
c_disable_cassandra = """sudo systemctl stop cassandra
sudo systemctl disable cassandra
"""

# jvm.options (check)
c_jvm_options_check = """cat /etc/cassandra/default.conf/jvm.options | grep '\-Xms\|\-Xmx'
"""

# Edit /etc/cassandra/default.conf/jvm.options
c_jvm_options_edit = """sudo sed -i.bak -e "s/#-Xms4G/-Xms32G/g" /etc/cassandra/default.conf/jvm.options
sudo sed -i -e "s/#-Xmx4G/-Xmx32G/g" /etc/cassandra/default.conf/jvm.options
cat /etc/cassandra/default.conf/jvm.options | grep '\-Xms\|\-Xmx'
"""

# /etc/sysctl.conf (check)
c_etc_sysctl_conf_check = """cat /etc/sysctl.conf | grep fs.file-max
"""

# Edit /etc/sysctl.conf
c_etc_sysctl_conf = """sudo cp /etc/sysctl.conf /etc/sysctl.conf.bak
sudo chmod 777 /etc/sysctl.conf
sudo echo fs.file-max = 999999 >> /etc/sysctl.conf
sudo chmod 644 /etc/sysctl.conf
cat /etc/sysctl.conf
"""

# Edit /etc/security/limits.conf
c_etc_security_limits_conf = """sudo cp /etc/security/limits.conf /etc/security/limits.conf.bak
sudo chmod 777 /etc/security/limits.conf
sudo echo '* soft nproc 65535' >> /etc/security/limits.conf
sudo echo '* hard nproc 65535' >> /etc/security/limits.conf
sudo echo '* soft nofile 999999' >> /etc/security/limits.conf
sudo echo '* hard nofile 999999' >> /etc/security/limits.conf
sudo chmod 644 /etc/security/limits.conf
cat /etc/security/limits.conf
"""

# /etc/profile.d/custom.sh (previously put the file to the server)
c_etc_profile_d_custom_sh = """sudo cp /home/worker/custom.sh /etc/profile.d/
sudo chmod 755 /etc/profile.d/custom.sh
ls -al /etc/profile.d/custom.sh
cat /etc/profile.d/custom.sh
"""

# reboot
c_reboot = """sudo reboot now
"""
