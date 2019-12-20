import paramiko
import traceback

import SL
import FOL


ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

for ip, conn in SL.server_list.items():
    print((' Host: ' + ip + ' ').center(60, '-'))
    try:
        try:
            ssh.connect(ip, username=conn[0], password=conn[1], port=conn[2])
        except IndexError:
            ssh.connect(ip, username=conn[0], password=conn[1])
        sftp = ssh.open_sftp()
    except Exception as e:
        print(f"ERROR: Can't connect to {ip}")
        print(traceback.format_exc())
        continue

    for param in FOL.file_operations_list:
        print(f"Execute operation: {param[0]} file {param[1]} to {param[2]}")
        try:
            if param[0] == 'get':
                sftp.get(param[1], param[2])
            elif param[0] == 'put':
                sftp.put(param[2], param[1])
            else:
                print(f"ERROR: Unknown operation: {param[0]}")
                break
        except Exception as e:
            print(f"ERROR: Execute operation: {param[0]}")
            print(traceback.format_exc())
            print(f"Execution break")
            break
    ssh.close()
    print('-' * 60)
