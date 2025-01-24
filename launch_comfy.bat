@echo off
cd X:\GitHub\comfy-cli
call .\.venv-py311\Scripts\activate.bat
comfy --workspace=X:\Diffusion\ComfyUI launch
pause