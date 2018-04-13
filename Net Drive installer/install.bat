@echo off

SET mypath=%~dp0

echo ^>^> Initalising...

rem cd %HOMEPATH%

rem cd documents

rem mkdir Scripts 

rem echo ^>^> Folder Scripts created in: %CD%

rem cd Scripts 

rem copy %mypath%\map_drive.bat

rem echo ^>^> copied map_Drive.bat to: %CD%

cd "%mypath%..\..\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup"

copy %mypath%mapdrive.vbs

echo ^>^> mapdrive.vbs copied to: %CD%

echo ^>^> completed, have a good day!

pause