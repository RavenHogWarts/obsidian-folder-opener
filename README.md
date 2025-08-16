# open-folder-with-obsidian

一个Windows右键菜单工具，让您可以直接用Obsidian打开任意文件夹作为vault。

## 安装使用

### 方法一：下载预编译版本（推荐）

1. 访问 [Releases页面](https://github.com/RavenHogwarts/open-folder-with-obsidian/releases)
2. 下载最新版本的 `obsidian-folder-opener.zip`, 并解压
3. 以管理员身份运行安装程序 `obsidian_installer.exe`
4. 按照提示完成安装

### 方法二：从源码构建

#### 前置要求

- Python 3.8+
- Windows操作系统
- 已安装Obsidian

#### 安装步骤

1. 克隆仓库：
```bash
git clone https://github.com/RavenHogwarts/open-folder-with-obsidian.git
cd open-folder-with-obsidian
```

2. 安装依赖：
```bash
pip install -r requirements.txt
```

3. 构建可执行文件：
```bash
build.bat
```

4. 运行安装程序：
```bash
# 以管理员身份运行
dist/obsidian_installer.exe
```

## 使用方法

安装完成后，您可以通过以下方式使用：

### 1. 文件夹右键菜单
- 在任意文件夹上**右键点击**
- 选择"**Open with Obsidian**"

### 2. 文件夹内右键菜单
- 在文件夹内的**空白处右键点击**
- 选择"**Open this folder in Obsidian**"

## 工作原理

1. **配置管理**：程序会自动修改Obsidian的配置文件 (`obsidian.json`)
2. **Vault添加**：将选择的文件夹添加为新的vault
3. **自动启动**：配置完成后自动启动Obsidian
4. **智能切换**：新添加的vault会被设置为当前活动vault

## 卸载

如需卸载右键菜单功能：

1. 双击运行 `remove_obsidian_context_menu.reg` 文件
2. 找到Obsidian安装目录，删除目录下的 `open_folder_with_obsidian.exe`