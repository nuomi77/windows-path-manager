import sys
import os
import ctypes
import winreg as reg
from tkinter import messagebox
import tkinter as tk

def is_admin():
    """检查是否具有管理员权限"""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_as_admin():
    """以管理员权限重新运行程序"""
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)

def add_to_path(new_path):
    """添加路径到用户环境变量PATH中"""
    try:
        key = reg.OpenKey(reg.HKEY_CURRENT_USER, "Environment", 0, reg.KEY_ALL_ACCESS)
        try:
            path_value, _ = reg.QueryValueEx(key, "Path")
        except FileNotFoundError:  # 更精确的异常处理
            path_value = ""

        paths = path_value.split(";")
        if new_path in paths:
            messagebox.showinfo("提示", "此路径已在PATH中！")
            return

        new_path_value = path_value + ";" + new_path if path_value else new_path
        reg.SetValueEx(key, "Path", 0, reg.REG_EXPAND_SZ, new_path_value)

        broadcast_environment_change() # 调用广播函数

        messagebox.showinfo("成功", "成功添加到PATH环境变量！")
    except Exception as e:
        messagebox.showerror("错误", f"添加到PATH失败：{str(e)}")
    finally:
        reg.CloseKey(key)

def remove_from_path(path_to_remove):
    """从用户环境变量PATH中移除路径"""
    try:
        key = reg.OpenKey(reg.HKEY_CURRENT_USER, "Environment", 0, reg.KEY_ALL_ACCESS)
        try:
            path_value, _ = reg.QueryValueEx(key, "Path")
        except FileNotFoundError:
            messagebox.showinfo("提示", "PATH 环境变量不存在！")
            return

        paths = path_value.split(";")
        if path_to_remove not in paths:
            messagebox.showinfo("提示", "此路径不在PATH中！")
            return

        paths = [p for p in paths if p != path_to_remove]  # 使用列表推导式高效移除
        new_path_value = ";".join(paths)

        reg.SetValueEx(key, "Path", 0, reg.REG_EXPAND_SZ, new_path_value)

        broadcast_environment_change() # 调用广播函数

        messagebox.showinfo("成功", "成功从PATH环境变量移除！")
    except Exception as e:
        messagebox.showerror("错误", f"从PATH移除失败：{str(e)}")
    finally:
        reg.CloseKey(key)

def broadcast_environment_change():
    """广播环境变量更改消息"""
    HWND_BROADCAST = 0xFFFF
    WM_SETTINGCHANGE = 0x1A
    SMTO_ABORTIFHUNG = 0x0002
    result = ctypes.c_long()
    ctypes.windll.user32.SendMessageTimeoutW(HWND_BROADCAST, WM_SETTINGCHANGE, 0,
                                             "Environment", SMTO_ABORTIFHUNG, 5000, ctypes.byref(result))

def register_context_menu():
    """注册右键菜单"""
    try:
        # 添加到PATH
        menu_key_add = r"Directory\\Background\\shell\\PathAdd"
        key_add = reg.CreateKey(reg.HKEY_CLASSES_ROOT, menu_key_add)
        reg.SetValue(key_add, "", reg.REG_SZ, "添加到PATH")
        command_key_add = reg.CreateKey(key_add, "command")
        command_add = f'"{sys.executable}" "{os.path.abspath(__file__)}" "add" "%V"'
        reg.SetValue(command_key_add, "", reg.REG_SZ, command_add)
        reg.CloseKey(command_key_add)
        reg.CloseKey(key_add)

        # 从PATH移除
        menu_key_remove = r"Directory\\Background\\shell\\PathRemove"
        key_remove = reg.CreateKey(reg.HKEY_CLASSES_ROOT, menu_key_remove)
        reg.SetValue(key_remove, "", reg.REG_SZ, "从PATH移除")
        command_key_remove = reg.CreateKey(key_remove, "command")
        command_remove = f'"{sys.executable}" "{os.path.abspath(__file__)}" "remove" "%V"'
        reg.SetValue(command_key_remove, "", reg.REG_SZ, command_remove)
        reg.CloseKey(command_key_remove)
        reg.CloseKey(key_remove)

        messagebox.showinfo("成功", "右键菜单注册成功！")
    except Exception as e:
        messagebox.showerror("错误", f"注册右键菜单失败：{str(e)}")

def unregister_context_menu():
    if not is_admin():
        run_as_admin()
    try:
        parent_menu_key = r"Directory\\Background\\shell\\PathManager"
        try:
           reg.DeleteKey(reg.HKEY_CLASSES_ROOT, parent_menu_key)
        except FileNotFoundError:
            pass
        messagebox.showinfo("成功", "右键菜单已取消注册！")
    except Exception as e:
        messagebox.showerror("错误", f"取消注册右键菜单失败：{str(e)}")
def main():
    root = tk.Tk()
    root.withdraw()
    print(sys.argv)

    if len(sys.argv) > 1:
        action = sys.argv[2] # 获取操作类型 "add" 或 "remove"
        path = sys.argv[3] if len(sys.argv)>3 else None # 获取路径，注意判断是否存在
        if action == "add":
            add_to_path(path)
        elif action == "remove":
            remove_from_path(path)
        else:
            messagebox.showerror("错误", "无效的操作参数！")
    else:
        if not is_admin():
            run_as_admin()
        else:
            # 创建GUI界面
            window = tk.Tk()
            window.title("Windows Path Manager")

            current_path_label = tk.Label(window, text="当前程序路径:")
            current_path_label.pack()
            current_path_text = tk.Text(window, height=1, width=50)
            current_path_text.insert(tk.END, os.path.dirname(os.path.abspath(__file__)))
            current_path_text.config(state=tk.DISABLED)
            current_path_text.pack()

            add_button = tk.Button(window, text="注册右键菜单", command=register_context_menu)
            add_button.pack()

            unregister_button = tk.Button(window, text="取消注册右键菜单", command=unregister_context_menu)
            unregister_button.pack()

            window.mainloop()


if __name__ == "__main__":
    main()