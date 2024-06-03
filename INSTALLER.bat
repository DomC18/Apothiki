@echo off
setlocal

:: Define Python download URL and installer name
set PYTHON_URL=https://www.python.org/ftp/python/3.12.3/python-3.12.3-amd64.exe
set PYTHON_INSTALLER=python-installer.exe
set PYTHON_SCRIPT=main.py
set SCRIPT_DIR=%~dp0\main.py
set MAIN_DIR=%~dp0

:: Define the name and path for the shortcut
set SHORTCUT_NAME=Apothiki
set SHORTCUT_PATH=%USERPROFILE%\Desktop\%SHORTCUT_NAME%.lnk

:: Download the latest Python installer
echo Downloading Python...
powershell -Command "Invoke-WebRequest -Uri %PYTHON_URL% -OutFile %PYTHON_INSTALLER%"

:: Install Python silently
echo Installing Python...
%PYTHON_INSTALLER% /quiet InstallAllUsers=1 PrependPath=1

:: Verify Python installation
echo Verifying Python installation...
python --version
if errorlevel 1 (
    echo Python installation failed.
    exit /b 1
)

:: Upgrade pip to the latest version
echo Upgrading pip...
python -m pip install --upgrade pip

:: Install the Pillow module
echo Installing Pillow...
python -m pip install Pillow

:: Clean up the installer
del %PYTHON_INSTALLER%

:: Create a desktop shortcut to run the script again
echo Creating a desktop shortcut...
powershell -Command "$WshShell = New-Object -ComObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%SHORTCUT_PATH%'); $Shortcut.TargetPath = '%MAIN_DIR%main.py'; $Shortcut.WorkingDirectory = '%MAIN_DIR%'; $Shortcut.IconLocation = 'python.exe,0'; $Shortcut.Save()"

powershell -Command clear
echo Python and Pillow have been installed successfully.
echo Desktop shortcut has been created, named Apothiki.

endlocal
pause
