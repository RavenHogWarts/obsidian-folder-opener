# -*- coding: utf-8 -*-
"""
用Obsidian打开文件夹的工具
通过修改obsidian.json配置文件来添加新的vault
"""
import os
import json
import hashlib
import time
import sys
import subprocess
from registry_utils import get_enhanced_obsidian_paths

def generate_vault_id(folder_path):
    """
    为文件夹路径生成唯一的vault ID
    使用路径的MD5哈希值的前16位
    """
    path_hash = hashlib.md5(folder_path.encode('utf-8')).hexdigest()
    return path_hash[:16]

def get_obsidian_config_path():
    """
    获取obsidian.json配置文件路径
    """
    return os.path.join(os.getenv("APPDATA"), 'obsidian', 'obsidian.json')

def clean_existing_open_flags(config):
    """
    移除现有vault中的open标志，为新vault让路
    """
    if 'vaults' in config:
        for vault_id, vault_info in config['vaults'].items():
            if 'open' in vault_info:
                del vault_info['open']
    return config

def read_obsidian_config():
    """
    读取obsidian.json配置文件
    """
    config_path = get_obsidian_config_path()
    
    if not os.path.exists(config_path):
        print(f"[错误] 未找到obsidian.json配置文件: {config_path}")
        return None
    
    try:
        with open(config_path, 'r', encoding='utf-8') as file:
            content = file.read()
            
        # 解析JSON
        config = json.loads(content)
        return config
        
    except json.JSONDecodeError as e:
        print(f"[错误] 解析obsidian.json失败: {e}")
        return None
    except Exception as e:
        print(f"[错误] 读取配置文件失败: {e}")
        return None

def write_obsidian_config(config):
    """
    写入obsidian.json配置文件
    """
    config_path = get_obsidian_config_path()
    
    try:
        # 确保目录存在
        config_dir = os.path.dirname(config_path)
        if not os.path.exists(config_dir):
            os.makedirs(config_dir)
        
        # 写入配置文件
        with open(config_path, 'w', encoding='utf-8') as file:
            json.dump(config, file, ensure_ascii=False, separators=(',', ':'))
        
        print(f"[成功] 配置文件已更新: {config_path}")
        return True
        
    except Exception as e:
        print(f"[错误] 写入配置文件失败: {e}")
        return False

def add_vault_to_config(config, folder_path):
    """
    在配置中添加新的vault
    """
    # 确保folder_path是绝对路径
    folder_path = os.path.abspath(folder_path)
    
    # 检查文件夹是否存在
    if not os.path.exists(folder_path):
        print(f"[错误] 文件夹不存在: {folder_path}")
        return False
    
    # 生成vault ID
    vault_id = generate_vault_id(folder_path)
    
    # 确保vaults字段存在
    if 'vaults' not in config:
        config['vaults'] = {}
    
    # 检查是否已经存在相同路径的vault
    for existing_id, vault_info in config['vaults'].items():
        if vault_info.get('path') == folder_path:
            print(f"[信息] 文件夹已存在于配置中: {folder_path}")
            print(f"[信息] 现有vault ID: {existing_id}")
            return existing_id
    
    # 添加新的vault
    current_timestamp = int(time.time() * 1000)  # 毫秒时间戳
    config['vaults'][vault_id] = {
        'path': folder_path,
        'ts': current_timestamp,
        'open': True
    }
    
    print(f"[成功] 已添加新vault:")
    print(f"  ID: {vault_id}")
    print(f"  路径: {folder_path}")
    print(f"  时间戳: {current_timestamp}")
    
    return vault_id

def launch_obsidian():
    """
    启动Obsidian应用程序
    """
    print("\n正在启动Obsidian...")
    print("=" * 40)
    
    # 使用增强的路径查找
    OBSIDIAN_PATHS = get_enhanced_obsidian_paths()
    
    path_found = False
    for i, path in enumerate(OBSIDIAN_PATHS, 1):
        print(f"正在检查路径 {i}: {path}")
        if os.path.exists(path):
            print(f"[成功找到] {path}")
            print("即将启动Obsidian...")
            subprocess.Popen([path], shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print("启动命令已执行")
            path_found = True
            break
        else:
            print(f"[未找到] {path}")
    
    if not path_found:
        print("所有路径都未找到Obsidian")
        print("请检查Obsidian是否已正确安装")
        return False
    else:
        print("\n" + "=" * 40)
        print("成功启动Obsidian！")
        print("=" * 40)
        return True

def open_folder_with_obsidian(folder_path):
    """
    用Obsidian打开指定文件夹
    """
    print(f"准备用Obsidian打开文件夹: {folder_path}")
    print("=" * 60)
    
    # 读取当前配置
    print("\n1. 读取Obsidian配置...")
    config = read_obsidian_config()
    if config is None:
        return False
    
    # 清理现有的open标志
    print("\n2. 清理现有vault的open标志...")
    config = clean_existing_open_flags(config)
    
    # 添加vault到配置
    print("\n3. 添加文件夹到Obsidian vault列表...")
    vault_id = add_vault_to_config(config, folder_path)
    if not vault_id:
        return False
    
    # 写入配置
    print("\n4. 保存配置...")
    if not write_obsidian_config(config):
        return False
    
    # 启动Obsidian
    print("\n5. 启动Obsidian...")
    if not launch_obsidian():
        return False
    
    print(f"\n✓ 成功完成！文件夹 '{folder_path}' 已添加到Obsidian")
    print("请在Obsidian中选择对应的vault来打开该文件夹")
    
    return True

def main():
    """
    主函数 - 处理命令行参数
    """
    if len(sys.argv) != 2:
        print("用法: open_folder_with_obsidian.exe <文件夹路径>")
        print("示例: open_folder_with_obsidian.exe \"C:\\Users\\Username\\Documents\\MyNotes\"")
        print(f"实际收到的参数数量: {len(sys.argv)}")
        print(f"参数列表: {sys.argv}")
        input("按回车键退出...")
        sys.exit(1)
    
    folder_path = sys.argv[1]
    print(f"原始参数: {repr(folder_path)}")
    
    # 去除路径两端的引号
    if folder_path.startswith('"') and folder_path.endswith('"'):
        folder_path = folder_path[1:-1]
        print(f"去除引号后: {repr(folder_path)}")
    
    # 验证路径是否存在
    if not os.path.exists(folder_path):
        print(f"[错误] 指定的文件夹不存在: {folder_path}")
        input("按回车键退出...")
        sys.exit(1)
    
    # 验证是否为文件夹
    if not os.path.isdir(folder_path):
        print(f"[错误] 指定的路径不是文件夹: {folder_path}")
        input("按回车键退出...")
        sys.exit(1)
    
    success = open_folder_with_obsidian(folder_path)
    
    if success:
        print("\n操作完成，程序将在3秒后退出...")
        time.sleep(3)
        sys.exit(0)
    else:
        print("\n操作失败！")
        input("按回车键退出...")
        sys.exit(1)

if __name__ == "__main__":
    main()
