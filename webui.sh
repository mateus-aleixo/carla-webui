#!/bin/bash

# Especifique manualmente o caminho para o CarlaUE4.exe
CARLA_PATH="/caminho/para/CarlaUE4.exe"

if [ ! -f "$CARLA_PATH" ]; then
    echo "Erro: Simulador CARLA nao encontrado."
    exit 1
fi

# Inicia o simulador CARLA em segundo plano
"$CARLA_PATH" -quality-level=Low &

# Aguarda 10 segundos para o CARLA inicializar
sleep 10

# Ativa o ambiente conda carla-webui
source $(conda info --base)/etc/profile.d/conda.sh
conda activate carla-webui
if [ $? -ne 0 ]; then
    echo "Erro ao ativar o ambiente conda."
    exit 1
fi

# Inicia o servidor em segundo plano
python3 server/main.py &

# Inicia o cliente em segundo plano
(cd client && npm run dev) &

# Aguarda um pouco para dar tempo do cliente iniciar
sleep 5

# Abre o navegador na URL http://localhost:5173/
xdg-open http://localhost:5173/ || open http://localhost:5173/ || sensible-browser http://localhost:5173/
