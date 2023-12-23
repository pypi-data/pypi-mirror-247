from flater.basic import Basic


class Window(Basic):

    from System.Windows import Window

    _type = Window

    def __init__(self):
        super().__init__()