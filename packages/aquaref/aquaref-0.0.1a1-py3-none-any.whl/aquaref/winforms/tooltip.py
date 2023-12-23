from .control import Control


class ToolTip(Control):

    from System.Windows.Forms import ToolTip

    _type = ToolTip

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def SetToolTip(self, Widget: Control, Text: str = ""):
        self._.SetToolTip(Widget._, Text)