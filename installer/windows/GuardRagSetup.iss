; GuardRag Windows installer (Inno Setup)
; Build with: ISCC.exe installer\windows\GuardRagSetup.iss

#define MyAppName "GuardRag"
#define MyAppVersion "0.2.0"
#define MyAppPublisher "GuardRag Team"

[Setup]
AppId={{4A5CA72E-3F93-4A89-BD96-C2FB90AE6368}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
DisableProgramGroupPage=yes
OutputDir=installer\windows\dist
OutputBaseFilename=GuardRag-Setup
Compression=lzma
SolidCompression=yes
WizardStyle=modern
ArchitecturesInstallIn64BitMode=x64
PrivilegesRequired=admin
SourceDir=..\..

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "installmodel"; Description: "Install Mistral model during setup (longer install)"; Flags: checkedonce
Name: "launchapp"; Description: "Launch GuardRag after setup completes"; Flags: checkedonce

[Files]
Source: "*"; DestDir: "{app}"; Excludes: ".git\*,.github\*,.venv\*,venv\*,.ollama\*,logs\*,dist\*,build\*,installer\windows\dist\*,__pycache__\*,*.pyc,*.pyo"; Flags: recursesubdirs createallsubdirs

[Icons]
Name: "{autoprograms}\{#MyAppName}\GuardRag Setup Script"; Filename: "{app}\setup.ps1"

[Run]
Filename: "powershell.exe"; Parameters: "-NoProfile -ExecutionPolicy Bypass -File ""{app}\installer\windows\post_install.ps1"" {code:GetInstallArgs}"; WorkingDir: "{app}"; Flags: waituntilterminated

[Code]
function GetInstallArgs(Param: String): String;
begin
  Result := '--model mistral:7b --wait-ollama-seconds 20';

  if not WizardIsTaskSelected('installmodel') then
    Result := Result + ' --skip-models';

  if WizardIsTaskSelected('launchapp') then
    Result := Result + ' --launch-app';
end;
