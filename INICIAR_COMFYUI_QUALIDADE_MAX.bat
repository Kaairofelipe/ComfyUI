@echo off
title ComfyUI - MODO QUALIDADE MAXIMA - RTX 2060 6GB
color 0E

echo ============================================================
echo   ComfyUI - QUALIDADE MAXIMA
echo   RTX 2060 6GB ^| CUDA 12.4 ^| xformers
echo   ATENCAO: Pode usar mais VRAM - feche outros programas
echo ============================================================
echo.

:: Fechar processos que consomem VRAM (opcional)
:: taskkill /f /im chrome.exe 2>nul

set KMP_DUPLICATE_LIB_OK=TRUE
set CUDA_VISIBLE_DEVICES=0
set PYTORCH_CUDA_ALLOC_CONF=garbage_collection_threshold:0.6,max_split_size_mb:1024
set SSL_CERT_FILE=D:\Kalainne_AI_Suite\envs\comfyui\Lib\site-packages\certifi\cacert.pem
set REQUESTS_CA_BUNDLE=D:\Kalainne_AI_Suite\envs\comfyui\Lib\site-packages\certifi\cacert.pem

cd /d "D:\GitHub_Local\ComfyUI"

echo [INFO] Modo Qualidade Maxima - sem lowvram
echo [INFO] Recomendado para modelos SD1.5 e SDXL com LoRAs
echo.

"D:\Kalainne_AI_Suite\envs\comfyui\python.exe" main.py ^
    --preview-method auto ^
    --fp16-vae ^
    --listen 0.0.0.0 ^
    --port 8188

echo.
echo [INFO] ComfyUI encerrado.
pause
