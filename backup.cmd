rem Hostname
rem set compname=%COMPUTERNAME%
FOR /F %%H IN ('hostname') DO SET compname=%%H
if "%compname%"=="" set compname=UNKNOWN

rem Date and time for file name, hours are counted <10 (one character instead of two => 07).
FOR /F "tokens=1-4 delims=., " %%i IN ('DATE /t') DO SET pdate=%%k%%j%%i
FOR /F "tokens=1-4 delims=:"  %%b IN ('TIME /T') DO SET ptime=%%b%%c
set token=%pdate%-%ptime%-%compname%
rem echo %token%

rem Project
SET PNAME=SSHRobot
SET PPATH=_MinistrBob
SET PDIR=%MYGIT_PATH%\%PPATH%\%PNAME%
rem Backup
SET BP=%BACKUP_GIT_PATH%\%PPATH%\%PNAME%
rem Path to 7-Zip
SET SZIP=c:\Program Files\7-Zip\7z.exe

set start_time=%time%

mkdir "%BP%"
"%SZIP%" a -t7z -mx5 -mmt=on -mtc=on -mta=on -mtr=on -xr@exclude.txt -xr!__pycache__ "%BP%\%token%-%PNAME%.7z" "%PDIR%\*"
"%SZIP%" a -t7z -mx5 -mmt=on -mtc=on -mta=on -mtr=on -mhe=on -p%mypass% -ir@exclude.txt "%BP%\%token%-%PNAME%-PASS.7z" "%PDIR%\exclude.txt"
rem Skips the last 14 files. Since each backup is 2 files, there are 7 LAST backups.
cd /d "%BP%"
for /f "skip=14 eol=: delims=" %%F in ('dir /b /o-d *.7z') do @del "%%F"

call :get_elapsed "%start_time%" "%time%"
echo The archive was created in %elapsed_min% minutes and %elapsed_sec% seconds
pause
exit /b

:get_elapsed
set "start_h=%~1"
set "end_h=%~2"
set /a s_h=%start_h:~0,2%
set /a s_m=%start_h:~3,2%
set /a s_s=%start_h:~6,2%
set /a e_h=%end_h:~0,2%
set /a e_m=%end_h:~3,2%
set /a e_s=%end_h:~6,2%
set /a total_s=(e_h*3600+e_m*60+e_s)-(s_h*3600+s_m*60+s_s)
if %total_s% lss 0 set /a total_s+=86400
set /a elapsed_min=total_s/60
set /a elapsed_sec=total_s%%60
exit /b
