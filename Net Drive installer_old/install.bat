@echo off c

SET mypath=%~dp0

echo ^>^> Initalising...

cd %HOMEPATH%

cd documents

mkdir Scripts 

echo ^>^> Folder Scripts created in: %CD%

cd Scripts 

copy %mypath%\map_drive.bat

echo ^>^> copied map_Drive.bat to: %CD%

cd "%mypath%..\..\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup"

copy %mypath%hidecmd.vbs

echo ^>^> hidecmd.vbs copied to: %CD%

echo ^>^> completed, have a good day!

pause



