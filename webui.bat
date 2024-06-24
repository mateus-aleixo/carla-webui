@echo off

REM Especifique manualmente o caminho para o CarlaUE4.exe
set CARLA_PATH=C:\Caminho\Para\CarlaUE4.exe

if not exist "%CARLA_PATH%" (
    echo Erro: Simulador CARLA nao encontrado.
    exit /b 1
)

REM Inicia o simulador CARLA em segundo plano
start "" /min "%CARLA_PATH%" -quality-level=Low

REM Aguarda 10 segundos para o CARLA inicializar
timeout /t 10 /nobreak >nul

REM Ativa o ambiente conda carla-webui
call conda activate carla-webui
if errorlevel 1 (
    echo Erro ao ativar o ambiente conda.
    exit /b 1
)

REM Inicia o servidor em segundo plano
start /min cmd /c "python server\main.py"

REM Aguarda um pouco para dar tempo do servidor iniciar
timeout /t 5 /nobreak >nul

REM Inicia o cliente em segundo plano
start /min cmd /c "cd client && npm run dev"

REM Aguarda um pouco para dar tempo do cliente iniciar
timeout /t 5 /nobreak >nul

REM Abre o navegador na URL http://localhost:5173/
start "" "http://localhost:5173/"
