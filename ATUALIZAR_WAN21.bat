@echo off
title Atualizar Wan2.1 - Geracao de Video
color 09

echo ============================================================
echo   Atualizando Wan2.1 - Geracao de Video
echo   Ambiente: D:\Kalainne_AI_Suite\envs\comfyui
echo ============================================================
echo.

:: ============================================================
echo [1/2] Atualizando codigo Wan2.1 (git pull)...
cd /d "C:\Users\KairoFelipe\Wan2.1"
git pull
if errorlevel 1 (
    echo [AVISO] git pull retornou erro - verifique conexao ou conflitos.
) else (
    echo [OK] Wan2.1 codigo atualizado.
)
echo.

:: ============================================================
echo [2/2] Atualizando dependencias Wan2.1...
if exist requirements.txt (
    "D:\Kalainne_AI_Suite\envs\comfyui\Scripts\pip.exe" install -r requirements.txt --upgrade
    if errorlevel 1 (
        echo [AVISO] Erro ao atualizar dependencias.
    ) else (
        echo [OK] Dependencias atualizadas.
    )
) else (
    echo [INFO] Nenhum requirements.txt encontrado em C:\Users\KairoFelipe\Wan2.1
)
echo.

echo ============================================================
echo   Wan2.1 atualizado!
echo   Para usar no ComfyUI, instale via Manager: ComfyUI-WanVideoWrapper
echo ============================================================
pause
