# Command List file, used for CentOS 8

# DEBUG
c_debug = """echo $%hosthame%
"""

#### Frequently used ####

# Install package
install_package = {'check': None,
                   'check_result': None,
                   'command': """sudo dnf -y install git""",
                   'show': """sudo dnf list installed | grep git""",
                   'execute_anyway': False,
                   'show_after': False,
                   'show_before': True
                   }

#### Commands for install ####
# Get hostname (check)
check_hostname = """hostname
"""

# Check sudo
# echo <password> | sudo -S ls
check_sudo = """sudo -S ls
"""

# Rename server
c_rename_server = """sudo hostnamectl set-hostname {hostname}
hostname
"""

# Disable Selinux (check)
check_disable_selinux = """cat /etc/selinux/config | grep ^SELINUX=
getenforce
sestatus
"""

# Disable Selinux
c_disable_selinux = """sed -i -- s/=enforcing/=disabled/g /etc/selinux/config
reboot
"""

# DNS settings (check)
check_dns_settings = """nmcli connection show eno5 | grep ipv4.dns
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
check_tyme_sync = """chronyc sourcestats
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
check_ropos = {'check': None,
               'check_result': None,
               'command': None,
               'show': """sudo dnf repolist""",
               'execute_anyway': False,
               'show_after': True,
               'show_before': False
               }
enable_ropos = {'check': None,
                'check_result': None,
                'command': """sudo dnf -y install yum-utils
sudo yum-config-manager --enable AppStream
sudo yum-config-manager --enable BaseOS
sudo yum-config-manager --enable extras
sudo yum-config-manager --enable epel
""",
                'show': """sudo dnf repolist""",
                'execute_anyway': False,
                'show_after': True,
                'show_before': True
                }
# Install and Enable epel repositories
enable_epel_ropos = {'check': None,
                     'check_result': None,
                     'command': """sudo dnf -y install yum-utils epel-release
sudo yum-config-manager --enable epel
""",
                     'show': """sudo dnf repolist | grep epel""",
                     'execute_anyway': False,
                     'show_after': False,
                     'show_before': True
                     }

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

# Setting proxy for OS
os_proxy = {'check': """sudo cat /etc/environment | wc -l""",
            'check_result': {'type': "int", 'value': 10, 'execute': 4, 'ok': 1, 'error': 3},
            'command': """sudo chmod 777 /etc/environment
sudo echo https_proxy=http://10.128.28.145:3128/ > /etc/environment
sudo echo http_proxy=http://10.128.28.145:3128/ >> /etc/environment
sudo echo no_proxy=localhost,127.0.0.0/8,::1,10.128.0.0/16 >> /etc/environment
sudo echo all_proxy=socks://10.128.28.145:3128/ >> /etc/environment
sudo echo ftp_proxy=http://10.128.28.145:3128/ >> /etc/environment
sudo echo HTTP_PROXY=http://10.128.28.145:3128/ >> /etc/environment
sudo echo FTP_PROXY=http://10.128.28.145:3128/ >> /etc/environment
sudo echo ALL_PROXY=socks://10.128.28.145:3128/ >> /etc/environment
sudo echo NO_PROXY=localhost,127.0.0.0/8,::1,10.128.0.0/16 >> /etc/environment
sudo echo HTTPS_PROXY=http://10.128.28.145:3128/ >> /etc/environment
sudo chmod 644 /etc/environment""",
            'show': """sudo cat /etc/environment""",
            'execute_anyway': False,
            'show_after': True,
            'show_before': True
            }
os_proxy_check = {'check': """sudo cat /etc/environment | wc -l""",
                  'check_result': {'type': "int", 'value': 10, 'execute': 4, 'ok': 1, 'error': 3},
                  'command': """""",
                  'show': """sudo cat /etc/environment""",
                  'execute_anyway': False,
                  'show_after': True,
                  'show_before': True
                  }

# Setting proxy for dnf
dnf_proxy = {'check': """sudo cat /etc/dnf/dnf.conf | grep -i proxy | wc -l""",
             'check_result': {'type': "int", 'value': 1, 'execute': 4, 'ok': 1, 'error': 3},
             'command': """sudo chmod 777 /etc/dnf/dnf.conf
sudo echo 'proxy=http://10.128.28.145:3128' >> /etc/dnf/dnf.conf
sudo chmod 644 /etc/dnf/dnf.conf""",
             'show': """sudo cat /etc/dnf/dnf.conf""",
             'execute_anyway': False,
             'show_after': True,
             'show_before': True
             }
# {1 ==; 2 !=; 3 <; 4 >; 5 =<; 6 >=}
# Check settings proxy for dnf (only check)
# type, value, execute, OK (not execute), error
dnf_proxy_check = {'check': """sudo cat /etc/dnf/dnf.conf | grep -i proxy | wc -l""",
                   'check_result': {'type': "int", 'value': 1, 'execute': 4, 'ok': 1, 'error': 3},
                   'command': """""",
                   'show': """sudo cat /etc/dnf/dnf.conf""",
                   'execute_anyway': True,
                   'show_after': True,
                   'show_before': True
                   }

# Setting proxy for dnf
yum_proxy = {'check': """sudo cat /etc/yum.conf | grep -i proxy | wc -l""",
             'check_result': {'type': "int", 'value': 1, 'execute': 4, 'ok': 1, 'error': 3},
             'command': """sudo chmod 777 /etc/yum.conf
sudo echo 'proxy=http://10.128.28.145:3128' >> /etc/yum.conf
sudo chmod 644 /etc/yum.conf""",
             'show': """sudo cat /etc/yum.conf""",
             'execute_anyway': False,
             'show_after': True,
             'show_before': True
             }

# Enable firewall
enable_firewall = {'check': None,
                   'check_result': None,
                   'command': """sudo systemctl start firewalld
sudo systemctl enable firewalld
sudo systemctl status firewalld
sudo systemctl status firewalld | grep Active
sudo firewall-cmd --state""",
                   'show': """""",
                   'execute_anyway': True,
                   'show_after': False,
                   'show_before': False
                   }

# Setting firewall
setting_firewall = {'check': None,
                    'check_result': None,
                    'command': """sudo firewall-cmd --add-service=zabbix-server --permanent
sudo firewall-cmd --reload
sudo firewall-cmd --zone=public --list-all""",
                    'show': """""",
                    'execute_anyway': True,
                    'show_after': False,
                    'show_before': False
                    }

# Setting firewall (check)
setting_firewall_check = {'check': None,
                          'check_result': None,
                          'command': """sudo firewall-cmd --reload
sudo firewall-cmd --zone=public --list-all""",
                          'show': """""",
                          'execute_anyway': True,
                          'show_after': False,
                          'show_before': False
                          }

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

# Cassandra firewall
# https://docs.datastax.com/en/archived/cassandra/3.0/cassandra/configuration/secureFireWall.html
firewall_cassandra = {'check': None,
                      'check_result': None,
                      'command': """sudo firewall-cmd --zone=public --add-port=7000/tcp --add-port=7001/tcp --add-port=7199/tcp --add-port=9042/tcp --add-port=9160/tcp --add-port=9142/tcp --add-port=61619-61621/tcp --permanent
sudo firewall-cmd --add-service=zabbix-agent --permanent
sudo firewall-cmd --reload
sudo firewall-cmd --zone=public --list-all""",
                      'show': """""",
                      'execute_anyway': True,
                      'show_after': False,
                      'show_before': False
                      }

# Disable cassandra
c_disable_cassandra = """sudo systemctl stop cassandra
sudo systemctl disable cassandra
"""

# jvm.options (check)
check_jvm_options = """cat /etc/cassandra/default.conf/jvm.options | grep '\-Xms\|\-Xmx'
"""

# Edit /etc/cassandra/default.conf/jvm.options
c_jvm_options_edit = """sudo sed -i.bak -e "s/#-Xms4G/-Xms32G/g" /etc/cassandra/default.conf/jvm.options
sudo sed -i -e "s/#-Xmx4G/-Xmx32G/g" /etc/cassandra/default.conf/jvm.options
cat /etc/cassandra/default.conf/jvm.options | grep '\-Xms\|\-Xmx'
"""

# /etc/sysctl.conf (check)
check_etc_sysctl_conf = """cat /etc/sysctl.conf | grep fs.file-max
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

# Enable desired repositories
visudo = {'check': """sudo cat /etc/sudoers | grep -i worker | wc -l""",
          'check_result': {'type': "int", 'value': 1, 'execute': 4, 'ok': 1, 'error': 3},
          'command': """echo 'worker ALL=(ALL:ALL) NOPASSWD:ALL' | sudo EDITOR='tee -a' visudo""",
          'show': """sudo cat /etc/sudoers | grep -i worker""",
          'execute_anyway': False,
          'show_after': True,
          'show_before': True
          }

# {1 ==; 2 !=; 3 <; 4 >; 5 =<; 6 >=}
# type, value, execute, OK (not execute), error (value OP result)
# Install Zabbix Agent
zabbix_agent = {'check': """sudo dnf list installed | grep ^zabbix-agent | wc -l""",
                'check_result': {'type': "int", 'value': 1, 'execute': 4, 'ok': 1, 'error': 3},
                'command': """sudo rpm -Uvh https://repo.zabbix.com/zabbix/5.0/rhel/8/x86_64/zabbix-release-5.0-1.el8.noarch.rpm
sudo dnf clean all
sudo dnf -y install zabbix-agent
sudo dnf list installed | grep ^zabbix
sudo sed -i.bak -e "s/Server=127.0.0.1/Server=127.0.0.1,10.128.241.0\/24/g" /etc/zabbix/zabbix_agentd.conf
sudo sed -i.bak -e "s/ServerActive=127.0.0.1/ServerActive=10.128.241.222/g" /etc/zabbix/zabbix_agentd.conf
sudo sed -i.bak -e "s/^Hostname=.*/Hostname=$(hostname -I | cut -d" " -f 1)/g" /etc/zabbix/zabbix_agentd.conf
cat /etc/zabbix/zabbix_agentd.conf | grep ^Server=
cat /etc/zabbix/zabbix_agentd.conf | grep ^ServerActive=
cat /etc/zabbix/zabbix_agentd.conf | grep ^Hostname=
sudo systemctl enable --now zabbix-agent
sudo systemctl restart zabbix-agent
sudo ps -Fu zabbix
sudo firewall-cmd --add-service=zabbix-agent --permanent
sudo firewall-cmd --reload
sudo firewall-cmd --zone=public --list-all
sudo firewall-cmd --zone=public --list-all | grep zabbix-agent
""",
                'show': """""",
                'execute_anyway': False,
                'show_after': True,
                'show_before': True
                }

zabbix_agent_change_host = {'check': None,
                   'check_result': None,
                   'command': """sudo sed -i.bak -e "s/^Hostname=.*/Hostname=$(hostname -I | cut -d" " -f 1)/g" /etc/zabbix/zabbix_agentd.conf
cat /etc/zabbix/zabbix_agentd.conf | grep ^Hostname=
sudo systemctl restart zabbix-agent
""",
                   'show': """cat /etc/zabbix/zabbix_agentd.conf | grep ^Hostname=""",
                   'execute_anyway': False,
                   'show_after': True,
                   'show_before': False
                   }

# nothing provides module(perl:5.26) needed by module perl-DBD-MySQL:4.046:8010020191114030811:073fa5fe-0.x86_64
fix_error = {'check': None,
             'check_result': None,
             'command': """sudo yum -y module reset perl-DBD-MySQL perl-DBD-SQLite perl-DBI""",
             'show': """""",
             'execute_anyway': False,
             'show_after': False,
             'show_before': False
             }

firewall_wildfly = {'check': None,
                    'check_result': None,
                    'command': """sudo systemctl start firewalld
sudo systemctl enable firewalld
sudo systemctl status firewalld
sudo systemctl status firewalld | grep Active
sudo firewall-cmd --state
sudo firewall-cmd --permanent --add-port=1098/tcp --add-port=1099/tcp --add-port=4444/tcp --add-port=4445/tcp --add-port=4712/tcp --add-port=4713/tcp --add-port=7600/tcp --add-port=8009/tcp --add-port=8080/tcp --add-port=8083/tcp --add-port=8093/tcp --add-port=8443/tcp --add-port=9990/tcp --add-port=9993/tcp --add-port=37559/tcp --add-port=23364/udp --add-port=45700/udp --add-port=45688/udp --add-port=55200/udp
sudo firewall-cmd --add-service=zabbix-agent --permanent
sudo firewall-cmd --reload
sudo firewall-cmd --zone=public --list-all""",
                    'show': """""",
                    'execute_anyway': True,
                    'show_after': False,
                    'show_before': False
                    }

setting_eno5 = {'check': None,
                'check_result': None,
                'command': """sudo ifconfig""",
                'show': """""",
                'execute_anyway': True,
                'show_after': False,
                'show_before': False
                }
