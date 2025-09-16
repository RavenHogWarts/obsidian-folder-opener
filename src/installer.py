# -*- coding: utf-8 -*-
"""
Obsidian文件夹打开器安装程序
自动检测Obsidian路径，生成注册表文件，并安装右键菜单功能
"""
import os
import sys
import shutil
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox
from registry_utils import get_enhanced_obsidian_paths
from config_manager import save_obsidian_path

def find_obsidian_installation():
    """
    查找Obsidian安装路径
    """
    print("正在查找Obsidian安装路径...")
    
    # 使用增强的路径查找
    obsidian_paths = get_enhanced_obsidian_paths()
    
    for path in obsidian_paths:
        if os.path.exists(path):
            obsidian_dir = os.path.dirname(path)
            print(f"找到Obsidian安装目录: {obsidian_dir}")
            return obsidian_dir, path
    
    print("未能自动找到Obsidian安装路径")
    return None, None

def select_main_exe():
    """
    查找open_folder_with_obsidian.exe文件
    """
    print("正在查找open_folder_with_obsidian.exe文件...")
    
    exe_filename = "open_folder_with_obsidian.exe"
    current_dir = os.getcwd()
    exe_path = os.path.join(current_dir, exe_filename)
    
    # 首先在当前目录查找
    if os.path.exists(exe_path):
        print(f"找到文件: {exe_path}")
        return exe_path
    
    # 如果当前目录没有，在上级目录查找
    parent_dir = os.path.dirname(current_dir)
    exe_path = os.path.join(parent_dir, exe_filename)
    if os.path.exists(exe_path):
        print(f"找到文件: {exe_path}")
        return exe_path
    
    # 如果还是找不到，让用户手动选择
    print("未能在当前目录或上级目录找到open_folder_with_obsidian.exe文件")
    print("请手动选择该文件...")
    
    root = tk.Tk()
    root.withdraw()  # 隐藏主窗口
    
    exe_path = filedialog.askopenfilename(
        title="选择 open_folder_with_obsidian.exe 文件",
        filetypes=[("可执行文件", "*.exe"), ("所有文件", "*.*")],
        initialdir=current_dir
    )
    
    root.destroy()
    
    if not exe_path:
        print("未选择文件，安装取消")
        return None
    
    if not os.path.exists(exe_path):
        print(f"文件不存在: {exe_path}")
        return None
    
    # 验证文件名是否正确
    if not exe_path.endswith(exe_filename):
        print(f"错误: 选择的文件必须是 {exe_filename}")
        return None
    
    print(f"选择的文件: {exe_path}")
    return exe_path

def safe_messagebox_error(title, message):
    """
    安全地显示错误消息框，确保GUI资源正确清理
    """
    root = None
    try:
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror(title, message)
    except Exception as e:
        print(f"GUI错误: {e}")
        print(f"错误信息: {title} - {message}")
    finally:
        if root:
            try:
                root.destroy()
            except:
                pass

def generate_registry_file(obsidian_dir, exe_path):
    """
    生成注册表文件到当前目录
    """
    print("正在生成注册表文件...")
    
    # 确保路径使用标准的Windows路径格式（反斜杠）
    exe_path_normalized = os.path.normpath(exe_path)
    obsidian_exe_path = os.path.normpath(os.path.join(obsidian_dir, "Obsidian.exe"))
    
    # 对于注册表文件，路径中的反斜杠需要双重转义
    exe_path_escaped = exe_path_normalized.replace("\\", "\\\\")
    obsidian_exe_escaped = obsidian_exe_path.replace("\\", "\\\\")
    
    # 注册表内容
    reg_content = f'''Windows Registry Editor Version 5.00

; Add "Open with Obsidian" to folder context menu
[HKEY_CLASSES_ROOT\\Directory\\shell\\OpenWithObsidian]
@="Open with Obsidian"
"Icon"="{obsidian_exe_escaped}"

[HKEY_CLASSES_ROOT\\Directory\\shell\\OpenWithObsidian\\command]
@="{exe_path_escaped} \\"%1\\""

; Add to folder background context menu (right-click in empty space)
[HKEY_CLASSES_ROOT\\Directory\\Background\\shell\\OpenWithObsidian]
@="Open this folder in Obsidian"
"Icon"="{obsidian_exe_escaped}"

[HKEY_CLASSES_ROOT\\Directory\\Background\\shell\\OpenWithObsidian\\command]
@="{exe_path_escaped} \\"%V\\""
'''
    
    # 写入注册表文件到当前目录，使用UTF-8编码
    reg_file_path = os.path.join(os.getcwd(), "add_obsidian_context_menu.reg")
    try:
        with open(reg_file_path, 'w', encoding='utf-8') as f:
            f.write(reg_content)
        print(f"注册表文件已生成: {reg_file_path}")
        return reg_file_path
    except Exception as e:
        print(f"生成注册表文件失败: {e}")
        return None

def generate_uninstall_registry_file(current_dir):
    """
    生成卸载注册表文件到当前目录
    """
    print("正在生成卸载注册表文件...")
    
    uninstall_reg_content = '''Windows Registry Editor Version 5.00

; Remove "Open with Obsidian" from folder context menu
[-HKEY_CLASSES_ROOT\\Directory\\shell\\OpenWithObsidian]

; Remove from folder background context menu
[-HKEY_CLASSES_ROOT\\Directory\\Background\\shell\\OpenWithObsidian]
'''
    
    uninstall_reg_path = os.path.join(current_dir, "remove_obsidian_context_menu.reg")
    try:
        with open(uninstall_reg_path, 'w', encoding='utf-8') as f:
            f.write(uninstall_reg_content)
        print(f"卸载注册表文件已生成: {uninstall_reg_path}")
        return uninstall_reg_path
    except Exception as e:
        print(f"生成卸载注册表文件失败: {e}")
        return None

def copy_exe_to_obsidian_dir(exe_path, obsidian_dir):
    """
    将exe文件复制到Obsidian目录
    """
    print("正在复制exe文件到Obsidian目录...")
    
    # 标准化路径
    exe_path = os.path.normpath(exe_path)
    obsidian_dir = os.path.normpath(obsidian_dir)
    
    exe_filename = os.path.basename(exe_path)
    target_path = os.path.join(obsidian_dir, exe_filename)
    
    try:
        # 检查源文件是否存在
        if not os.path.exists(exe_path):
            print(f"源文件不存在: {exe_path}")
            return None
        
        # 检查目标目录是否存在
        if not os.path.exists(obsidian_dir):
            print(f"目标目录不存在: {obsidian_dir}")
            return None
        
        # 如果目标文件已存在，先删除
        if os.path.exists(target_path):
            print(f"目标文件已存在，将被覆盖: {target_path}")
            os.remove(target_path)
        
        shutil.copy2(exe_path, target_path)
        print(f"文件已复制到: {target_path}")
        return target_path
    except Exception as e:
        print(f"复制文件失败: {e}")
        return None

def apply_registry_file(reg_file_path):
    """
    应用注册表文件
    """
    print("正在应用注册表文件...")
    
    try:
        # 检查是否以管理员身份运行
        import ctypes
        if not ctypes.windll.shell32.IsUserAnAdmin():
            print("错误: 需要管理员权限来修改注册表")
            print("请以管理员身份运行此程序")
            return False
        
        # 应用注册表文件
        result = subprocess.run(['regedit', '/s', reg_file_path], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print("注册表文件应用成功")
            return True
        else:
            print(f"应用注册表文件失败: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"应用注册表文件时出错: {e}")
        return False

def show_completion_dialog(obsidian_dir, exe_path):
    """
    显示安装完成对话框
    """
    root = tk.Tk()
    root.title("安装完成")
    root.geometry("500x300")
    root.resizable(False, False)
    
    # 确保窗口关闭时正确退出
    def on_closing():
        root.quit()     # 退出mainloop
        root.destroy()  # 销毁窗口
        sys.exit(0)     # 退出程序
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    
    # 居中显示
    root.update_idletasks()
    x = (root.winfo_screenwidth() // 2) - (root.winfo_width() // 2)
    y = (root.winfo_screenheight() // 2) - (root.winfo_height() // 2)
    root.geometry(f"+{x}+{y}")
    
    message = f"""✓ Obsidian文件夹打开器安装成功！

安装详情：
• Obsidian目录: {obsidian_dir}
• 执行文件: {exe_path}
• 右键菜单已添加
• 注册表文件已生成到当前目录

使用方法：
1. 在任意文件夹上右键点击，选择"Open with Obsidian"
2. 或在文件夹内空白处右键，选择"Open this folder in Obsidian"

如需卸载：
运行当前目录下的 remove_obsidian_context_menu.reg 文件
"""
    
    label = tk.Label(root, text=message, justify=tk.LEFT, padx=20, pady=20)
    label.pack(expand=True, fill=tk.BOTH)
    
    button_frame = tk.Frame(root)
    button_frame.pack(pady=10)
    
    def close_app():
        root.quit()     # 退出mainloop
        root.destroy()  # 销毁窗口
        sys.exit(0)     # 退出程序
    
    ok_button = tk.Button(button_frame, text="确定", command=close_app, width=10)
    ok_button.pack()
    
    # 设置焦点到按钮，允许按回车关闭
    ok_button.focus_set()
    root.bind('<Return>', lambda e: close_app())
    
    try:
        root.mainloop()
    except Exception as e:
        print(f"GUI异常: {e}")
    finally:
        # 确保窗口被销毁
        try:
            root.quit()
            root.destroy()
        except:
            pass
        sys.exit(0)

def main():
    """
    主安装流程
    """
    print("=" * 60)
    print("Obsidian文件夹打开器安装程序")
    print("=" * 60)
    
    # 检查是否以管理员身份运行
    try:
        import ctypes
        if not ctypes.windll.shell32.IsUserAnAdmin():
            root = tk.Tk()
            root.withdraw()
            messagebox.showerror("权限不足", 
                               "此程序需要管理员权限来修改注册表。\n"
                               "请右键选择此程序，然后选择'以管理员身份运行'。")
            root.destroy()  # 确保销毁窗口
            sys.exit(1)
    except Exception as e:
        print(f"权限检查异常: {e}")
        pass
    
    # 1. 查找Obsidian安装路径
    obsidian_dir, obsidian_exe = find_obsidian_installation()
    
    if not obsidian_dir:
        root = tk.Tk()
        root.withdraw()
        
        try:
            choice = messagebox.askyesno("未找到Obsidian", 
                                       "未能自动找到Obsidian安装路径。\n"
                                       "是否手动选择Obsidian安装目录？")
            
            if choice:
                obsidian_dir = filedialog.askdirectory(title="请选择Obsidian安装目录")
                if not obsidian_dir:
                    print("未选择目录，安装取消")
                    root.destroy()  # 确保销毁窗口
                    sys.exit(1)
                
                # 标准化路径格式
                obsidian_dir = os.path.normpath(obsidian_dir)
                obsidian_exe = os.path.join(obsidian_dir, "Obsidian.exe")
                
                if not os.path.exists(obsidian_exe):
                    safe_messagebox_error("错误", 
                        f"在选择的目录中未找到Obsidian.exe文件\n"
                        f"选择的目录: {obsidian_dir}\n"
                        f"期望的文件: {obsidian_exe}")
                    root.destroy()  # 确保销毁窗口
                    sys.exit(1)
                
                print(f"手动选择的Obsidian目录: {obsidian_dir}")
                print(f"找到Obsidian.exe: {obsidian_exe}")
                
                # 保存用户选择的路径到配置文件
                print("正在保存Obsidian路径到配置文件...")
                if save_obsidian_path(obsidian_dir):
                    print("✓ Obsidian路径已保存到配置文件")
                else:
                    print("⚠ 保存配置文件失败，但安装仍将继续")
                    
            else:
                print("安装取消")
                root.destroy()  # 确保销毁窗口
                sys.exit(1)
        
        finally:
            # 确保GUI窗口被正确销毁
            try:
                root.destroy()
            except:
                pass
    else:
        # 即使是自动找到的路径，也保存到配置文件
        print("正在保存自动找到的Obsidian路径到配置文件...")
        if save_obsidian_path(obsidian_dir):
            print("✓ Obsidian路径已保存到配置文件")
    
    print(f"使用Obsidian目录: {obsidian_dir}")
    
    # 2. 查找open_folder_with_obsidian.exe文件
    main_exe_path = select_main_exe()
    if not main_exe_path:
        sys.exit(1)
    
    # 3. 复制exe文件到Obsidian目录
    target_exe_path = copy_exe_to_obsidian_dir(main_exe_path, obsidian_dir)
    if not target_exe_path:
        safe_messagebox_error("错误", "复制文件失败")
        sys.exit(1)
    
    # 4. 生成注册表文件到当前目录
    current_dir = os.getcwd()
    reg_file_path = generate_registry_file(obsidian_dir, target_exe_path)
    if not reg_file_path:
        safe_messagebox_error("错误", "生成注册表文件失败")
        sys.exit(1)
    
    # 5. 生成卸载注册表文件到当前目录
    uninstall_reg_path = generate_uninstall_registry_file(current_dir)
    
    # 6. 应用注册表文件
    if apply_registry_file(reg_file_path):
        print("安装成功！")
        show_completion_dialog(obsidian_dir, target_exe_path)
    else:
        safe_messagebox_error("错误", "应用注册表文件失败")
        sys.exit(1)

if __name__ == "__main__":
    main()
