from game_core import constants


class Option:

    def __init__(self, text, pos, func, font):
        """
        Initialize option
        :param text: text function to display
        :param pos: initial position of the text
        :param func: function which will be called on mouse onclick event
        :param font: set text font
        """
        self.text = text
        self.pos = pos
        self.func = func
        self.rect = 0
        self.rend = 0
        self.hovered = False
        self.font = font
        self.set_rect()

    def select(self):
        """
        Call function when option is hovered and clicked
        """
        self.func()

    def set_rend(self):
        """
        Set text render options
        """
        text = self.text()
        self.rend = self.font.render(text, True, self.get_color())

    def get_color(self):
        """
        Get hovered and default color of text
        """
        if self.hovered:
            return 251, 223, 124
        else:
            return 0, 0, 0

    def set_rect(self):
        """
        Get hovered and default color of text
        """
        self.set_rend()
        self.rect = self.rend.get_rect()
        self.rect.center = (int((constants.display_width / 2)), int(constants.display_height / 2))
        self.rect.top = self.pos


class GroupedOptions:
    """
    Initialize option group
    """
    def __init__(self):
        self.options = []

    def add(self, option):
        """
        Add option to this options group
        """
        self.options.append(option)
