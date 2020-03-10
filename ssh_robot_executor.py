import paramiko
import traceback

import SL
import CL

# Current SL (Server List)
# sl = SL.server_list_full
# sl = SL.cassandra_servers
sl = SL.test_servers
# Current CL (Command List)
cl = CL.command_list

commands = cl.splitlines()
port = '22'

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

for ip, conn in sl.items():
    print((' Host: ' + ip + ' ').center(60, '-'))
    if len(conn) == 3:
        port = conn[2]
    try:
        ssh.connect(ip, username=conn[0], password=conn[1], port=port)
    except (ConnectionError, TimeoutError) as e:
        print(f"ERROR: Can't connect to {ip}")
        print(e)
    except Exception as e:
        print(f"ERROR: Can't connect to {ip}")
        print(traceback.format_exc())
    finally:
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
