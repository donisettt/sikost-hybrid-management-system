[Setup]
AppName=SIKOST VibeHouse
AppVersion=1.0
DefaultDirName={autopf}\SIKOST VibeHouse
DefaultGroupName=SIKOST VibeHouse
UninstallDisplayIcon={app}\SIKOST-VibeHouse.exe
OutputDir=.
OutputBaseFilename=SIKOST-VibeHouse-Installer
Compression=lzma
SolidCompression=yes

[Files]
Source: "..\dist\SIKOST-VibeHouse.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\SIKOST VibeHouse"; Filename: "{app}\SIKOST-VibeHouse.exe"
Name: "{commondesktop}\SIKOST VibeHouse"; Filename: "{app}\SIKOST-VibeHouse.exe"; Tasks: desktopicon

[Tasks]
Name: "desktopicon"; Description: "Buat shortcut di desktop"; GroupDescription: "Shortcut:"