
def get_platform(self):
    import platform
    system_name = platform.system().lower()
    if 'linux' in system_name:
        return 'linux64'
    elif 'darwin' in system_name:
        return 'mac-arm64' if platform.processor() == 'arm' else 'mac-x64'
    elif 'win' in system_name:
        return 'win64' if platform.architecture()[0] == '64bit' else 'win32'
    else:
        raise ValueError(f"Unsupported platform: {system_name}")
