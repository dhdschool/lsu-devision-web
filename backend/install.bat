@echo off

:: run as admin required
net session >nul 2>&1
if %errorLevel% NEQ 0 (
    echo Please run this script as Administrator.
    pause
    exit /b 1
)


where wsl >nul 2>&1
IF %ERRORLEVEL% EQU 0 (
    echo wsl is installed...
) ELSE (
    :: Enable wsl download
    dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart
    dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart

    :: Install wsl
    wsl --install -d Ubuntu
)
:: Install docker
where "Docker Desktop.exe" >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Installing docker desktop

    set "dockerInstaller=%TEMP%\DockerDesktopInstaller.exe"

    if exist "%dockerInstaller%" del /f /q "%dockerInstaller%"

    powershell -Command "https://desktop.docker.com/win/main/amd64/Docker%20Desktop%20Installer.exe" `
        -OutFile $dockerInstaller `
        -UseBasicParsing `
        -Headers @{'User-Agent' = 'Mozilla/5.0'}

    echo Installing Docker Desktop silently...
    "%dockerInstaller%" install --quiet

    echo Please restart your computer
    pause
    exit /b 0
)

:: Run docker desktop
powershell -Command "Get-Process -Name 'Docker Desktop' -ErrorAction SilentlyContinue" >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Starting Docker Desktop...
    start "" "C:\Program Files\Docker\Docker\Docker Desktop.exe"
    echo Waiting for Docker to start...
    timeout /t 20 /nobreak >nul
)

:: Wait for docker desktop
set /a retries=0
:waitdocker
docker info >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    if %retries% GEQ 12 (
        echo Docker daemon not responding after 60 seconds. Exiting.
        pause
        exit /b 1
    )
    set /a retries+=1
    timeout /t 5 >nul
    goto waitdocker
)

docker pull ghcr.io/dhdschool/backend-web:latest
docker pull ghcr.io/dhdschool/backend-celery:latest

:: Build and run docker container
docker compose -f docker-compose.yml up -d --pull always

if %ERRORLEVEL% NEQ 0 (
    echo Docker Compose failed to start containers.
    pause
    exit /b 1
)

echo Backend running at http://localhost:8000
echo To stop containers: docker-compose down

pause
endlocal

