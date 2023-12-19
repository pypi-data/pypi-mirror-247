import winreg

hkey_cur_user = winreg.HKEY_CURRENT_USER

def winreg_cur_user_QueryValueEx(key, sub):
    try:
        with winreg.OpenKey(hkey_cur_user, key) as reg_key:
            value, _ = winreg.QueryValueEx(reg_key, sub)
            print("Value:", value)
            return value
    except FileNotFoundError:
        print("Registry key not found.")
    except Exception as e:
        print("Error:", e)
    return None

def winreg_cur_user_SetValueEx(key, sub, value):
    try:
        with winreg.OpenKey(hkey_cur_user, key, 0, winreg.KEY_WRITE) as reg_key:
            winreg.SetValueEx(reg_key, sub, 0, winreg.REG_SZ, value)
            print("Value set successfully.")
            return True
    except FileNotFoundError:
        print("Registry key not found.")
    except Exception as e:
        print("Error:", e)
    return False
