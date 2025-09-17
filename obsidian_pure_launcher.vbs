' =============================================================================
' Obsidian 启动器 - 环境变量版本
' 用户配置：修改下面的 OBSIDIAN_PATH 变量来自定义 Obsidian 路径
' =============================================================================

' ========== 用户配置区域 ==========
' 设置您的 Obsidian 可执行文件完整路径
' 常用路径示例：
'   "%LOCALAPPDATA%\Obsidian\Obsidian.exe"           (默认安装位置)
'   "C:\Program Files\Obsidian\Obsidian.exe"         (系统级安装)
'   "D:\PortableApps\Obsidian\Obsidian.exe"          (便携版)
'   "E:\Software\Obsidian\Obsidian.exe"              (自定义位置)

OBSIDIAN_PATH = "D:\Program Files\Obsidian\Obsidian.exe"

' ==================================

' 初始化脚本对象
On Error Resume Next
Set ws = CreateObject("WScript.Shell")
Set fso = CreateObject("Scripting.FileSystemObject")

' 1. 修改 Obsidian 配置文件（保持原有逻辑）
obsidianJsonPath = ws.ExpandEnvironmentStrings("%APPDATA%\obsidian\obsidian.json")
If fso.FileExists(obsidianJsonPath) Then
    Set file = fso.OpenTextFile(obsidianJsonPath, 1, False)
    content = file.ReadAll
    file.Close
    newContent = Replace(content, ",""open"":true", "")
    Set file = fso.OpenTextFile(obsidianJsonPath, 2, False)
    file.Write newContent
    file.Close
End If

' 2. 使用环境变量路径启动 Obsidian
' 展开环境变量
obsidianExePath = ws.ExpandEnvironmentStrings(OBSIDIAN_PATH)

' 检查路径是否存在
If fso.FileExists(obsidianExePath) Then
    ' 路径存在，直接启动
    ws.Run Chr(34) & obsidianExePath & Chr(34), 1, False
Else
    MsgBox "Path not found: " & obsidianExePath, vbCritical, "Obsidian Launcher"
End If

On Error GoTo 0