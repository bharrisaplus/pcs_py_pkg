''' Show a deck of cards '''

import tkinter
from turtle import Turtle

from ._constants import (
    save_icon_utf8 as floppy_code,
    card_group_a,
    card_group_b,
    card_to_utf8
)

from ._utils import _capture_tkinter as screen_grab


class CloseUp():
    ''' A view of the card deck '''

    def __init__(self, window_title, screen_grab_filename='shuffled'):
        self.screen_grab_filename = screen_grab_filename

        self.rootWindow = tkinter.Tk()
        self.rootWindow.withdraw()

        window_height = int(self.rootWindow.winfo_screenheight() * 0.63)
        window_width = int(self.rootWindow.winfo_screenwidth() * 0.63)
        self.cardStyle = ('Consolas', int(window_height * 0.1325))
        self.controlsStyle = ('Consolas', int(window_height * 0.033))
        self.cardFrame = tkinter.Frame(self.rootWindow, bd=0, highlightthickness=0)
        self.controlsFrame = tkinter.Frame(self.rootWindow, bd=0, highlightthickness=0)
        self.cards_for_display = None

        self.rootWindow.title(window_title)
        self.rootWindow.geometry("{}x{}".format(window_width, window_height))
        self.rootWindow.grid_columnconfigure(0, weight=1)
        self.cardFrame.grid()
        self.controlsFrame.grid()

    def get_coordinates_for_capture(self):
        '''Set the points for the crop bounding box

        Returns:
            tuple: (int, int, int, int)
        '''
        self.rootWindow.update_idletasks()

        capture_area_start_x = self.rootWindow.winfo_rootx()
        capture_area_start_y = self.rootWindow.winfo_rooty()
        offset_y = self.controlsFrame.winfo_height() + 20
        capture_area_end_x = capture_area_start_x + self.rootWindow.winfo_width()
        capture_area_end_y = capture_area_start_y + self.rootWindow.winfo_height() - offset_y

        return (capture_area_start_x, capture_area_start_y, capture_area_end_x, capture_area_end_y)

    def _save_window_command(self):
        ''' Create wrapper method to grab screenshot and close window '''

        def run_command():
            ''' Passed to the command= param for tkinter button widget and invoked upon click '''

            screen_grab(self.get_coordinates_for_capture(), self.screen_grab_filename)
            self.rootWindow.destroy()

        return run_command

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
        tkinter.Button(
            self.controlsFrame, relief="flat", font=self.controlsStyle, fg="goldenrod3",
            text=chr(int(floppy_code, 16)), command=self._save_window_command()
        ).pack()

        for frame_idx, card_info in enumerate(self.cards_for_display[:13]):
            tkinter.Label(
                self.cardFrame, text=card_info[0], font=self.cardStyle, fg=card_info[1]
            ).grid(column=frame_idx, row=0)

        for frame_idx, card_info in enumerate(self.cards_for_display[13:26]):
            tkinter.Label(
                self.cardFrame, text=card_info[0], font=self.cardStyle, fg=card_info[1]
            ).grid(column=frame_idx, row=1)

        for frame_idx, card_info in enumerate(self.cards_for_display[26:39]):
            tkinter.Label(
                self.cardFrame, text=card_info[0], font=self.cardStyle, fg=card_info[1]
            ).grid(column=frame_idx, row=2)

        for frame_idx, card_info in enumerate(self.cards_for_display[39:]):
            tkinter.Label(
                self.cardFrame, text=card_info[0], font=self.cardStyle, fg=card_info[1]
            ).grid(column=frame_idx, row=3)

        self.rootWindow.deiconify()
        self.rootWindow.mainloop()

    def get_color_for_suite(self, card_suite, color_per_suite=False):
        '''Pick the tkinter color for the card suite

        Args:
            card_suite (str):
            color_per_suite (bool): Whether to use one color per suite (default: False)

        Returns:
            str: tkinter color name
        '''

        suite_color = None

        if card_suite in card_group_a:
            suite_color = 'midnight blue'

            if color_per_suite and card_suite == card_group_a[1]:
                suite_color = 'dark olive green'

        if card_suite in card_group_b:
            suite_color = 'firebrick'

            if color_per_suite and card_suite == card_group_b[1]:
                suite_color = 'DarkOrange2'

        return suite_color

    def load_cards(self, cards, color_per_suite=False):
        ''' Create display ready cards

        Args:
            cards (tuple[tuple(str, int)], list[int]]): See _utils.py@_setup_52
            color_per_suite (bool: Whether to use one color per suite (default: False)
        '''
        _formatted = []

        for card in cards:
            _formatted.append((
                chr(int(card_to_utf8.get(card), 16)),
                self.get_color_for_suite(card[0], color_per_suite)
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
