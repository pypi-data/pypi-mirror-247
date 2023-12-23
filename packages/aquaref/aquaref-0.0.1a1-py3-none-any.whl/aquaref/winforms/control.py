from ..basic import Basic


class Control(Basic):
    """
    基础组件，不可见
    """
    def __init__(self, Parent: Basic = None, *args, **kwargs):
        """
        初始化组件

        Args:
            Parent (Control): 父组件，如果设置此类将自动调用 Parent.Add 添加该组件
        """
        super().__init__(*args, **kwargs)

        if Parent:
            Parent.Add(self)

    def Add(self, Widget, _WinForms_Widget=None):
        """
        在容器组件中添加组件

        Args:
            Widget (aquaref.Window): 组件类
            _WinForms_Widget (System.Windows.Forms.Control): 组件类（应为WinForms的组件）
        """
        if _WinForms_Widget:
            self._.Controls.Add(_WinForms_Widget)
        else:
            self._.Controls.Add(Widget._)

    @property
    def Anchor(self):
        return self._.Anchor

    @Anchor.setter
    def Anchor(self, Style: str):
        self._.Anchor = Style

    @property
    def AutoScroll(self):
        return self._.AutoScroll

    @AutoScroll.setter
    def AutoScroll(self, Enable: str):
        self._.AutoScroll = Enable

    def Create(self, Type) -> Basic:
        _ = Type(self)
        return _

    @property
    def Dock(self):
        return self._.Dock

    @Dock.setter
    def Dock(self, Style):
        from System.Windows.Forms import DockStyle

        self._.Dock = (getattr(DockStyle, Style))

    @property
    def Enable(self):
        return self._.Enable

    @Enable.setter
    def Enable(self, Enable: bool):
        self._.Enable = Enable

    @property
    def Handle(self):
        return self._.Handle

    def Hide(self):
        self._.Hide()

    @property
    def Icon(self):
        return self._.Icon.ToString()

    @Icon.setter
    def Icon(self, FileName: str):
        from System.Drawing import Icon

        self._.Icon = Icon(fileName=FileName)

    @property
    def Margin(self):
        return self._.Margin

    @Margin.setter
    def Margin(self, *args):
        from System.Windows.Forms import Padding

        self._.Margin = Padding(*args)

    def Margin2(self, *args):
        from System.Windows.Forms import Padding

        self._.Margin = Padding(*args)

    def Pack(self, Dock=None, Margin=None, Padding=None, Anchor=None):
        if Dock:
            self.Dock = Dock
        if Margin:
            if type(Margin).__name__ == "int":
                self.Margin = Margin
            elif type(Margin).__name__ == "tuple" or type(Margin).__name__ == "list":
                self.Margin2(*Margin),
        if Padding:
            if type(Padding).__name__ == "int":
                self.Margin = Padding
            elif type(Padding).__name__ == "tuple" or type(Padding).__name__ == "list":
                self.Margin2(*Padding)
        if Anchor:
            self.Anchor = Anchor

    @property
    def Padding(self):
        return self._.Padding

    @Padding.setter
    def Padding(self, *args):
        from System.Windows.Forms import Padding

        self._.Padding = Padding(*args)

    def Padding2(self, *args):
        from System.Windows.Forms import Padding

        self._.Padding = Padding(*args)

    def Place(self, X=None, Y=None, Width=None, Height=None):
        if X is None:
            X = self.Pos[0]
        if Y is None:
            Y = self.Pos[1]
        self.Pos = [X, Y]

        if Width is None:
            Width = self.Size[0]
        if Height is None:
            Height = self.Size[1]
        self.Size = [Width, Height]

    @property
    def Pos(self):
        return self._.Location.X, self._.Location.Y

    @Pos.setter
    def Pos(self, Tuple: tuple):
        from System.Drawing import Point
        self._.Location = Point(Tuple[0], Tuple[1])

    def Show(self):
        """
        显示窗口
        """
        self._.Show()

    @property
    def Size(self):
        return self._.Size.Width, self._.Size.Height

    @Size.setter
    def Size(self, Tuple: tuple):
        from System.Drawing import Size
        self._.Size = Size(Tuple[0], Tuple[1])

    @property
    def Text(self):
        return self._.Text

    @Text.setter
    def Text(self, String: str):
        self._.Text = String

    @property
    def ToolTip(self):
        return self._.ToolTip

    @ToolTip.setter
    def ToolTip(self, String: str):
        self._.ToolTip = String


