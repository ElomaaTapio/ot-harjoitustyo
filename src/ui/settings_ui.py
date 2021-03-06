from tkinter import Button, StringVar, Toplevel, Radiobutton, Grid, NSEW, NW, W, Label, Entry, DISABLED, NORMAL, messagebox


class SettingsUI():
    """Window where settings for the game can be altered.
    Attributes:
        root: Main window.
        settings_handler: Setting object.
        game: GameWindow
        options: Array of preset options.
        widgets: Array of widgets on the popup.
        setting: Variable for the selected setting.
        error: Boolean for determining invalid input.
        settings: Array of current settings
        playheight: GameUI height.
        playwidth: GameUI width.
        boxsize: GameUI size of the squares.
        pop: Popup window. Everything displayed is here.
    """

    def __init__(self, root, settings_handler, game):
        """Constructor. Sets up attributes.
        Args:
            root: Main window
            settings_handler: Setting object.
            game: GameUI object.
        """
        self.root = root
        self.settings_handler = settings_handler
        self.game = game
        self.options = ["10;10;10;50", "16;16;40;50", "16;30;99;50"]
        self.widgets = []
        self.setting = StringVar()
        self.error = False
        self.main()

    def main(self):
        """Calls functions to generate settings popup.
        """
        self.current_settings()
        self.pop = Toplevel(self.root)
        self.pop.title("Settings")
        self.geometry()
        self.focus()
        self.buttons()
        self.labels()
        self.grid_config()

    def current_settings(self):
        """Gets current game settings.
        """
        self.settings = self.settings_handler.load().split(";")
        self.playheight = int(self.settings[0])
        self.playwidth = int(self.settings[1])
        self.boxsize = int(self.settings[3])

    def geometry(self):
        """Sets the popup window size and positions it in the center of the GameUI.
        """
        geometry_x = self.root.winfo_x()+(self.boxsize//2)*self.playwidth-150
        geometry_y = self.root.winfo_y()+(self.playheight + 1)*(self.boxsize//2)-100
        self.pop.geometry(f"300x200+{geometry_x}+{geometry_y}")
        self.pop.resizable(False, False)

    def focus(self):
        """Grabs focus to the popup window and prevent interactions with the GameUI.
        """
        self.pop.focus_set()
        self.pop.wait_visibility()
        self.pop.grab_set()

    def labels(self):
        """Generates text on the popup window
        """
        label = Label(self.pop, text="Options:")
        label.grid(row=0, column=0, sticky=NW)
        texts = ["Height (5-20):", "Width (5-25):", "Mines (1-500):"]
        for i in range(3):
            label = Label(self.pop, text=texts[i])
            label.grid(row=i+1, column=1)

    def buttons(self):
        """Generates buttons on the popup window
        """
        texts = ["10x10 grid\n 10 mines",
                 "16x16 grid\n 40 mines", "16x30 grid\n 99 mines"]
        for i in range(3):
            button = Radiobutton(self.pop, variable=self.setting)
            button.config(
                text=texts[i], value=self.options[i], command=self.check_custom)
            button.grid(row=i+1, column=0, sticky=NSEW)
            self.widgets.append(button)
        self.custom_game_widgets()
        self.set_states()
        button4 = Button(self.pop, text="OK", command=self.change_setting)
        button4.grid(row=4, column=0, sticky=NSEW)
        button5 = Button(self.pop, text="Cancel", command=self.pop.destroy)
        button5.grid(row=4, column=2, sticky=NSEW)

    def custom_game_widgets(self):
        """Generates radiobutton and entrys for inputting custom game settings.
        """
        button = Radiobutton(
            self.pop, text="custom", variable=self.setting, value="1", command=self.check_custom)
        button.grid(row=0, column=1, sticky=NW)
        self.widgets.append(button)
        for i in range(3):
            entry = Entry(self.pop, width=5)
            entry.grid(row=i+1, column=2, sticky=W)
            self.widgets.append(entry)

    def set_states(self):
        """Sets radiobutton states.
        """
        current = self.settings_handler.load()
        if current not in self.options:
            self.widgets[3].select()
        else:
            self.check_custom()
            for i in range(len(self.options)):
                if self.options[i] == current:
                    self.widgets[i].select()
                else:
                    self.widgets[i].deselect()

    def check_custom(self):
        """Checks if the custom setting option is selected and
        disables or activates the entry boxes accordingly.
        """
        if self.setting.get() == "1":
            for i in self.widgets[4:]:
                i.config(state=NORMAL)
        else:
            for i in self.widgets[4:]:
                i.config(state=DISABLED)

    def grid_config(self):
        """Configures the placement grid.
        """
        for j in range(5):
            Grid.rowconfigure(self.pop, j, weight=1)
        for i in range(3):
            Grid.columnconfigure(self.pop, i, weight=1)

    def change_setting(self):
        """Writes new settings to setting file.
        """
        self.error = False
        if self.setting.get() == "1":
            try:
                correct, setting = self.get_entry()
                if correct:
                    self.settings_handler.write(setting)
            except TypeError:
                self.error = True
        else:
            self.settings_handler.write(self.setting.get())
        if not self.error:
            self.pop.destroy()
            self.game.reset(True)

    def get_entry(self):
        """Formulates a string out of the contents of the entry boxes.
        """
        try:
            setting = ""
            height = int(self.widgets[4].get())
            width = int(self.widgets[5].get())
            mines = int(self.widgets[6].get())
            correct = False
            if 5 <= height <= 20:
                setting += self.widgets[4].get() + ";"
                if 5 <= width <= 25:
                    setting += self.widgets[5].get() + ";"
                    if 1 <= mines <= 500 and height*width-8 > mines:
                        setting += self.widgets[6].get() + ";"
                        correct = True
            setting += "50"
            if correct:
                return correct, setting
            else:
                messagebox.showerror(
                    "Error", "Values out of range or too many mines")
        except ValueError:
            messagebox.showerror("Error", "Invalid input")
            self.error = True
