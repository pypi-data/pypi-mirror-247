from .control import Control


class Label(Control):

    from System.Windows.Forms import Label

    _type = Label

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
