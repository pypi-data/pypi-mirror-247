from ..basic import Basic


class Form(Basic):

    from System.Windows.Forms import Form

    _type = Form

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._app = None

        import os
        self.Icon = os.path.join(os.path.abspath(os.path.dirname(__file__)), "py.ico")

    def AppClose(self):
        if self._app:
            self._app.Close()

    def AppRestart(self):
        """
        不支持，请勿使用
        """
        if self._app:
            self._app.Restart()

    def AppRun(self):
        from .application import Application
        self._app = Application()
        self._app.Run(self)
        from aquareflog import Debug
        Debug("主程序已结束")

    def Close(self):
        self._.Close()

    @property
    def MdiParent(self):
        _Form = Form(Init=False)
        _Form.Myself = self._.MdiParent
        return _Form

    @MdiParent.setter
    def MdiParent(self, Form: Basic):
        self._.MdiParent = Form._