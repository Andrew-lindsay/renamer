Set oShell = CreateObject ("Wscript.Shell") 
Dim strArgs
strArgs = "cmd /c %HOMEPATH%\Documents\Scripts\map_drive.bat"
oShell.Run strArgs, 0, false