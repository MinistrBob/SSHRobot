# SSHRobot
Executing commands on multiple servers through SSH.  
- **ssh_robot_executor.py** - Execute list of command from variable command_list from CL.py on list of servers from variable lst from SL.py.  
- **ssh_robot_file_worker.py** - Perform a series of file operations from variable file_operations_list from FOL.py on list of servers from variable lst from SL.py.  
  
**WARNING:** The project was written for personal use, for cases when the use of Ansible is impossible for various reasons. Therefore, this project in no way can be compared with Ansible in functionality and usability.   

## Quick Start
1. Create list of servers (file SL.py) see below
2. Create list of commands (file CL.py) see below
3. Create SETTINGS.py from SETTINGS_example.py which contains comments to help you figure out what settings you can make.
3. Run ssh_robot_executor.py or ssh_robot_file_worker.py

## Project files for personal use
These files, for privacy reasons, are included in `.gitignore` exceptions, so you need to move them between computers manually.
### SETTINGS.py
Contains various settings. SETTINGS.py which does not push into GitHub and therefore it is possible to store private data in it (for example, passwords, etc.).
You can get SETTINGS.py from SETTINGS_example.py which contains comments to help you figure out what settings you can make.
### SL.py (Server list)
List of servers with their logins and port (optional, default port = 22).
It is dictionary key = IP, value another dictionary that contains various params that can be accessed by parameter name.
You can get this with help ssh_SL_generator.py
Example:
```Python
server_list = {
    '10.128.241.101': {'login': 'root', 'password': 'root_pwd', 'hostname': 'ca-isarch-101.dc1.local'},
    '10.128.241.102': {'login': 'root', 'password': 'root_pwd', 'hostname': 'ca-isarch-102.dc1.local'},
    '10.128.241.103': {'login': 'root', 'password': 'root_pwd', 'hostname': 'ca-isarch-103.dc1.local'}
    ...
}
```
### CL.py (Command List)
List of commands.
Example:
```Python
command_list = """df -h
cd /etc
du
"""
```
### FOL.py (File Operations list)
Example:
```Python
file_operations_list = [
    ('get', r"/home/worker/file1.txt", r"c:/temp/file1.txt"),
    ('get', r'/home/worker/file2.txt', r'c:/temp/file2.txt')
]
```
### CL_archive.txt
History list of commands.

## paramiko
Documentation - https://docs.paramiko.org/en/stable/

## Requirements
```Shell
pip install -r c:\MyGit\SSHRobot\requirements.txt
```

## Possible errors
Paramiko error when trying to edit file: “sudo: no tty present and no askpass program specified” - https://stackoverflow.com/questions/33579184/paramiko-error-when-trying-to-edit-file-sudo-no-tty-present-and-no-askpass-pr
