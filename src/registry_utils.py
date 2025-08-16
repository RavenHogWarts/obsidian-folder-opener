# -*- coding: utf-8 -*-
"""
注册表工具模块
用于查询Windows注册表信息
"""
import winreg
import os

def get_program_files_paths():
    """
    从注册表获取Program Files相关路径
    返回包含各种Program Files路径的字典
    """
    paths = {}
    
    try:
        # 打开注册表键
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, 
                            r"SOFTWARE\Microsoft\Windows\CurrentVersion")
        
        # 查询Program Files目录
        try:
            program_files_dir, _ = winreg.QueryValueEx(key, "ProgramFilesDir")
            paths["ProgramFilesDir"] = program_files_dir
            print(f"Program Files目录: {program_files_dir}")
        except FileNotFoundError:
            paths["ProgramFilesDir"] = None
            print("未找到ProgramFilesDir")
        
        # 查询Program Files (x86)目录
        try:
            program_files_x86, _ = winreg.QueryValueEx(key, "ProgramFilesDir (x86)")
            paths["ProgramFilesDirX86"] = program_files_x86
            print(f"Program Files (x86)目录: {program_files_x86}")
        except FileNotFoundError:
            paths["ProgramFilesDirX86"] = None
            print("未找到ProgramFilesDir (x86)")
        
        # 查询Program W6432目录
        try:
            program_w6432, _ = winreg.QueryValueEx(key, "ProgramW6432Dir")
            paths["ProgramW6432Dir"] = program_w6432
            print(f"Program W6432目录: {program_w6432}")
        except FileNotFoundError:
            paths["ProgramW6432Dir"] = None
            print("未找到ProgramW6432Dir")
        
        # 关闭键
        winreg.CloseKey(key)
        
    except Exception as e:
        print(f"读取注册表时出错: {e}")
        # 使用默认路径作为后备
        paths = {
            "ProgramFilesDir": r"C:\Program Files",
            "ProgramFilesDirX86": r"C:\Program Files (x86)",
            "ProgramW6432Dir": r"C:\Program Files"
        }
    
    return paths

def find_obsidian_in_registry():
    """
    从注册表中查找Obsidian的安装路径
    """
    possible_keys = [
        (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"),
        (winreg.HKEY_CURRENT_USER, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"),
        (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"),
    ]
    
    for hkey, subkey in possible_keys:
        try:
            with winreg.OpenKey(hkey, subkey) as key:
                i = 0
                while True:
                    try:
                        subkey_name = winreg.EnumKey(key, i)
                        with winreg.OpenKey(key, subkey_name) as app_key:
                            try:
                                display_name, _ = winreg.QueryValueEx(app_key, "DisplayName")
                                if "Obsidian" in display_name:
                                    try:
                                        install_location, _ = winreg.QueryValueEx(app_key, "InstallLocation")
                                        exe_path = os.path.join(install_location, "Obsidian.exe")
                                        if os.path.exists(exe_path):
                                            print(f"从注册表找到Obsidian: {exe_path}")
                                            return exe_path
                                    except FileNotFoundError:
                                        # 尝试从DisplayIcon获取路径
                                        try:
                                            icon_path, _ = winreg.QueryValueEx(app_key, "DisplayIcon")
                                            if icon_path.endswith("Obsidian.exe"):
                                                if os.path.exists(icon_path):
                                                    print(f"从注册表图标路径找到Obsidian: {icon_path}")
                                                    return icon_path
                                        except FileNotFoundError:
                                            pass
                            except FileNotFoundError:
                                pass
                        i += 1
                    except OSError:
                        break
        except Exception as e:
            continue
    
    print("未在注册表中找到Obsidian")
    return None

def get_enhanced_obsidian_paths():
    """
    获取增强的Obsidian路径列表，结合注册表查询和常规路径
    """
    paths = []
    
    # 首先尝试从注册表获取
    registry_path = find_obsidian_in_registry()
    if registry_path:
        paths.append(registry_path)
    
    # 获取Program Files路径
    program_paths = get_program_files_paths()
    
    # 添加常规路径
    common_paths = [
        fr'C:\Users\{os.getlogin()}\AppData\Local\Obsidian\Obsidian.exe',
    ]
    
    # 添加Program Files相关路径
    for key, program_dir in program_paths.items():
        if program_dir:
            obsidian_path = os.path.join(program_dir, "Obsidian", "Obsidian.exe")
            common_paths.append(obsidian_path)
    
    # 合并路径并去重
    paths.extend(common_paths)
    unique_paths = []
    for path in paths:
        if path not in unique_paths:
            unique_paths.append(path)
    
    return unique_paths

if __name__ == "__main__":
    print("=" * 50)
    print("注册表查询测试")
    print("=" * 50)
    
    # 测试获取Program Files路径
    print("\n1. 获取Program Files路径:")
    paths = get_program_files_paths()
    
    # 测试查找Obsidian
    print("\n2. 查找Obsidian安装路径:")
    obsidian_paths = get_enhanced_obsidian_paths()
    
    print(f"\n找到 {len(obsidian_paths)} 个可能的Obsidian路径:")
    for i, path in enumerate(obsidian_paths, 1):
        exists = "✓" if os.path.exists(path) else "✗"
        print(f"{i}. {exists} {path}")
