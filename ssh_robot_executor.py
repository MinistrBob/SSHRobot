import paramiko
import traceback
import SETTINGS

commands = SETTINGS.cl.splitlines()
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

for ip, param in SETTINGS.sl.items():
    print((' Host: ' + ip + ' ').center(60, '-'))
    if 'port' in param:
        default_SSH_port = param['port']
    try:
        ssh.connect(ip, username=param['login'], password=param['password'], port=SETTINGS.default_SSH_port)
    except (ConnectionError, TimeoutError) as e:
        print(f"ERROR: Can't connect to {ip}")
        print(e)
        continue
    except Exception as e:
        print(f"ERROR: Can't connect to {ip}")
        print(traceback.format_exc())
        continue

    for command in commands:
        # command = command.replace("{ip}", ip)
        command = command.replace("{hostname}", param['hostname'])
        print(f"# {command}")
        try:
            stdin, stdout, stderr = ssh.exec_command(command)
            stdin.write(param['login'] + '\n')
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
