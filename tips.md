# ComfyUI: Fixing Common Installation and Import Issues

## Introduction

Many users, especially those new to ComfyUI, encounter frustrating issues when trying to get it to work correctly. These often stem from a few core problems related to Python environments, package locations, and dependency conflicts. This guide will walk you through the process we used to solve these issues step-by-step so that you can avoid the same problems.

## Common Problems

- **Python packages installing to the wrong locations**: This is the most common problem and it happens when packages are installed into your user's Python environment (usually in AppData/Roaming) instead of ComfyUI's embedded environment. This leads to import failures and conflicts.
- **Conflicts between system Python and ComfyUI's embedded Python**: If you have other Python installations on your system, they can interfere with ComfyUI's setup, causing errors.
- **Custom nodes failing to import due to missing dependencies**: Many ComfyUI custom nodes require specific Python packages. If these are missing or in the wrong location, the nodes won't load.
- **FFMPEG warnings and video processing issues**: If you're planning to work with videos in ComfyUI, FFMPEG needs to be correctly installed and configured. This often causes warnings when not properly set up.

## Step-by-Step Solutions

### 1. Prevent Python Packages from Installing to the Wrong Location

The first step is to create a `pip.ini` file. This will tell pip (the Python package installer) to install packages in the active Python environment, instead of your user's folder.

1. **Open PowerShell.**
2. **Create the pip directory**: Copy and paste this command into PowerShell and press Enter:
    ```powershell
    New-Item -ItemType Directory -Force -Path "$env:APPDATA\pip"
    ```
3. **Create the pip.ini file with the correct settings**: Copy and paste this command into PowerShell and press Enter:
    ```powershell
    @"
    [global]
    user = false
    "@ | Out-File -FilePath "$env:APPDATA\pip\pip.ini" -Encoding UTF8
    ```
4. **Verify**: To make sure it worked, you can copy and paste this command into PowerShell and press Enter:
    ```powershell
    Get-Content "$env:APPDATA\pip\pip.ini"
    ```
    You should see the text:
    ```
    [global]
    user = false
    ```

What this does: This will prevent packages from being installed in your user's roaming folder and ensure they get installed into the active Python environment, which is ComfyUI's.

### 2. Set Up a Proper Python Environment for ComfyUI

To make sure ComfyUI uses its embedded Python and the packages you install, you will need to create a startup script.

1. **Open Notepad (or another text editor).**
2. **Copy and paste the following code into the text editor:**
    ```batch
    @echo off
    setlocal
    :: Set environment variables to ignore user site packages and set correct path
    set PYTHONNOUSERSITE=1
    set PYTHONPATH=%~dp0python_embeded\Lib\site-packages
    :: Start ComfyUI
    .\python_embeded\python.exe -s ComfyUI\main.py --windows-standalone-build
    endlocal
    ```
3. **Save the file as `start_comfyui.bat` in your ComfyUI main directory (where `ComfyUI\main.py` is located).**
4. **Run ComfyUI using this batch file instead of running the Python command directly.**

What this does: This script sets environment variables to tell Python to ignore the user's site-packages and to use ComfyUI's embedded Python and its site-packages folder, before starting ComfyUI.

### 3. Install FFMPEG Properly

If you plan to use video within ComfyUI, it's important that FFMPEG is properly installed.

1. **Download FFMPEG**: Go to [https://www.gyan.dev/ffmpeg/builds/](https://www.gyan.dev/ffmpeg/builds/) and download the full `ffmpeg-git-full.7z` file.
2. **Create a directory**: Inside will be a folder like `ffmpeg-git-YYYY-MM-DD-full`, rename it to just `ffmpeg` (`C:\ffmpeg`).
    ```powershell
    New-Item -ItemType Directory -Path "C:\ffmpeg" -Force
    ```
3. **Extract the contents**: Extract the contents of the downloaded file to `C:\ffmpeg` so that `ffmpeg.exe` ends up in `C:\ffmpeg\bin\ffmpeg.exe`.
4. **Verify**: Check to see that it is in the proper place by copying and pasting the following command into PowerShell and press Enter:
    ```powershell
    Test-Path "C:\ffmpeg\bin\ffmpeg.exe"
    ```
    This should return `True`.

5. **Set the FFMPEG System PATH**:
    - Open PowerShell as an Administrator (right-click and select "Run as Administrator").
    - Copy and paste this command into PowerShell and press Enter:
        ```powershell
        [Environment]::SetEnvironmentVariable("Path", $env:Path + ";C:\ffmpeg\bin", [EnvironmentVariableTarget]::Machine)
        ```
    - Close and reopen PowerShell as Admin to verify that it works by copying and pasting this command into PowerShell and press Enter:
        ```powershell
        ffmpeg -version
        ```
        This should show the FFMPEG version details.

What this does: This sets up a dedicated installation of FFMPEG and adds it to the system path so that both ComfyUI and other applications can access it.

### Configure ComfyUI to Use FFMPEG

Now, you need to tell the WAS Node Suite (if you use it) where to find FFMPEG.

1. Locate the `was_suite_config.json` file in your ComfyUI custom nodes directory:
    ```
    E:\ComfyUI_windows_portable\ComfyUI\custom_nodes\was-node-suite-comfyui\was_suite_config.json
    ```
2. Open the file in a text editor.
3. Find the line that says:
    ```json
    {
        "ffmpeg_bin_path": "/path/to/ffmpeg"
    }
    ```
4. Replace it with:
    ```json
    {
        "ffmpeg_bin_path": "C:/ffmpeg/bin/ffmpeg.exe"
    }
    ```
    *Note: Use forward slashes `/` instead of backslashes `\` even on Windows, and ensure that you keep the commas and other formatting of the file the same.*

5. Save the `was_suite_config.json` file.

What this does: This tells ComfyUI's WAS Node Suite where to find your FFMPEG installation.

## Verification Steps

After making these changes, it's important to verify that your setup is working correctly.

1. **Check FFMPEG is accessible**: Open PowerShell (as Admin) and run `ffmpeg -version`.
2. **Verify Python packages install to the correct location**: Install a small test package:
    ```powershell
    .\python_embeded\python.exe -m pip install emoji
    ```
    and check where it is located:
    ```powershell
    .\python_embeded\python.exe -c "import emoji; print(emoji.__file__)"
    ```
    It should be in ComfyUI's folder.
3. **Start ComfyUI using the `start_comfyui.bat` file and check the logs**:
    - There should be no import errors for custom nodes.
    - There should be no FFMPEG warnings.
    - GPU acceleration should be enabled ("Using cuda:0" in the logs).

## Tips for Future Installations

- Always use the `start_comfyui.bat` file to launch ComfyUI.
- Install new dependencies using ComfyUI's embedded Python. For example:
    ```powershell
    .\python_embeded\python.exe -m pip install [package_name]
    ```
- When installing custom nodes, check their dependencies and install them as described above.
- After making changes it may be necessary to shut down ComfyUI and restart using `start_comfyui.bat`.

## Common Error Messages and Solutions

- **"ModuleNotFoundError: No module named 'xyz'"**:
    Install the missing package using ComfyUI's embedded Python:
    ```powershell
    .\python_embeded\python.exe -m pip install [package_name]
    ```
- **"Cannot import module for custom nodes"**:
    - Verify that all dependencies are installed in ComfyUI's embedded Python environment.
    - Check for conflicting versions of packages.
- **"FFMPEG warning"**:
    - Double-check that FFMPEG is correctly installed in `C:\ffmpeg\bin`.
    - Double-check that `was_suite_config.json` has the correct path:
        ```json
        "ffmpeg_bin_path": "C:/ffmpeg/bin/ffmpeg.exe"
        ```
    - Ensure that FFMPEG is added to the system PATH.
- **"DWPose: Onnxruntime not found"**:
    Install the GPU version of onnxruntime:
    ```powershell
    .\python_embeded\python.exe -m pip install onnxruntime-gpu
    ```

I was able to solve all these problems and more simply by asking Claude 3.5 Sonnet how to fix them. Specifically, I would copy in the full text of any error I received and asked what was wrong and how to fix it. Claude Sonnet is extremely good with solving code issues, but as with any Chatbot or model, it might make mistakes. If and when it does, let it know and correct it. Don’t worry, you won’t hurt its feelings.

By following these steps carefully, you should be able to resolve many common issues with ComfyUI. If you still encounter problems, carefully double-check each step, as a small mistake can lead to unexpected results. Remember to install packages using ComfyUI's embedded Python and not your system Python. Let me know if you would like to add to the document for clarity or anything.

## Disclaimer

I am not a professional programmer. The information in this guide is provided “as is” and is based on my own experiences and troubleshooting. I make no guarantees regarding its accuracy or applicability to your specific setup. By following this guide, you assume all risks associated with implementation and agree that I cannot be held liable for any damages, issues, or losses arising from its use. Always perform backups and use your own judgment when making changes to your system, as your mileage may vary.