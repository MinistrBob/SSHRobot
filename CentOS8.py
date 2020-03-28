# Command List file, used for CentOS 8

# DEBUG
command_list = """echo $%hosthame%
"""

# Get hostname (for test)
# command_list = """hostname
# """

# Rename server
# command_list = """hostnamectl set-hostname {hostname}
# hostname
# """

# Disable Selinux
# command_list = """sed -i -- s/=enforcing/=disabled/g /etc/selinux/config
# reboot
# """

# DNS settings
# command_list = """nmcli connection modify eno5 ipv4.dns "10.128.241.101 10.128.241.102"
# nmcli connection modify eno5 ipv4.dns-search "dc1.local"
# systemctl restart NetworkManager
# nmcli connection show eno5 | grep ipv4.dns
# cat /etc/resolv.conf
# """

# Time sync
# command_list = """sudo chmod 777 /etc/chrony.conf
# sudo sed -i.bak -e "s/pool 2.centos.pool.ntp.org iburst/# pool 2.centos.pool.ntp.org iburst\\nserver 10.128.1.1 iburst/g" /etc/chrony.conf
# sudo chmod 644 /etc/chrony.conf
# sudo chmod 644 /etc/chrony.conf.bak
# head -5 /etc/chrony.conf
# sudo systemctl enable chronyd
# sudo systemctl start chronyd
# chronyc sourcestats
# """

# Time sync (test)
# command_list = """chronyc sourcestats
# """

# Disable cockpit
# command_list = """sudo systemctl disable --now cockpit.socket
# """

# Enable desired repositories
# command_list = """dnf install yum-utils
# yum-config-manager --enable AppStream
# yum-config-manager --enable BaseOS
# yum-config-manager --enable extras
# """

# ===============================================
# Disable ipv6
# command_list = """sudo echo net.ipv6.conf.all.disable_ipv6 = 1 >> /etc/sysctl.conf
# sudo echo net.ipv6.conf.default.disable_ipv6 = 1 >> /etc/sysctl.conf
# cat /etc/sysctl.conf
# sudo sysctl -p
# sudo systemctl stop NetworkManager.service
# sudo systemctl start NetworkManager.service
# sudo ifconfig eno5 | grep inet6
# sudo netstat -tulnp | grep 'tcp6\|udp6'
# """