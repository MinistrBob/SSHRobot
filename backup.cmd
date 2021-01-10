rem Date and time for file name, hours are counted <10 (one character instead of two => 07).
FOR /F "tokens=1-4 delims=., " %%i IN ('DATE /t') DO SET pdate=%%k_%%j_%%i
FOR /F "tokens=1-4 delims=:"  %%b IN ('TIME /T') DO SET ptime=%%b_%%c
set date_name=%pdate%_%ptime%
rem echo %date_name%

rem Base Project Folder
SET BASEPATH=c:\MyGit
rem Folder Project Name 
SET PNAME=SSHRobot
rem Backup Path
SET BP=d:\YandexDisk\MyGitBackup\%PNAME%
rem Path to WinRAR
rem SET WINRAR=C:\Program Files\WinRAR\WinRAR.exe
rem Path to 7-Zip
SET SZIP=c:\Program Files\7-Zip\7z.exe

mkdir "%BP%"
rem "%WINRAR%" a -r -s -m5 -md1024 -ag_YYYYMMDD-NN "%BP%\%PNAME%.rar" "c:\MyGit\%PNAME%\*"
"%SZIP%" a -t7z -r -mx9 -mtc=on -mta=on -mtr=on -xr!CL_archive.txt -xr!SL.py -xr!FOL.py -xr!test.py -xr!SETTINGS.py -xr!__pycache__ "%BP%\%date_name%_%PNAME%.7z" "%BASEPATH%\%PNAME%\*"
"%SZIP%" a -t7z -r -mx9 -mtc=on -mta=on -mtr=on -p%mypass% "%BP%\%date_name%_%PNAME%_PASS.7z" "%BASEPATH%\%PNAME%\SETTINGS.py" "%BASEPATH%\%PNAME%\CL_archive.txt" "%BASEPATH%\%PNAME%\SL.py" "%BASEPATH%\%PNAME%\FOL.py" "%BASEPATH%\%PNAME%\test.py"
rem Delete backups except last 6
cd /d "%BP%"
for /f "skip=6 eol=: delims=" %%F in ('dir /b /o-d *.7z') do @del "%%F"

pause
