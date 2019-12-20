rem Folder Project Name 
SET PNAME=SSHRobot
rem Backup Path
SET BP=d:\BACKUP\MyGit
rem Path to WinRAR
SET WINRAR=C:\Program Files\WinRAR\WinRAR.exe

mkdir "%BP%"
"%WINRAR%" a -r -s -m5 -md1024 -ag_YYYYMMDD-NN "%BP%\%PNAME%.rar" "c:\MyGit\%PNAME%\*"
rem pause
