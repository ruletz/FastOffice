
$WshShell = New-Object -ComObject WScript.Shell
$Shortcut = $WshShell.CreateShortcut("$env:USERPROFILE\Desktop\OnlyOffice Fast.lnk")
$Shortcut.TargetPath = "wscript.exe"
$Shortcut.Arguments = '"c:\Projects\OnlyOffice\OnlyOffice.vbs"'
$Shortcut.WorkingDirectory = "c:\Projects\OnlyOffice\app"
$Shortcut.IconLocation = "c:\Projects\OnlyOffice\app\app.ico,0"
$Shortcut.Description = "OnlyOffice - Optimized for Speed"
$Shortcut.Save()
