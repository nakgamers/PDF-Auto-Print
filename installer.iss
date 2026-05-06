[Setup]
AppName=Nandz PDF Auto Print
AppVersion=2.0
DefaultDirName={autopf}\Nandz PDF Auto Print
DefaultGroupName=Nandz PDF Auto Print
OutputDir=output
OutputBaseFilename=NandzPDFAutoPrintSetup
Compression=lzma
SolidCompression=yes
WizardStyle=modern

SetupIconFile=release\favicon.ico
UninstallDisplayIcon={app}\print.exe

; =========================================================
; FILES
; =========================================================
[Files]

; COPY SEMUA FILE DI FOLDER RELEASE
Source: "release\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

; =========================================================
; SHORTCUT
; =========================================================
[Icons]

Name: "{group}\Nandz PDF Auto Print"; Filename: "{app}\print.exe"; IconFilename: "{app}\print.exe"

Name: "{commondesktop}\Nandz PDF Auto Print"; Filename: "{app}\print.exe"; IconFilename: "{app}\print.exe"

; =========================================================
; RUN AFTER INSTALL
; =========================================================
[Run]

Filename: "{app}\print.exe"; Description: "Jalankan Nandz PDF Auto Print"; Flags: nowait postinstall skipifsilent