from tkinter import filedialog, Button, Label
import tkinter as tk
from typing import Callable

class GUI:
    def __init__(self, logic):
        """
        Initialize the GUI with the given logic handler.
        
        Args:
            logic: An object that handles the core image processing logic.
        """
        self.logic = logic
        self._config_screen()
        self.filename_var = tk.StringVar()
        self._screen()
        
    def _config_screen(self) -> None:
        """
        Configure the main window properties like size and title.
        """
        self.root = tk.Tk()
        self.root.geometry('500x300')
        self.root.title('Resolution change')
    
    def _screen(self) -> None:
        """
        Set up all the UI elements on the window, including file selection 
        and image resolution buttons if a file is selected.
        """
        self.create_button('choose_File', 'Choose File', lambda: self.choose_file(), 0.5, 20)

        if hasattr(self, 'path') and self.path != 'path':
            self.create_button('create_Thumbnail', 'Create Thumbnail', 
                               lambda: self.logic.thumbnail_Resolution(self.path), 0.25, 100)
            self.create_button('Remove Backgraound', 'Remove Background', 
                               lambda: self.logic.remove_background(self.path), 0.25, 150)
            self.create_button('create_2x', 'Create 2x', 
                               lambda: self.logic.increase_Resolution(self.path, 2), 0.75, 100)
            self.create_button('create_4x', 'Create 4x', 
                               lambda: self.logic.increase_Resolution(self.path, 4), 0.75, 150)
            self.create_button('create_8x', 'Create 8x', 
                               lambda: self.logic.increase_Resolution(self.path, 8), 0.75, 200)
        
        self.create_label(self.filename_var, 0.5, 50)

    def create_button(self, name_Button: str, text: str, command: Callable[[], None], x: float, y: int) -> None:
        """
        Create a button and place it on the window.
        
        Args:
            name_Button: Name used to store the button as an attribute.
            text: Text displayed on the button.
            command: Function to be called when the button is clicked.
            x: Relative horizontal position (0 to 1).
            y: Absolute vertical position in pixels.
        """
        button = Button(self.root, text=text, width=12, font=("Arial", 14), command=command)
        button.place(relx=x, y=y, anchor="n")
        setattr(self, name_Button, button)
            
    def create_label(self, text, x, y) -> None:
        """
        Create a label to display dynamic text.
        
        Args:
            text: A StringVar instance used to update the label's content.
            x: Relative horizontal position (0 to 1).
            y: Absolute vertical position in pixels.
        """
        label = tk.Label(self.root, textvariable=text, font=("Arial", 15, "bold"))
        label.place(relx=x, y=y, anchor="n")        
    

    def choose_file(self) -> None:
        """
        Open a file dialog for the user to select an image file.
        Updates the GUI with additional resolution buttons after selection.
        """
        path = filedialog.askopenfilename()
        if path:
            self.filename_var.set(path.split('/')[-1])  # show just the file name
            self.path = path
            self._screen()
