from ..basic import Basic


class Application(Basic):
    """
    主程序，用于实现窗口的消息循环

    """

    from System.Windows.Forms import Application

    _type = Application

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def Close(self, Window, _WinForms_Window=None):
        """
        关闭窗口

        Args:
            Window (aquaref.Window): 窗口类
            _WinForms_Window (System.Windows.Forms.Application): 窗口类（应为WinForms的窗口）
        """
        if _WinForms_Window:
            self._.Close(_WinForms_Window)
        else:
            self._.Close(Window._)

    def Restart(self):
        """
        重启窗口
        """
        self._.Restart()

    def Run(self, Window, _WinForms_Window=None):
        """
        运行窗口

        Args:
            Window (aquaref.Window): 窗口类
            _WinForms_Window (System.Windows.Forms.Application): 窗口类（应为WinForms的窗口）
        """
        from aquareflog import Debug, Info
        from System.Runtime.InteropServices import RuntimeInformation

        Info(f'运行框架为 "{RuntimeInformation.FrameworkDescription}"')
        Debug("正在运行主程序...")
        if _WinForms_Window:
            self._.Run(_WinForms_Window)
        else:
            self._.Run(Window._)


if __name__ == '__main__':
    app = Application()