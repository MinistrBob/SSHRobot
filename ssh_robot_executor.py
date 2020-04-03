import paramiko
import traceback
import SETTINGS

commands = SETTINGS.cl.splitlines()
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
error_count = 0
for ip, param in SETTINGS.sl.items():
    print((' Host: ' + ip + ' ').center(60, '-'))
    if 'port' in param:
        default_SSH_port = param['port']
    try:
        ssh.connect(ip, username=param['login'], password=param['password'], port=SETTINGS.default_SSH_port)
        # chan = ssh.get_transport().open_session()
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
        # param_name =
        # command = command.replace("%hosthame%", param['hostname'])
        print(f"# {command}")
        try:
            stdin, stdout, stderr = ssh.exec_command(command)
            stdin.write(param['password'] + '\n')
            stdin.flush()
            err = stderr.read().decode('utf-8')
            out = stdout.read().decode('utf-8')
            if len(out) > 0:
                print(f"{stdout.read().decode('utf-8')}")
            else:
                if SETTINGS.replace_empty_out_str_with_null:
                    print(SETTINGS.replace_empty_out_str_template)
            # print(err)
            if len(err) > 0:
                # Some normal messages are redirected to the stderr. But this is not a error.
                # We bypass this behavior of some commands.
                # Example: systemctl start may redirect to stderr message: Created symlink ...
                if err.startswith("Created symlink") and "systemctl enable" in command.lower():
                    print(f"# {err}")
                elif err.startswith("Removed") and "systemctl disable" in command.lower():
                    print(f"# {err}")
                elif err.startswith("[sudo] password for"):
                    pass
                else:
                    print(f"ERROR: Execute command: {command}")
                    print(f"{err}")
                    print(f"Execution break")
                    error_count += 1
                    break
        except Exception as e:
            print(f"ERROR: Execute command: {command}")
            print(traceback.format_exc())
            print(f"Execution break")
            break
    ssh.close()
    print('-' * 60)
if error_count > 0:
    print(f"!!! THERE WERE {error_count} ERRORS")
