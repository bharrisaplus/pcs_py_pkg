''' Show a deck of cards '''

from turtle import Turtle
from tkinter import (
    Frame as tkFrame,
    Button as tkButton,
    Label as tkLabel,
    Tk
)


from ._constants import save_icon_utf8 as floppy_code

from ._utils import (
    _capture_tkinter as screen_grab,
    get_card_color,
    get_card_symbol
)

# https://www.tcl-lang.org/man/tcl8.6/TkCmd/colors.htm
tk_card_colors = ['midnight blue', 'firebrick', 'dark olive green', 'DarkOrange2']
tk_bg_colors = ["Ivory2"]


class CloseUp():
    ''' A view of the card deck '''

    def __init__(self, window_title, screen_grab_filename='shuffled'):
        self.screen_grab_filename = screen_grab_filename

        self.rootWindow = Tk()
        self.rootWindow.withdraw()

        window_height = int(self.rootWindow.winfo_screenheight() * 0.63)
        window_width = int(self.rootWindow.winfo_screenwidth() * 0.63)
        self.cardStyle = ('Consolas', int(window_height * 0.1325))
        self.controlsStyle = ('Consolas', int(window_height * 0.033))
        self.cards_for_display = None

        self.rootWindow.title(window_title)
        self.rootWindow.geometry("{}x{}".format(window_width, window_height))
        self.rootWindow.grid_columnconfigure(0, weight=1)

        self.cardFrame = tkFrame(self.rootWindow, bd=0, highlightthickness=0)
        self.controlsFrame = tkFrame(self.rootWindow, bd=0, highlightthickness=0, pady=9)

        self.cardFrame.grid()
        self.controlsFrame.grid()

    def get_coordinates_for_capture(self):
        '''Set the points for the crop bounding box

        Returns:
            tuple: (int, int, int, int)
        '''

        capture_area_start_x = self.rootWindow.winfo_rootx()
        capture_area_start_y = self.rootWindow.winfo_rooty()
        offset_y = self.controlsFrame.winfo_height()
        capture_area_end_x = capture_area_start_x + self.rootWindow.winfo_width()
        capture_area_end_y = capture_area_start_y + self.rootWindow.winfo_height() - offset_y

        return (capture_area_start_x, capture_area_start_y, capture_area_end_x, capture_area_end_y)

    def _save_window_command(self):
        ''' Click handler to grab screenshot then close window '''

        self.rootWindow.update_idletasks()
        screen_grab(self.get_coordinates_for_capture(), self.screen_grab_filename)
        self.rootWindow.destroy()


    def show_window(self):
        ''' Display shuffled cards

        Show the cards using utf-8 symbols, create a layout in tkinter like:
            rootWindow
                cardFrame:
                    [{Cards 1 - 13}]
                    [{Cards 14 - 26}]
                    [{Cards 27 - 39}]
                    [{Cards 40 - 52}]
                controlFrame:
                    [{saveButton}]

            When clicked, the saveButton will create an image file of the rootWindow and cardFrame.
        '''

        tkButton(
            self.controlsFrame, relief="flat", font=self.controlsStyle, fg="goldenrod3",
            text=chr(int(floppy_code, 16)), command=self._save_window_command,
        ).pack()

        for row_idx in range(4):
            for column_idx, info in enumerate(self.cards_for_display[row_idx*13:(row_idx+1)*13]):
                tkLabel(
                    self.cardFrame, text=info[0], font=self.cardStyle, fg=info[1]
                ).grid(column=column_idx, row=row_idx)

        self.rootWindow.deiconify()
        self.rootWindow.mainloop()


    def load_cards(self, cards, color_per_suite=False):
        ''' Create display ready cards

        Args:
            cards (tuple[tuple(str, int)], list[int]]): See _utils.py@_setup_52
            color_per_suite (bool: Whether to use one color per suite (default: False)
        '''
        _formatted = []

        for card in cards:
            _formatted.append((
                get_card_symbol(card), tk_card_colors[get_card_color(card, color_per_suite)]
            ))

        self.cards_for_display = _formatted


def hello_tutle():
    ''' Print card symbols to screen '''

    s1 = chr(int(card_to_utf8.get(('spade', 1)), 16))
    d1 = chr(int(card_to_utf8.get(('diamond', 1)), 16))
    style = ('Consolas', 45)
    tooter = Turtle()

    tooter.screen.title('pcs: hello tooter turtle')
    tooter.penup()
    tooter.color('deep pink')
    tooter.goto(0, 30)
    tooter.write(s1, font=style, move=True)
    tooter.goto(50, 30)
    tooter.write(d1, font=style, move=True)
    tooter.hideturtle()

    tooter.screen.mainloop()


if __name__ == '__main__':
    hello_tutle()
