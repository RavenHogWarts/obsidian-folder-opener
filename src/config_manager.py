# -*- coding: utf-8 -*-
"""
配置管理模块
用于保存和读取用户配置，包括Obsidian安装路径
"""
import os
import json
import logging

def get_config_file_path():
    """获取配置文件路径"""
    # 使用AppData目录存储配置
    appdata_dir = os.getenv("APPDATA")
    config_dir = os.path.join(appdata_dir, 'ObsidianFolderOpener')
    
    # 确保目录存在
    if not os.path.exists(config_dir):
        os.makedirs(config_dir)
    
    return os.path.join(config_dir, 'config.json')

def load_config():
    """加载配置文件"""
    config_file = get_config_file_path()
    
    if not os.path.exists(config_file):
        # 返回默认配置
        return {
            'obsidian_path': None,
            'last_updated': None
        }
    
    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            config = json.load(f)
        print(f"[配置] 已加载配置文件: {config_file}")
        return config
    except Exception as e:
        print(f"[警告] 加载配置文件失败: {e}")
        return {
            'obsidian_path': None,
            'last_updated': None
        }

def save_config(config):
    """保存配置文件"""
    config_file = get_config_file_path()
    
    try:
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=2)
        print(f"[配置] 配置已保存到: {config_file}")
        return True
    except Exception as e:
        print(f"[错误] 保存配置文件失败: {e}")
        return False

def save_obsidian_path(obsidian_path):
    """保存Obsidian路径到配置"""
    import time
    
    config = load_config()
    config['obsidian_path'] = obsidian_path
    config['last_updated'] = int(time.time())
    
    return save_config(config)

def get_obsidian_path():
    """从配置获取Obsidian路径"""
    config = load_config()
    obsidian_path = config.get('obsidian_path')
    
    if obsidian_path and os.path.exists(obsidian_path):
        print(f"[配置] 使用已保存的Obsidian路径: {obsidian_path}")
        return obsidian_path
    elif obsidian_path:
        print(f"[警告] 已保存的Obsidian路径不存在: {obsidian_path}")
    
    return None

def get_saved_obsidian_exe_path():
    """获取保存的Obsidian.exe完整路径"""
    obsidian_dir = get_obsidian_path()
    if obsidian_dir:
        obsidian_exe = os.path.join(obsidian_dir, "Obsidian.exe")
        if os.path.exists(obsidian_exe):
            return obsidian_exe
        else:
            print(f"[警告] Obsidian.exe不存在于保存的路径: {obsidian_exe}")
    
    return None

if __name__ == "__main__":
    print("配置管理模块测试")
    print("=" * 40)
    
    # 测试加载配置
    config = load_config()
    print(f"当前配置: {config}")
    
    # 测试获取Obsidian路径
    path = get_obsidian_path()
    print(f"Obsidian路径: {path}")
    
    exe_path = get_saved_obsidian_exe_path()
    print(f"Obsidian.exe路径: {exe_path}")