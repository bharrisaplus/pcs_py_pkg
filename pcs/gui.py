''' Show a deck of cards '''

from turtle import Turtle
from tkinter import (
    Frame as tkFrame,
    Button as tkButton,
    Canvas as tkCanvas,
    Tk
)


from ._constants import (
    save_icon_utf8 as floppy_code,
    boundingBoxType as boundingBox
)

from ._utils import (
    _capture_tkinter as screen_grab,
    get_card_color,
    get_card_symbol
)

# https://www.tcl-lang.org/man/tcl8.6/TkCmd/colors.htm
tk_card_colors: list[str] = ['midnight blue', 'firebrick', 'dark olive green', 'DarkOrange2']
tk_bg_colors: list[str] = ["Ivory2"]


class CloseUp():
    ''' A view of the card deck

    Show the cards using utf-8 symbols. Create widgets in tkinter based on the layout below:
        rootWindow
            cardFrame:
                [{Cards 1 - 13}]
                [{Cards 14 - 26}]
                [{Cards 27 - 39}]
                [{Cards 40 - 52}]
            controlFrame:
                [{saveButton}]

        When clicked, the saveButton will create an image file of the rootWindow and cardFrame.

    Attributes:
        rootWindow (Tk): Main widget. About half the screen
        cardFrame (tkFrame): Where cards render. About 4/5 of the rootWindow height
        controlsFrame (tkFrame): Where the save button renders. About 1/5 of the rootwindow height
        cardStyle (tuple[str, int]): Font family and font size for cards
        controlsStyle (tuple[str, int]): Font family and font size for save button
        cards_for_display (list[tuple[chr, int]]): Data to render the card
        screen_grab_filename (str): What to call the saved image
    '''

    def __init__(self, window_title, screen_grab_filename='shuffled') -> None:
        self.screen_grab_filename = screen_grab_filename

        self.rootWindow = Tk()

        window_height = int(self.rootWindow.winfo_screenheight() * 0.63)
        window_width = int(self.rootWindow.winfo_screenwidth() * 0.63)
        self.cardStyle = ('Consolas', int(window_height * 0.1325))
        self.controlsStyle = ('Consolas', int(window_height * 0.033))
        self.cards_for_display = None
        self.card_tag = 'card'

        self.rootWindow.title(window_title)
        self.rootWindow.geometry("{}x{}".format(window_width, window_height))
        self.rootWindow.grid_columnconfigure(0, weight=1)

        self.cardCanvas = tkCanvas(self.rootWindow, name='card_canvas',
            bd=0, highlightthickness=0,
            width=(window_width * 0.85) // 1, height=(window_height * 0.85) // 1
        )
        self.controlsFrame = tkFrame(self.rootWindow, bd=0, highlightthickness=0, pady=9)

        self.cardCanvas.grid()
        self.controlsFrame.grid()

    def get_coordinates_for_capture(self) -> boundingBox:
        ''' Determine where to capture screen at. Helper for CloseUp._save_window_command '''

        capture_area_start_x = self.rootWindow.winfo_rootx()
        capture_area_start_y = self.rootWindow.winfo_rooty()
        offset_y = self.controlsFrame.winfo_height()
        capture_area_end_x = capture_area_start_x + self.rootWindow.winfo_width()
        capture_area_end_y = capture_area_start_y + self.rootWindow.winfo_height() - offset_y

        return (capture_area_start_x, capture_area_start_y, capture_area_end_x, capture_area_end_y)

    def _save_window_command(self) -> None:
        ''' Click handler to grab screenshot then close window '''

        self.rootWindow.update_idletasks()
        screen_grab(self.get_coordinates_for_capture(), self.screen_grab_filename)
        self.rootWindow.destroy()


    def show_window(self) -> None:
        ''' Curtain Up '''

        tkButton(
            self.controlsFrame, relief="flat", font=self.controlsStyle, fg="goldenrod3",
            text=chr(int(floppy_code, 16)), command=self._save_window_command,
        ).pack()

        cardCanvas_width = self.cardCanvas.winfo_reqwidth()
        cardCanvas_height = self.cardCanvas.winfo_reqheight()

        for row_idx in range(4):
            for column_idx, info in enumerate(self.cards_for_display[row_idx*13:(row_idx+1)*13]):
                pos_x = column_idx * (cardCanvas_width // 13)
                pos_y = row_idx * (cardCanvas_height // 4)

                self.cardCanvas.create_text(pos_x, pos_y, anchor="nw", tags=self.card_tag,
                    text=info[0], font=self.cardStyle, fill=info[1]
                )

        self.rootWindow.mainloop()


    def load_cards(self, cards: list[int], color_per_suite: bool = False) -> None:
        ''' Create display ready cards '''
        _formatted = []

        for card in cards:
            _formatted.append((
                get_card_symbol(card), tk_card_colors[get_card_color(card, color_per_suite)]
            ))

        self.cards_for_display = _formatted


def hello_tutle() -> None:
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
