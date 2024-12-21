# Windows Path Manager

这是一个用于在 Windows 系统中方便地管理环境变量 PATH 的工具。它提供简洁的 GUI 界面和方便的右键菜单集成，帮助用户轻松添加和移除路径，避免手动编辑带来的繁琐和潜在错误。

## 特性

*   **右键菜单集成：** 通过右键菜单快速添加/移除文件夹路径，提高操作效率。
*   **路径重复检测：** 自动检测重复添加的路径（不区分大小写），避免 PATH 变量冗余。
*   **管理员权限自动提升：** 需要管理员权限的操作会自动请求提升，无需手动以管理员身份运行。
*   **环境变量更改广播：** 修改后立即广播环境变量更改，确保其他程序及时感知。
*   **错误处理和提示：** 提供清晰的错误提示信息，帮助用户解决问题。

## 安装

1.  访问 [GitHub Releases 页面](<https://github.com/nuomi77/windows-path-manager/releases>) 下载最新版本的 zip 压缩包。
2.  将压缩包解压到任意目录。
3.  运行 `Windows Path Manager` 即可启动程序。

## 使用方法

### GUI 界面

运行 `Windows Path Manager` 后，将显示主窗口。

*   **当前程序路径：** 窗口顶部显示当前程序所在的目录，仅供参考。
*   **注册右键菜单：** 点击“注册右键菜单”按钮，将“添加到 PATH”和“从 PATH 移除”添加到文件夹的右键菜单。首次注册或更新注册可能需要管理员权限。
*   **取消注册右键菜单：** 点击“取消注册右键菜单”按钮，移除右键菜单项。此操作也可能需要管理员权限。

### 右键菜单

注册右键菜单后，在文件夹上右键单击，即可看到新增的菜单项：

*   **添加到 PATH：** 将选定文件夹的完整路径添加到用户环境变量 PATH 中。
*   **从 PATH 移除：** 从用户环境变量 PATH 中移除选定文件夹的路径。

## 贡献

欢迎提交issue和pull request。

## 许可证

本项目使用MIT许可证。