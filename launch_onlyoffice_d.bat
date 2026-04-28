@echo off
:: OnlyOffice Optimized Launcher - D: Drive
start "" /HIGH "D:\Projects\OnlyOffice\app\DesktopEditors.exe" ^
    --no-proxy-server ^
    --disable-gpu-compositing ^
    --renderer-process-limit=1 ^
    --disable-background-networking ^
    --disable-default-apps ^
    --disable-extensions ^
    --disable-sync ^
    --disable-translate ^
    --no-first-run ^
    --disable-component-update ^
    --disable-background-timer-throttling ^
    --disable-renderer-backgrounding ^
    --disable-backgrounding-occluded-windows ^
    --disable-hang-monitor ^
    --disable-domain-reliability ^
    --disable-client-side-phishing-detection ^
    --disable-features=TranslateUI,BlinkGenPropertyTrees,AudioServiceOutOfProcess,CalculateNativeWinOcclusion,WinRetrieveSuggestionsOnlyOnDemand ^
    --process-per-site ^
    --disable-logging ^
    --disable-breakpad ^
    --disable-component-extensions-with-background-pages ^
    --disable-ipc-flooding-protection ^
    --enable-simple-cache-backend ^
    --disable-smooth-scrolling ^
    --disable-spell-checking ^
    --disable-notifications ^
    --disable-speech-api ^
    --disable-speech-synthesis-api ^
    --enable-low-end-device-mode ^
    --js-flags="--max-old-space-size=256 --optimize-for-size --gc-interval=100 --lite-mode" ^
    %*
