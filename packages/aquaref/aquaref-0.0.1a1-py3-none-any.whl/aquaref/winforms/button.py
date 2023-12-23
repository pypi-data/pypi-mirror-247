from .control import Control


class Button(Control):

    from System.Windows.Forms import Button

    _type = Button

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
