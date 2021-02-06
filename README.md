# SSHRobot
Executing commands on multiple servers through SSH.  
- **ssh_robot_executor.py** - Execute list of command from variable command_list from CL.py on list of servers from variable lst from SL.py.  
- **ssh_robot_file_worker.py** - Perform a series of file operations from variable file_operations_list from FOL.py on list of servers from variable lst from SL.py.  
  
**WARNING:** The project was written for personal use, for cases when the use of Ansible is impossible for various reasons. Therefore, this project in no way can be compared with Ansible in functionality and usability.   

## Quick Start
1. Create list of servers (file SL.py) see below
2. Create list of modules (MOD) see below. File name can be any  
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
## MOD (Module List)
List of modules. It can have any name because it is imported like this  
`import CentOS8 as MOD` 

Algorithm (very simplified) for executing module commands:  
  SHOW commands before
    CHECK commands
      IF check:
        MAIN commands
  SHOW commands after
 
Module example:  
A show commands can be executed before and after the main and check commands. With the help of them, you can show reference information, which can be used for visual control of execution.    
**check** - (**str**). Commands for check.  
**check_result** - (**dict**). Based on the result of executing the check commands, a decision is made whether to execute the main commands. If the type and result are the same as expected, then the check is considered passed.  
  - **type** - (**str**). Expected result type (int or str).  
  - **value** - (**int\str**). Expected execution result.  
  - There are additional checks for an int type.  
    - **ok, execute, error** - (**int**). Specifies the type of the comparison operator {1 ==; 2 !=; 3 <; 4 >; 5 =<; 6 >=}.  
    - if `value (ok operator) result => True` then return 'noexec' = Do not execute the main command.   
    - if `value (execute operator) result => True` then return 'exec' = Execute the main command.  
    - if `value (error operator) result => True` then return 'error' = This is error.   
**command** - (**str**). Main commands.  
**show** - (**str**). Commands for show.  
**execute_anyway** - (**bool**). Regardless of the result of the execution of the check commands, the decision is made whether to execute the main commands. If `True`, then the main commands will execute in any way.  
**show_after** - (**bool**). Do the show command run after the main command is executed? This setting is also available in `SETTINGS.py`.
**show_before** - (**bool**). Do the show command run before the main command is executed? This setting is also available in `SETTINGS.py`.
```# Setting proxy for yum
Command 'show' displays content `/etc/yum.conf` before and after execution main and check commands. This allows you to see what has changed in the configuration.  
Then the 'check' command is executed. If it returns one line ('ok'), then everything is fine and you don't need to execute the main command. 
yum_proxy = {'check': """sudo cat /etc/yum.conf | grep -i proxy | wc -l""",
             'check_result': {'type': "int", 'value': 1, 'execute': 4, 'ok': 1, 'error': 3},
             'command': """sudo chmod 777 /etc/yum.conf
sudo echo 'proxy=http://10.128.28.145:3128' >> /etc/yum.conf
sudo chmod 644 /etc/yum.conf""",
             'show': """sudo cat /etc/yum.conf""",
             'execute_anyway': False,
             'show_after': True,
             'show_before': True
             }
```
## FOL.py (File Operations list)
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
