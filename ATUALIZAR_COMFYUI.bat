@echo off
title Atualizar ComfyUI e Dependencias
color 09

echo ============================================================
echo   Atualizando ComfyUI e Dependencias
echo   RTX 2060 ^| CUDA 12.4 ^| Kalainne AI Suite
echo ============================================================
echo.

cd /d "D:\GitHub_Local\ComfyUI"

:: ============================================================
echo [1/6] Atualizando ComfyUI (git pull)...
git pull
if errorlevel 1 (
    echo [AVISO] git pull retornou erro - verifique conexao ou conflitos.
) else (
    echo [OK] ComfyUI core atualizado.
)
echo.

:: ============================================================
echo [2/6] Atualizando dependencias principais...
"D:\Kalainne_AI_Suite\envs\comfyui\Scripts\pip.exe" install -r requirements.txt --upgrade
if errorlevel 1 (
    echo [AVISO] Erro ao atualizar dependencias principais.
) else (
    echo [OK] Dependencias atualizadas.
)
echo.

:: ============================================================
echo [3/6] Atualizando xformers (aceleracao RTX 2060)...
"D:\Kalainne_AI_Suite\envs\comfyui\Scripts\pip.exe" install xformers --upgrade
if errorlevel 1 (
    echo [AVISO] Erro ao atualizar xformers.
) else (
    echo [OK] xformers atualizado.
)
echo.

:: ============================================================
echo [4/6] Atualizando ComfyUI-Manager...
pushd "D:\GitHub_Local\ComfyUI\custom_nodes\ComfyUI-Manager"
git pull
"D:\Kalainne_AI_Suite\envs\comfyui\Scripts\pip.exe" install -r requirements.txt --upgrade
popd
echo [OK] ComfyUI-Manager atualizado.
echo.

:: ============================================================
echo [5/6] Atualizando todos os custom nodes instalados via git...
for /d %%G in ("D:\GitHub_Local\ComfyUI\custom_nodes\*") do (
    if exist "%%G\.git" (
        echo   -^> Atualizando: %%~nxG
        pushd "%%G"
        git pull
        popd
    )
)
echo [OK] Todos os custom nodes verificados.
echo.

:: ============================================================
echo [6/6] Verificando versoes instaladas...
"D:\Kalainne_AI_Suite\envs\comfyui\python.exe" -c "import torch, xformers; print('PyTorch  :', torch.__version__); print('CUDA     :', torch.cuda.is_available()); print('GPU      :', torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'N/A'); print('xformers :', xformers.__version__)"
echo.

echo ============================================================
echo   Atualizacao concluida com sucesso!
echo ============================================================
pause
