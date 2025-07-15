from textual.widget import Widget

from rich.panel import Panel
from rich.text import Text
from rich import box


class SelectWidget(Widget):
    """
    SelectWidget is a widget that takes in a list and outputs a Widget
    that the user can select the options specified in the options provided
    """

    def __init__(self, options: list) -> None:
        super().__init__()
        self.options = options
        self.select_index = 0

    def render(self) -> Panel:
        return Panel(self.__convert_list_to_text(self.options),
                     title="Tunnel Select",
                     border_style=self.app.get_css_variables()["primary"],
                     box=box.SQUARE,
                     expand=True)

    def move_up(self) -> None:
        """Moves the cursor up"""
        if (self.select_index > 0):
            self.select_index -= 1
            self.refresh()

    def move_down(self) -> None:
        """Moves the cursor down"""
        if (self.select_index < len(self.options) - 1):
            self.select_index += 1
            self.refresh()

    def __convert_list_to_text(self, options: list) -> Text:
        """
        The Widget outputs rich text that highlight the option that is
        currently available. This method creates the text that is
        rendered onto the widget.
        """
        styles = self.app.get_css_variables()
        text = Text()
        for i in range(len(self.options)):
            temp = Text(self.options[i] + "\n")
            if i == self.select_index:
                temp.stylize(f"{styles['background']} on {styles['foreground']}")
            text += temp

        return text


class TunnelSelect(SelectWidget):
    """Displays tunnels that can be selected"""

    def __init__(self, options: list) -> None:
        super().__init__(options)
