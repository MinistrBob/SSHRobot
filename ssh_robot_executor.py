import paramiko
import traceback
import SETTINGS


def main():
    commands = SETTINGS.cl.splitlines()
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    list_error_connect = []
    list_error_execute = []
    list_success = []
    total = len(SETTINGS.sl)
    if total > 0:
        for ip, param in SETTINGS.sl.items():
            # Create connection to server
            print((' Host: ' + ip + ' ').center(60, '-'))
            if 'port' in param:
                default_SSH_port = param['port']
            try:
                ssh.connect(ip, username=param['login'], password=param['password'], port=SETTINGS.default_SSH_port)
                # chan = ssh.get_transport().open_session()
            except (ConnectionError, TimeoutError) as e:
                print(f"ERROR: Can't connect to {ip}")
                print(e)
                list_error_connect.append((ip, e))
                continue
            except Exception as e:
                print(f"ERROR: Can't connect to {ip}")
                print(traceback.format_exc())
                list_error_connect.append((ip, e))
                continue
            # Execute commands
            for command in commands:
                # command = command.replace("{ip}", ip)
                command = command.replace("{hostname}", param['hostname'])
                # param_name =
                # command = command.replace("%hosthame%", param['hostname'])
                print(f"# {command}")
                try:
                    stdin, stdout, stderr = ssh.exec_command(command, get_pty=True)
                    stdin.write(param['password'] + '\n')
                    stdin.flush()
                    err = stderr.read().decode('utf-8')
                    out = stdout.read().decode('utf-8')
                    if len(out) > 0:
                        print(out)
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
                            list_error_execute.append((ip, err))
                            break
                except Exception as e:
                    print(f"ERROR: Execute command: {command}")
                    print(traceback.format_exc())
                    print(f"Execution break")
                    list_error_execute.append((ip, e))
                    break
            ssh.close()
            list_success.append(ip)
            print('-' * 60)
        success = len(list_success)
        error_c = len(list_error_connect)
        error_e = len(list_error_execute)
        if success > 0:
            print(
                f"RESULT: The commands was executed successfully on {success}/{total}={round(success * 100 / total)}% "
                f"servers:")
            for i in list_success:
                print(f"    {i}")
        else:
            print("RESULT: NOT A SINGLE SUCCESSFUL EXECUTION!!!")
        if SETTINGS.report:
            get_report(len(list_error_connect), len(list_error_execute), list_error_connect, list_error_execute,
                       len(SETTINGS.sl))
    else:
        print("List servers empty")


def get_report(error_c, error_e, list_error_connect, list_error_execute, total):
    if error_c > 0:
        print(f"Failed to connect to {error_c}/{total}={round(error_c * 100 / total)}% servers:")
        for i in list_error_connect:
            print(f"    {i}")
    if error_e > 0:
        print(f"Error executing commands on {error_e}/{total}={round(error_e * 100 / total)}% servers:")
        for i in list_error_execute:
            print(f"    {i}")


if __name__ == '__main__':
    main()
