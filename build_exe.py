# build_exe.py
import PyInstaller.__main__
import os
import tkinter.ttk

# 获取 tkinter 库文件的实际位置
tcl_folder = os.path.dirname(tkinter.__file__)
tk_dll = os.path.join(tcl_folder, 'tk86t.dll')
tcl_dll = os.path.join(tcl_folder, 'tcl86t.dll')
tk_lib = os.path.join(tcl_folder, 'tk8.6')
tcl_lib = os.path.join(tcl_folder, 'tcl8.6')

# 确保在脚本所在目录运行
os.chdir(os.path.dirname(os.path.abspath(__file__)))

options = [
    'main.py',    # 主程序文件名
    # '--noconsole',        # 不显示控制台窗口
    '--name=Windows Path Manager',  # exe的名称
    '--uac-admin',        # 请求管理员权限
    '--clean',            # 清理临时文件
]

# 添加 tk/tcl 依赖
if os.path.exists(tk_lib):
    options.extend(['--add-data', f'{tk_lib};tk8.6'])
if os.path.exists(tcl_lib):
    options.extend(['--add-data', f'{tcl_lib};tcl8.6'])
if os.path.exists(tk_dll):
    options.extend(['--add-binary', f'{tk_dll};.'])
if os.path.exists(tcl_dll):
    options.extend(['--add-binary', f'{tcl_dll};.'])

# 运行打包命令
PyInstaller.__main__.run(options)