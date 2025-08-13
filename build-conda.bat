@echo off
chcp 65001 >nul
REM 注意：不要使用 setlocal，否则 conda activate 的环境改变不会在父脚本中保留

echo ========================================
echo Conda Environment Setup Script
echo ========================================
echo.

REM 1) Locate conda.bat
set "CONDA_CMD="

REM Try multiple possible conda paths
if exist "%USERPROFILE%\anaconda3\Scripts\conda.bat" (
  set "CONDA_CMD=%USERPROFILE%\anaconda3\Scripts\conda.bat"
) else if exist "%USERPROFILE%\miniconda3\Scripts\conda.bat" (
  set "CONDA_CMD=%USERPROFILE%\miniconda3\Scripts\conda.bat"
) else if exist "C:\ProgramData\Anaconda3\Scripts\conda.bat" (
  set "CONDA_CMD=C:\ProgramData\Anaconda3\Scripts\conda.bat"
) else (
  REM Try where command as fallback
  for /f "delims=" %%i in ('where conda 2^>nul') do (
    set "CONDA_CMD=%%i"
    goto :found_conda
  )
  echo ERROR: conda not detected, please install Anaconda/Miniconda and add it to PATH.
  echo Reference: https://docs.conda.io/
  exit /b 1
)

:found_conda
echo Found conda at: %CONDA_CMD%
echo.
REM 2) Parse default environment name (from name: field in HTTP\environment.yml)
set "DEFAULT_ENV_NAME="

REM Check if environment.yml exists
if not exist "HTTP\environment.yml" (
  echo WARNING: HTTP\environment.yml not found, using default name
  set "DEFAULT_ENV_NAME=NWT"
) else (
  echo Found environment.yml file, parsing name...
  for /f "tokens=2 delims=:" %%n in ('findstr /B /C:"name:" "HTTP\environment.yml" 2^>nul') do (
    set "DEFAULT_ENV_NAME=%%n"
  )
)

if not defined DEFAULT_ENV_NAME set "DEFAULT_ENV_NAME=NWT"
REM Remove leading/trailing spaces
set "DEFAULT_ENV_NAME=%DEFAULT_ENV_NAME: =%"
echo Detected default environment name: %DEFAULT_ENV_NAME%
echo.

REM Tool: Check if environment exists
:check_env_exists
REM Usage: call :check_env_exists ENVNAME  —— Returns 0 if exists / 1 if not exists via errorlevel

REM Create temp file in current directory instead of %TEMP%
set "TEMP_FILE=conda_envs_temp.txt"
call "%CONDA_CMD%" env list > "%TEMP_FILE%" 2>nul
if exist "%TEMP_FILE%" (
  findstr /R /I /C:"^[ ]*%~1[ ]" "%TEMP_FILE%" >nul
  set "ENV_EXISTS=%errorlevel%"
  del "%TEMP_FILE%" 2>nul
  if !ENV_EXISTS! equ 0 (
    exit /b 0
  ) else (
    exit /b 1
  )
) else (
  echo ERROR: Failed to create temporary file for environment check
  exit /b 1
)

REM 3) Check if default environment already exists
call :check_env_exists %DEFAULT_ENV_NAME%
if %errorlevel% equ 0 (
  echo Found existing Conda environment with same name: %DEFAULT_ENV_NAME%
  choice /C YN /M "Use existing environment? (Y=Use, N=Create new)"
  if errorlevel 2 goto ask_new_name
  set "ENV_NAME=%DEFAULT_ENV_NAME%"
  goto create_or_activate
) else (
  set "ENV_NAME=%DEFAULT_ENV_NAME%"
  goto create_or_activate
)

:ask_new_name
:input_loop
set "ENV_NAME="
set /p ENV_NAME=Enter new environment name (letters/numbers/underscores/hyphens only): 
if "%ENV_NAME%"=="" (
  echo Environment name cannot be empty, please re-enter.
  goto input_loop
)
call :check_env_exists %ENV_NAME%
if %errorlevel% equ 0 (
  echo This environment name already exists, please re-enter.
  goto input_loop
)

:create_or_activate
REM 4) Create environment if it doesn't exist; activate if it exists
call :check_env_exists %ENV_NAME%
if %errorlevel% neq 0 (
  echo.
  echo Creating environment "%ENV_NAME%" using HTTP\environment.yml...
  call "%CONDA_CMD%" env create -n "%ENV_NAME%" -f "HTTP\environment.yml" -y
  if %errorlevel% neq 0 (
    echo ERROR: Failed to create Conda environment.
    exit /b 1
  )
  echo Environment "%ENV_NAME%" created successfully ✓
) else (
  echo.
  echo Using existing environment "%ENV_NAME%"...
)

REM 5) Activate environment (effective in current session, for use by subsequent scripts)
call "%CONDA_CMD%" activate "%ENV_NAME%"
if %errorlevel% neq 0 (
  echo ERROR: Failed to activate environment.
  exit /b 1
)
set "CONDA_ENV_NAME=%ENV_NAME%"
echo.
echo Conda environment activated: %ENV_NAME%
python --version 2>nul
echo.
exit /b 0