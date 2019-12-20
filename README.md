# SSHRobot
Executing commands on multiple servers through SSH.
ssh_robot_executor.py - Execute list of command from variable command_list from CL.py on list of servers from variable lst from SL.py.
ssh_robot_file_worker.py - Perform a series of file operations from variable file_operations_list from FOL.py on list of servers from variable lst from SL.py.

# Project files for personal use
These files, for privacy reasons, are included in .gitignore exceptions, so you need to move them between computers manually.
# SL.py (Server list)
List of servers with their logins and port (optional, default port = 22).
Example:
lst = {
    '10.11.12.2': ('main_login2', 'main_password2', 2244),
    '10.11.12.3': ('main_login3', 'main_password3'),
    '10.11.12.4': ('main_login4', 'main_password4')
    ...
}

# CL.py (Command List)
List of commands.
Example:
command_list = """df -h
cd /etc
du
"""

# FOL.py (File Operations list)
Example:
file_operations_list = [
    ('get', r"/home/worker/file1.txt", r"c:/temp/file1.txt"),
    ('get', r'/home/worker/file2.txt', r'c:/temp/file2.txt')
]


# CL_archive.txt
History list of commands.

# paramiko
Documentation - https://docs.paramiko.org/en/stable/

# Requirements
pip freeze > c:\MyGit\SSHRobot\requirements.txt
pip install -r c:\MyGit\SSHRobot\requirements.txt