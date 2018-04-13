Set oShell = CreateObject ("Wscript.Shell") 
'Dim strArgs
'strArgs = "cmd /c %HOMEPATH%\Documents\Scripts\map_drive.bat"
Dim command
command = "cmd /c net use Y: ""\\192.168.0.14\drive 1"" 0p3N97lock /USER:admin /persistent:yes"
oShell.Run command, 0, false