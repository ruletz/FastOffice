; Inno Setup Script for OnlyOffice High-Performance Edition (ruletzz Edition)

[Setup]
AppName=OnlyOffice High-Performance Edition
AppVersion=1.0
AppPublisher=ruletzz
DefaultDirName={autopf}\OnlyOfficeOptimized
DefaultGroupName=OnlyOffice High-Performance Edition
AllowNoIcons=yes
OutputDir=.
OutputBaseFilename=OnlyOffice_Optimized_v1_Setup
Compression=lzma
SolidCompression=yes
ArchitecturesAllowed=x64
ArchitecturesInstallIn64BitMode=x64

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"
Name: "portuguese"; MessagesFile: "compiler:Languages\Portuguese.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "C:\Projects\OnlyOffice\app\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\OnlyOffice Optimized"; Filename: "{app}\DesktopEditors.exe"; Parameters: "--no-proxy-server --disable-gpu-compositing --renderer-process-limit=1 --disable-background-networking --disable-default-apps --disable-extensions --disable-sync --disable-translate --no-first-run --disable-component-update --disable-background-timer-throttling --disable-renderer-backgrounding --disable-backgrounding-occluded-windows --disable-hang-monitor --disable-domain-reliability --disable-client-side-phishing-detection --disable-features=TranslateUI,BlinkGenPropertyTrees,AudioServiceOutOfProcess,CalculateNativeWinOcclusion,WinRetrieveSuggestionsOnlyOnDemand,MediaRouter,OptimizationHints,InterestFeedContentSuggestions --process-per-site --disable-logging --disable-breakpad --disable-component-extensions-with-background-pages --disable-ipc-flooding-protection --enable-simple-cache-backend --disable-smooth-scrolling --disable-spell-checking --disable-notifications --disable-speech-api --disable-speech-synthesis-api --enable-low-end-device-mode --js-flags=""--max-old-space-size=512 --optimize-for-size --max-semi-space-size=4"""
Name: "{autodesktop}\OnlyOffice Optimized"; Filename: "{app}\DesktopEditors.exe"; Parameters: "--no-proxy-server --disable-gpu-compositing --renderer-process-limit=1 --disable-background-networking --disable-default-apps --disable-extensions --disable-sync --disable-translate --no-first-run --disable-component-update --disable-background-timer-throttling --disable-renderer-backgrounding --disable-backgrounding-occluded-windows --disable-hang-monitor --disable-domain-reliability --disable-client-side-phishing-detection --disable-features=TranslateUI,BlinkGenPropertyTrees,AudioServiceOutOfProcess,CalculateNativeWinOcclusion,WinRetrieveSuggestionsOnlyOnDemand,MediaRouter,OptimizationHints,InterestFeedContentSuggestions --process-per-site --disable-logging --disable-breakpad --disable-component-extensions-with-background-pages --disable-ipc-flooding-protection --enable-simple-cache-backend --disable-smooth-scrolling --disable-spell-checking --disable-notifications --disable-speech-api --disable-speech-synthesis-api --enable-low-end-device-mode --js-flags=""--max-old-space-size=512 --optimize-for-size --max-semi-space-size=4"""; Tasks: desktopicon

[Run]
Filename: "{app}\DesktopEditors.exe"; Parameters: "--no-proxy-server --disable-gpu-compositing --renderer-process-limit=1 --disable-background-networking --disable-default-apps --disable-extensions --disable-sync --disable-translate --no-first-run --disable-component-update --disable-background-timer-throttling --disable-renderer-backgrounding --disable-backgrounding-occluded-windows --disable-hang-monitor --disable-domain-reliability --disable-client-side-phishing-detection --disable-features=TranslateUI,BlinkGenPropertyTrees,AudioServiceOutOfProcess,CalculateNativeWinOcclusion,WinRetrieveSuggestionsOnlyOnDemand,MediaRouter,OptimizationHints,InterestFeedContentSuggestions --process-per-site --disable-logging --disable-breakpad --disable-component-extensions-with-background-pages --disable-ipc-flooding-protection --enable-simple-cache-backend --disable-smooth-scrolling --disable-spell-checking --disable-notifications --disable-speech-api --disable-speech-synthesis-api --enable-low-end-device-mode --js-flags=""--max-old-space-size=512 --optimize-for-size --max-semi-space-size=4"""; Description: "{cm:LaunchProgram,OnlyOffice Optimized}"; Flags: nowait postinstall skipifsilent

[Registry]
; File associations for .docx
Root: HKA; Subkey: "Software\Classes\.docx"; ValueType: string; ValueName: ""; ValueData: "OnlyOffice.Docx"; Flags: uninsdeletevalue
Root: HKA; Subkey: "Software\Classes\OnlyOffice.Docx"; ValueType: string; ValueName: ""; ValueData: "Word Document (Optimized)"; Flags: uninsdeletekey
Root: HKA; Subkey: "Software\Classes\OnlyOffice.Docx\DefaultIcon"; ValueType: string; ValueName: ""; ValueData: "{app}\DesktopEditors.exe,0"
Root: HKA; Subkey: "Software\Classes\OnlyOffice.Docx\shell\open\command"; ValueType: string; ValueName: ""; ValueData: """{app}\DesktopEditors.exe"" --no-proxy-server --disable-gpu-compositing --renderer-process-limit=1 --disable-background-networking --disable-default-apps --disable-extensions --disable-sync --disable-translate --no-first-run --disable-component-update --disable-background-timer-throttling --disable-renderer-backgrounding --disable-backgrounding-occluded-windows --disable-hang-monitor --disable-domain-reliability --disable-client-side-phishing-detection --disable-features=TranslateUI,BlinkGenPropertyTrees,AudioServiceOutOfProcess,CalculateNativeWinOcclusion,WinRetrieveSuggestionsOnlyOnDemand,MediaRouter,OptimizationHints,InterestFeedContentSuggestions --process-per-site --disable-logging --disable-breakpad --disable-component-extensions-with-background-pages --disable-ipc-flooding-protection --enable-simple-cache-backend --disable-smooth-scrolling --disable-spell-checking --disable-notifications --disable-speech-api --disable-speech-synthesis-api --enable-low-end-device-mode --js-flags=""--max-old-space-size=512 --optimize-for-size --max-semi-space-size=4"" ""%1"""

; File associations for .xlsx
Root: HKA; Subkey: "Software\Classes\.xlsx"; ValueType: string; ValueName: ""; ValueData: "OnlyOffice.Xlsx"; Flags: uninsdeletevalue
Root: HKA; Subkey: "Software\Classes\OnlyOffice.Xlsx"; ValueType: string; ValueName: ""; ValueData: "Excel Spreadsheet (Optimized)"; Flags: uninsdeletekey
Root: HKA; Subkey: "Software\Classes\OnlyOffice.Xlsx\DefaultIcon"; ValueType: string; ValueName: ""; ValueData: "{app}\DesktopEditors.exe,0"
Root: HKA; Subkey: "Software\Classes\OnlyOffice.Xlsx\shell\open\command"; ValueType: string; ValueName: ""; ValueData: """{app}\DesktopEditors.exe"" --no-proxy-server --disable-gpu-compositing --renderer-process-limit=1 --disable-background-networking --disable-default-apps --disable-extensions --disable-sync --disable-translate --no-first-run --disable-component-update --disable-background-timer-throttling --disable-renderer-backgrounding --disable-backgrounding-occluded-windows --disable-hang-monitor --disable-domain-reliability --disable-client-side-phishing-detection --disable-features=TranslateUI,BlinkGenPropertyTrees,AudioServiceOutOfProcess,CalculateNativeWinOcclusion,WinRetrieveSuggestionsOnlyOnDemand,MediaRouter,OptimizationHints,InterestFeedContentSuggestions --process-per-site --disable-logging --disable-breakpad --disable-component-extensions-with-background-pages --disable-ipc-flooding-protection --enable-simple-cache-backend --disable-smooth-scrolling --disable-spell-checking --disable-notifications --disable-speech-api --disable-speech-synthesis-api --enable-low-end-device-mode --js-flags=""--max-old-space-size=512 --optimize-for-size --max-semi-space-size=4"" ""%1"""

; File associations for .pptx
Root: HKA; Subkey: "Software\Classes\.pptx"; ValueType: string; ValueName: ""; ValueData: "OnlyOffice.Pptx"; Flags: uninsdeletevalue
Root: HKA; Subkey: "Software\Classes\OnlyOffice.Pptx"; ValueType: string; ValueName: ""; ValueData: "PowerPoint Presentation (Optimized)"; Flags: uninsdeletekey
Root: HKA; Subkey: "Software\Classes\OnlyOffice.Pptx\DefaultIcon"; ValueType: string; ValueName: ""; ValueData: "{app}\DesktopEditors.exe,0"
Root: HKA; Subkey: "Software\Classes\OnlyOffice.Pptx\shell\open\command"; ValueType: string; ValueName: ""; ValueData: """{app}\DesktopEditors.exe"" --no-proxy-server --disable-gpu-compositing --renderer-process-limit=1 --disable-background-networking --disable-default-apps --disable-extensions --disable-sync --disable-translate --no-first-run --disable-component-update --disable-background-timer-throttling --disable-renderer-backgrounding --disable-backgrounding-occluded-windows --disable-hang-monitor --disable-domain-reliability --disable-client-side-phishing-detection --disable-features=TranslateUI,BlinkGenPropertyTrees,AudioServiceOutOfProcess,CalculateNativeWinOcclusion,WinRetrieveSuggestionsOnlyOnDemand,MediaRouter,OptimizationHints,InterestFeedContentSuggestions --process-per-site --disable-logging --disable-breakpad --disable-component-extensions-with-background-pages --disable-ipc-flooding-protection --enable-simple-cache-backend --disable-smooth-scrolling --disable-spell-checking --disable-notifications --disable-speech-api --disable-speech-synthesis-api --enable-low-end-device-mode --js-flags=""--max-old-space-size=512 --optimize-for-size --max-semi-space-size=4"" ""%1"""
