@echo off
chcp 65001 >nul
:: Obsidian文件夹打开器构建脚本
:: 用于本地构建exe文件

echo ========================================
echo Obsidian文件夹打开器构建脚本
echo ========================================
echo.

:: 检查Python是否安装
py --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未找到Python，请先安装Python 3.8+
    pause
    exit /b 1
)

echo [信息] Python已安装
py --version

echo [1/4] 安装依赖包...

:: 安装依赖
echo 正在安装项目依赖...
py -m pip install -r requirements.txt
if errorlevel 1 (
    echo [错误] 依赖安装失败
    echo 请尝试以下解决方案:
    echo 1. 重新创建虚拟环境: python -m venv .venv
    echo 2. 激活虚拟环境: .venv\Scripts\activate.bat
    echo 3. 手动安装: python -m pip install pyinstaller
    pause
    exit /b 1
)

echo.
echo [2/4] 清理旧的构建文件...
if exist dist rmdir /s /q dist
if exist build rmdir /s /q build
if exist *.spec del *.spec

echo.
echo [3/4] 构建可执行文件...

echo 正在构建主程序 (open_folder_with_obsidian.exe)...
if exist src\app-icon.ico (
    py -m PyInstaller --onefile --windowed --icon=src\app-icon.ico --name=open_folder_with_obsidian src/main.py
) else (
    echo [警告] 未找到src\app-icon.ico图标文件，使用默认图标
    py -m PyInstaller --onefile --windowed --name=open_folder_with_obsidian src/main.py
)
if errorlevel 1 (
    echo [错误] 主程序构建失败
    pause
    exit /b 1
)

echo 正在构建安装程序 (obsidian_installer.exe)...
if exist src\app-icon.ico (
    py -m PyInstaller --onefile --windowed --icon=src\app-icon.ico --name=obsidian_installer src/installer.py
) else (
    echo [警告] 未找到src\app-icon.ico图标文件，使用默认图标
    py -m PyInstaller --onefile --windowed --name=obsidian_installer src/installer.py
)
if errorlevel 1 (
    echo [错误] 安装程序构建失败
    pause
    exit /b 1
)

echo.
echo [4/4] 清理构建文件...

:: 清理build目录但保留dist目录
if exist build rmdir /s /q build
if exist *.spec del *.spec

:: 创建使用说明文件到dist目录
echo 创建使用说明文件...
(
echo Obsidian文件夹打开器
echo.
echo 构建时间: %date% %time%
echo.
echo 文件说明:
echo - open_folder_with_obsidian.exe: 主程序，用于打开文件夹
echo - obsidian_installer.exe: 安装程序，用于设置右键菜单
echo.
echo 使用方法:
echo 1. 以管理员身份运行 obsidian_installer.exe 进行安装
echo 2. 安装完成后即可在任意文件夹右键选择"用Obsidian打开"
echo.
echo 卸载方法:
echo 在Obsidian安装目录运行 remove_obsidian_context_menu.reg 文件
) > dist\README.md

echo.
echo ========================================
echo 构建完成！
echo ========================================
echo.
echo 输出文件位置:
echo - dist\open_folder_with_obsidian.exe
echo - dist\obsidian_installer.exe  
echo - dist\README.md
echo.
echo 下一步: 以管理员身份运行 obsidian_installer.exe 进行安装
echo.

:: 询问是否打开输出目录
set /p choice="是否打开输出目录? (y/n): "
if /i "%choice%"=="y" (
    start "" "dist"
)

pause
