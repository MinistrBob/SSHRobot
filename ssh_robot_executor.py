import paramiko
import traceback

import SL
import CL


commands = CL.command_list.splitlines()

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

for ip, conn in SL.server_list.items():
    print((' Host: ' + ip + ' ').center(60, '-'))
    try:
        try:
            ssh.connect(ip, username=conn[0], password=conn[1], port=conn[2])
        except IndexError:
            ssh.connect(ip, username=conn[0], password=conn[1])
    except Exception as e:
        print(f"ERROR: Can't connect to {ip}")
        print(traceback.format_exc())
        continue

    for command in commands:
        command = command.replace("{ip}", ip)
        print(f"Execute command: {command}")
        try:
            stdin, stdout, stderr = ssh.exec_command(command)
            stdin.write(conn[1] + '\n')
            stdin.flush()
            err = stderr.read().decode('utf-8')
            print(stdout.read().decode('utf-8'))
            # print(err)
            if len(err) > 0:
                print(f"ERROR: Execute command: {command}")
                print(f"{err}")
                print(f"Execution break")
                break
        except Exception as e:
            print(f"ERROR: Execute command: {command}")
            print(traceback.format_exc())
            print(f"Execution break")
            break
    ssh.close()
    print('-' * 60)

