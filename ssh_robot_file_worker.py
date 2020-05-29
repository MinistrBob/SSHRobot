import paramiko
import traceback
import SETTINGS

import SL
import FOL
files = SETTINGS.fl

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

for ip, param in SETTINGS.sl.items():
    print((' Host: ' + ip + ' ').center(60, '-'))
    if 'port' in param:
        default_SSH_port = param['port']
    try:
        ssh.connect(ip, username=param['login'], password=param['password'], port=SETTINGS.default_SSH_port)
        # chan = ssh.get_transport().open_session()
        sftp = ssh.open_sftp()
    except (ConnectionError, TimeoutError) as e:
        print(f"ERROR: Can't connect to {ip}")
        print(e)
        continue
    except Exception as e:
        print(f"ERROR: Can't connect to {ip}")
        print(traceback.format_exc())
        continue

    for file in files:
        print(f"Execute operation: {file[0]} file {file[1]} to {file[2]}")
        try:
            if file[0] == 'get':
                sftp.get(file[1], file[2])
            elif file[0] == 'put':
                sftp.put(file[1], file[2])
            else:
                print(f"ERROR: Unknown operation: {file[0]}")
                break
        except Exception as e:
            print(f"ERROR: Execute operation: {file[0]}")
            print(traceback.format_exc())
            print(f"Execution break")
            break
    ssh.close()
    print('-' * 60)
