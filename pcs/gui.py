''' Show a deck of cards '''

from tkinter.ttk import Combobox as tkCombobox
from tkinter import (
    Frame as tkFrame,
    Button as tkButton,
    Canvas as tkCanvas,
    PhotoImage as tkImage,
    EventType as tkEventType,
    Event as tkEvent,
    Tk
)


from ._constants import (
    save_icon_utf8 as floppy_code,
    boundingBoxType as boundingBox,
    sqwiggle_b16_path as sqwiggle_b16,
    sqwiggle_b32_path as sqwiggle_b32
)

from ._utils import (
    _capture_tkinter as screen_grab,
    get_card_color,
    get_card_symbol
)

# https://www.tcl-lang.org/man/tcl8.6/TkCmd/colors.htm
tk_card_colors: list[str] = ['midnight blue', 'firebrick', 'dark olive green', 'DarkOrange2']
tk_bg_colors: list[str] = ['ivory2', 'ivory3', 'snow', 'AntiqueWhite2', 'bisque2', 'cornsilk2', 'honeydew2', 'lavender blush', 'LightYellow2']


class CloseUp():
    ''' A view of the card deck

    Show the cards using utf-8 symbols. Create widgets in tkinter based on the layout below:
        rootWindow
            cardFrame:
                [{Cards 1 - 13}]
                [{Cards 14 - 26}]
                [{Cards 27 - 39}]
                [{Cards 40 - 52}]
            controlsFrame:
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
        self.controlsStyle = ('Consolas', int(window_height * 0.03))
        self.cards_for_display = None
        self.card_tag = 'card'

        self.rootWindow.title(window_title)
        self.rootWindow.geometry("{}x{}".format(window_width, window_height))
        self.rootWindow.grid_columnconfigure(0, weight=1)
        self.rootWindow.configure(bg=tk_bg_colors[0])
        self.rootWindow.wm_iconphoto(True, tkImage(file=sqwiggle_b16), tkImage(file=sqwiggle_b32))

        self.cardCanvas = tkCanvas(self.rootWindow, name='card_canvas',
            bd=0, highlightthickness=0, bg=tk_bg_colors[0],
            width=(window_width * 0.85) // 1, height=(window_height * 0.85) // 1
        )
        self.controlsFrame = tkFrame(self.rootWindow, name='controls_frame',
            bd=0, highlightthickness=0, bg=tk_bg_colors[0],
            padx=(window_width * 0.025), pady=(window_width * 0.025)
        )

        self.cardCanvas.grid()
        self.controlsFrame.grid(sticky='ew')

        self._last_tilt_event = None
        self._last_untilt_event = None

    def _slant_card(self, _event: tkEvent) -> None:
        ''' Create effect where cards move as mouse hovers over '''

        _item_id = _event.widget.find_withtag("current")

        if _event.type == tkEventType.Enter:
            if self._last_tilt_event:
                _event.widget.after_cancel(self._last_tilt_event)

            self._last_tilt_event = _event.widget.after_idle(
                lambda: _event.widget.itemconfig(_item_id, angle=2.8125) if _item_id else None
            )
        else:
            if self._last_untilt_event:
                _event.widget.after_cancel(self._last_untilt_event)

            self._last_untilt_event = _event.widget.after_idle(
                lambda: _event.widget.itemconfig(_item_id, angle=0) if _item_id else None
            )


    def _update_background(self, _event: tkEvent) -> None:
        ''' Seclect handler for Combobox to upate the colors for various widgets based on user pick '''

        self.rootWindow.update_idletasks()

        selected_option = _event.widget.get()

        if self.rootWindow.cget('bg') != selected_option:
            self.rootWindow.configure(bg=selected_option)
            self.cardCanvas.configure(bg=selected_option)
            self.controlsFrame.configure(bg=selected_option)

            save_button = self.controlsFrame.nametowidget("save_button")

            if save_button:
                save_button.configure(bg=selected_option, activebackground=selected_option)

    def get_coordinates_for_capture(self) -> boundingBox:
        ''' Determine where to capture screen at. Helper for CloseUp._save_window_command '''

        capture_area_start_x = self.rootWindow.winfo_rootx()
        capture_area_start_y = self.rootWindow.winfo_rooty()

        capture_area_end_x = capture_area_start_x + self.rootWindow.winfo_width()
        capture_area_end_y = capture_area_start_y + self.cardCanvas.winfo_height()

        return (capture_area_start_x, capture_area_start_y, capture_area_end_x, capture_area_end_y)

    def _save_window_command(self) -> None:
        ''' Click handler to grab screenshot then close window '''

        self.rootWindow.update_idletasks()
        screen_grab(self.get_coordinates_for_capture(), self.screen_grab_filename)
        self.rootWindow.destroy()


    def show_window(self) -> None:
        ''' Curtain Up '''

        backgroundDropdown = tkCombobox(self.controlsFrame, values=tk_bg_colors, state='readonly')

        backgroundDropdown.pack(side='left')
        backgroundDropdown.current(0)

        tkButton(self.controlsFrame, name='save_button',
            text=chr(int(floppy_code, 16)), relief="flat", font=self.controlsStyle, bd=0,
            bg=tk_bg_colors[0], fg="dim gray", activebackground=tk_bg_colors[0],
            activeforeground='dim gray', command=self._save_window_command,
        ).pack(side='right')

        cardCanvas_width = self.cardCanvas.winfo_reqwidth()
        cardCanvas_height = self.cardCanvas.winfo_reqheight()

        backgroundDropdown.bind('<<ComboboxSelected>>', self._update_background)
        self.cardCanvas.tag_bind(self.card_tag, "<Enter>", self._slant_card)
        self.cardCanvas.tag_bind(self.card_tag, "<Leave>", self._slant_card)

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
