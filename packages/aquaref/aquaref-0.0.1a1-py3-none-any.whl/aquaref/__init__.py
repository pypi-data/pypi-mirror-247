from .library import LoadMetro, LoadReaLTaiizor
from aquareflog import Debug, Error, Info, Success, SaveLog, GetLog

# ---

from clr import AddReference

Debug("准备导入...")


def Load(Name):
    Debug(f'加载 "{Name}" 中...')

    from System.IO import FileNotFoundException

    try:
        AddReference(Name)
    except FileNotFoundException:
        Error(f'"加载 "{Name}" 失败！"')
    else:
        Success(f'加载 "{Name}" 成功！')


Load("System.IO")
Load("System.Drawing")
Load("System.Windows")
Load("System.Windows.Forms")
#Load("System.Windows.Forms.Integration")
Load("System.Runtime.InteropServices")

# ---

from .winforms import *
