import paramiko
import traceback
import SETTINGS


def main():
    final_result = {
        'list_error_connect': [],
        'list_error_execute': [],
        'list_error_check': [],
        'list_success': []
    }
    total = len(SETTINGS.sl)
    if total > 0:
        for ip, param in SETTINGS.sl.items():
            one_server(ip, param, final_result, SETTINGS.module)
        print("=" * 120)
        success = len(final_result['list_success'])
        if success > 0:
            print(
                f"RESULT: The commands was executed successfully on {success}/{total}={round(success * 100 / total)}% "
                f"servers:")
            if SETTINGS.succes_list_report:
                for i in final_result['list_success']:
                    print(f"{i}")
                print("=" * 120)
        else:
            print("RESULT: NOT A SINGLE SUCCESSFUL EXECUTION!!!")
        if SETTINGS.report:
            get_report(final_result)
    else:
        print("List servers empty")


def compare_values(value, result, operator):
    # {1 ==; 2 !=; 3 <; 4 >; 5 =<; 6 >=}
    if operator == 1:
        return value == result
    elif operator == 2:
        return value != result
    elif operator == 3:
        return value < result
    elif operator == 4:
        return value > result
    elif operator == 5:
        return value <= result
    elif operator == 6:
        return value >= result
    else:
        return 'error'


def check_result(cr, result, ip, final_result):
    """"
    String values are compared only by ==.
    return False if error or value matches (not need execute)
    """
    # 'check_result': {'type': "int", 'value': 1, 'execute': 3, 'ok': 1, 'error': 4},
    if cr['type'] == "int":
        try:
            value = int(cr['value'])
            try:
                result = int(result)
                s = compare_values(value, result, cr['ok'])
                if s == 'error':
                    final_result['list_error_check'].append((ip, f"Error compare value and result (ok)"))
                    return 'error'
                elif s:
                    return 'noexec'
                else:
                    s = compare_values(value, result, cr['execute'])
                    if s == 'error':
                        final_result['list_error_check'].append((ip, f"Error compare value and result (execute)"))
                        return 'error'
                    elif s:
                        return 'exec'
                    else:
                        s = compare_values(value, result, cr['error'])
                        if s == 'error':
                            final_result['list_error_check'].append((ip, f"Error compare value and result (error)"))
                            return 'error'
                        elif s:
                            final_result['list_error_check'].append((ip, f"This value of result indicates an error "
                                                                         f"situation"))
                            return 'error'
                        else:
                            final_result['list_error_check'].append((ip, f"I don't understand what to do"))
                            return 'error'
            except Exception as e:
                final_result['list_error_check'].append((ip, f"Can't int result:{e}"))
                return 'error'
        except Exception as e:
            final_result['list_error_check'].append((ip, f"Can't int value:{e}"))
            return 'error'
    elif cr['type'] == "str":
        if cr['value'] == result:
            return 'noexec'
        else:
            return 'exec'
    else:
        final_result['list_error_check'].append((ip, "Unknown value format"))
        return 'error'


def one_server(ip, param, final_result, module):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # Create connection to server
    print((' Host: ' + ip + ' ').center(60, '-'))
    if 'port' in param:
        default_ssh_port = param['port']
    else:
        default_ssh_port = SETTINGS.default_SSH_port
    try:
        ssh.connect(ip, username=param['login'], password=param['password'], port=default_ssh_port)
        # chan = ssh.get_transport().open_session()
    except (ConnectionError, TimeoutError) as e:
        print(f"ERROR: Can't connect to {ip}")
        print(e)
        final_result['list_error_connect'].append((ip, e))
        return
    except Exception as e:
        print(f"ERROR: Can't connect to {ip}")
        print(traceback.format_exc())
        final_result['list_error_connect'].append((ip, e))
        return

    # Show before
    if SETTINGS.show_before and module['show_before'] and module['show']:
        print("show before:")
        result = execute_one_command(module['show'], ip, param, ssh)
        if not result:  # if error execute command
            return
    # Check if is
    cr = "exec"  # if there is no check then the commands will be executed anyway
    if module['check']:
        print("check:")
        result = ''
        res = ''
        commands = module['check'].splitlines()
        for command in commands:
            res = execute_one_command(module['check'], ip, param, ssh)
            if not res:  # if error execute command
                return
            else:
                result = result + res
        cr = check_result(module['check_result'], result, ip, final_result)
    # If the result is not what was expected or parameter 'execute_anyway'=True - execute commands
    if cr == "exec" or module['execute_anyway']:
        if module['command']:
            # Execute commands
            print("execute:")
            result = ''
            res = ''
            commands = module['command'].splitlines()
            for command in commands:
                res = execute_one_command(command, ip, param, ssh, final_result)
                if not res:  # if error execute command
                    return
            final_result['list_success'].append((ip, SETTINGS.success_sign))
    elif cr == "noexec":
        # The server passed the test, you do not need to execute commands, we put it on the list of successful
        print("test passed OK:")
        final_result['list_success'].append((ip, SETTINGS.success_sign))
    else:
        return
    # Show after
    if SETTINGS.show_after and module['show_after'] and module['show']:
        print("show after:")
        result = ''
        result = execute_one_command(module['show'], ip, param, ssh)
        if not result:  # if error execute command
            return
    ssh.close()
    # print('-' * 60)
    print()


def execute_one_command(command, ip, param, ssh, final_result=None):
    result = ""
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
            print(out.rstrip())
            result += out.rstrip()
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
                print(f"# {err}")
            else:
                print(f"ERROR: Execute command: {command}")
                print(f"{err}")
                print(f"Execution break")
                if final_result:
                    final_result['list_error_execute'].append((ip, err))
                return False
    except Exception as e:
        print(f"ERROR: Execute command: {command}")
        print(traceback.format_exc())
        print(f"Execution break")
        if final_result:
            final_result['list_error_execute'].append((ip, e))
        return False
    if not result:  # If the command returns nothing, this should not be considered an error.
        result = "OK"
    return result


def get_report(final_result):
    error_c = len(final_result['list_error_connect'])
    error_e = len(final_result['list_error_execute'])
    total = len(SETTINGS.sl)
    if error_c > 0:
        print("=" * 120)
        print(f"Failed to connect to {error_c}/{total}={round(error_c * 100 / total)}% servers:")
        for i in final_result['list_error_connect']:
            print(f"{i}")
    if error_e > 0:
        print("=" * 120)
        print(f"Error executing commands on {error_e}/{total}={round(error_e * 100 / total)}% servers:")
        for i in final_result['list_error_execute']:
            print(f"{i}")
    print("=" * 120)
    print(f"Total list:")
    total_list = [*final_result['list_success'], *final_result['list_error_execute'], *final_result['list_error_check'],
                  *final_result['list_error_connect']]
    total_list.sort(key=lambda tup: tup[0])
    for i in total_list:
        # print(f"{i}")
        print(f"{i[0]}\t{i[1]}")


if __name__ == '__main__':
    main()
