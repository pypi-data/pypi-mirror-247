def LoadMetro():
    try:
        import MetroFramework
    except ModuleNotFoundError:
        from aquareflog import Debug, Success, Error
        Debug('加载 "MetroFramework" 中...')
        try:
            from .metro import libs
        except ModuleNotFoundError:
            Error('加载 "MetroFramework" 失败，未找到该库，请安装Aquaref-MetroFramework重试！')
        else:
            for lib in libs:
                from clr import AddReference
                AddReference(libs[lib])
                Debug(f'加载 "{libs[lib]}"')
            Success('加载 "MetroFramework" 成功！')


def LoadReaLTaiizor():
    try:
        import ReaLTaiizor
    except ModuleNotFoundError:
        from aquareflog import Debug, Success, Error
        Debug('加载 "ReaLTaiizor" 中...')
        try:
            from .realtaiizor import libs
        except ModuleNotFoundError:
            Error('加载 "ReaLTaiizor" 失败，未找到该库，请安装Aquaref-ReaLTaiizor重试！')
        else:
            for lib in libs:
                from clr import AddReference

                AddReference(libs[lib])
                Debug(f'加载 "{libs[lib]}"')
            Success('加载 "ReaLTaiizor" 成功！')