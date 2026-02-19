# Modelos Recomendados para RTX 2060 (6GB VRAM)
## ComfyUI v0.12.3 | PyTorch 2.6.0+cu124 | xformers

---

## ONDE COLOCAR OS MODELOS

| Tipo | Pasta |
|------|-------|
| Modelos principais (.safetensors) | `D:\GitHub_Local\ComfyUI\models\checkpoints\` |
| VAE | `D:\GitHub_Local\ComfyUI\models\vae\` |
| LoRAs | `D:\GitHub_Local\ComfyUI\models\loras\` |
| ControlNet | `D:\GitHub_Local\ComfyUI\models\controlnet\` |
| Upscalers | `D:\GitHub_Local\ComfyUI\models\upscale_models\` |
| CLIP/Text Encoders | `D:\GitHub_Local\ComfyUI\models\text_encoders\` |
| Modelos de difusão (FLUX, Wan) | `D:\GitHub_Local\ComfyUI\models\diffusion_models\` |

---

## MODELOS PARA IMAGENS

### Stable Diffusion 1.5 (Funciona OTIMO - 6GB VRAM)
- **Realistic Vision V6.0**: https://civitai.com/models/4201
- **DreamShaper v8**: https://civitai.com/models/4384
- **Anything V5**: https://civitai.com/models/9409

### SDXL (Funciona bem - pode precisar de --lowvram)
- **SDXL Base 1.0**: https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0
- **DreamShaper XL**: https://civitai.com/models/112902
- **Juggernaut XL**: https://civitai.com/models/133005

### FLUX.1 Schnell (Quantizado - funciona com 6GB)
- **FLUX.1-schnell GGUF Q4**: https://huggingface.co/city96/FLUX.1-schnell-gguf
  - Coloque em: `models/diffusion_models/`
  - Text encoder T5: `models/text_encoders/`
  - CLIP L: `models/text_encoders/`
  - VAE: `models/vae/`

---

## MODELOS PARA VIDEO

### Wan2.1 (Ja instalado o codigo em C:\Users\KairoFelipe\Wan2.1)
**PESOS DO MODELO** precisam ser baixados:
- Wan2.1 1.3B (text-to-video, funciona com 6GB):
  https://huggingface.co/Wan-AI/Wan2.1-T2V-1.3B
- Wan2.1 14B: Requer 20GB+ VRAM (incompativel com RTX 2060)

Para usar Wan2.1 NO COMFYUI, instale via ComfyUI Manager:
- Pesquise: "ComfyUI-WanVideoWrapper" ou "ComfyUI-Wan2.1"

---

## VAE RECOMENDADO (instalar sempre)
- **vae-ft-mse-840000-ema-pruned.safetensors** (para SD1.5)
  https://huggingface.co/stabilityai/sd-vae-ft-mse-original
- **sdxl_vae.safetensors** (para SDXL)
  https://huggingface.co/stabilityai/sdxl-vae

---

## UPSCALERS (pasta: models/upscale_models/)
- **4x-UltraSharp.pth**: https://civitai.com/models/116225 (Excelente qualidade)
- **4x_NMKD-Siax_200k.pth**: Para fotos realistas
- **RealESRGAN_x4plus.pth**: https://github.com/xinntao/Real-ESRGAN

---

## CONFIGURACAO OTIMA PARA RTX 2060

O script `INICIAR_COMFYUI.bat` ja usa:
- `--lowvram`: Descarrega da VRAM quando necessario
- `--fp16-vae`: VAE em half precision (economiza 2GB)
- `--preview-method auto`: Previews em tempo real
- SSL certificados corrigidos para Windows Enterprise
- KMP_DUPLICATE_LIB_OK=TRUE (resolve conflito OpenMP)
- PYTORCH_CUDA_ALLOC_CONF otimizado

Resolucoes possiveis com 6GB:
| Modelo | Resolucao Max |
|--------|---------------|
| SD 1.5 | 768x768 |
| SDXL | 1024x1024 (com lowvram) |
| FLUX schnell GGUF Q4 | 1024x1024 |
| Wan2.1 1.3B video | 480x832 (17 frames) |

---

## INICIAR O COMFYUI
Clique duplo em: `D:\GitHub_Local\ComfyUI\INICIAR_COMFYUI.bat`
Acesse no navegador: http://localhost:8188
