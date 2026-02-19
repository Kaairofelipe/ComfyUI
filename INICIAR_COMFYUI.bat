@echo off
title ComfyUI - RTX 2060 6GB - CUDA 12.4
color 0A

echo ============================================================
echo   ComfyUI v0.12.3 - Otimizado para RTX 2060 ^(6GB VRAM^)
echo   PyTorch 2.6.0 + CUDA 12.4 + xformers
echo   Ambiente: D:\Kalainne_AI_Suite\envs\comfyui
echo ============================================================
echo.

:: Configurar variaveis de ambiente para performance
set PYTHONPATH=D:\GitHub_Local\ComfyUI
set KMP_DUPLICATE_LIB_OK=TRUE
set CUDA_VISIBLE_DEVICES=0
set PYTORCH_CUDA_ALLOC_CONF=garbage_collection_threshold:0.6,max_split_size_mb:512
:: Corrigir SSL (certificados corporativos Windows podem causar erro)
set SSL_CERT_FILE=D:\Kalainne_AI_Suite\envs\comfyui\Lib\site-packages\certifi\cacert.pem
set REQUESTS_CA_BUNDLE=D:\Kalainne_AI_Suite\envs\comfyui\Lib\site-packages\certifi\cacert.pem

:: Diretorio do ComfyUI
cd /d "D:\GitHub_Local\ComfyUI"

echo [INFO] Iniciando ComfyUI com otimizacoes para RTX 2060...
echo [INFO] VRAM: 6GB - Usando --lowvram e --xformers
echo.

:: Iniciar ComfyUI com configuracoes otimizadas para 6GB VRAM
:: xformers e detectado automaticamente quando instalado
:: --preview-method auto: previews durante geracao
:: --lowvram: otimiza para GPUs com 4-8GB VRAM
:: --fp16-vae: VAE em fp16 para economizar VRAM
"D:\Kalainne_AI_Suite\envs\comfyui\python.exe" main.py ^
    --preview-method auto ^
    --fp16-vae ^
    --lowvram ^
    --listen 0.0.0.0 ^
    --port 8188 ^
    --windows-standalone-build

echo.
echo [INFO] ComfyUI encerrado.
pause
