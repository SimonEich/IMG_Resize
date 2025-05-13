from tkinter import Entry, filedialog, Button, Label
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
        self.root.geometry('500x350')
        self.root.title('Resolution change')
    
    def _screen(self) -> None:
        """
        Set up all the UI elements on the window, including file selection 
        and image resolution buttons if a file is selected.
        """
        self.create_button('choose_File', 'Choose File', lambda: self.choose_file(), 0.5, 20)

        if hasattr(self, 'path') and self.path != 'path':
            self.create_button('create_Thumbnail', 'Create Thumbnail', 
                               lambda: self.logic.thumbnail_Resolution(self.path, 1280, 720), 0.25, 100)
            self.create_button('Remove Backgraound', 'Remove Background', 
                               lambda: self.logic.remove_background(self.path), 0.25, 150)
            self.create_button('remove_white', 'Remove White Pixels',
                               lambda: self.logic.remove_white_pixels(self.path), 0.25, 200)
            self.create_button('Custom resolution', 'Custom Resolution',
                               lambda: self.custom_resolution_screen(self.path), 0.25, 250)
            self.create_button('create_2x', 'Create 2x', 
                               lambda: self.logic.increase_Resolution(self.path, 2), 0.75, 100)
            self.create_button('create_4x', 'Create 4x', 
                               lambda: self.logic.increase_Resolution(self.path, 4), 0.75, 150)
            self.create_button('create_8x', 'Create 8x', 
                               lambda: self.logic.custom_resolution_screen(self.path), 0.75, 200)
        
        self.create_label(self.filename_var, 0.5, 50)
        

    def custom_resolution_screen(self, path) -> None:
        """
        Open a dialog to allow the user to enter a custom resolution.
        """
        self.custom_root = tk.Tk()
        self.custom_root.geometry('300x200')
        self.custom_root.title('Custom Resolution')

        # Labels and Entry fields
        Label(self.custom_root, text="Width:", font=("Arial", 12)).pack(pady=(20, 5))
        self.width_entry = Entry(self.custom_root, font=("Arial", 14), width=20)
        self.width_entry.pack()

        Label(self.custom_root, text="Height:", font=("Arial", 12)).pack(pady=(10, 5))
        self.height_entry = Entry(self.custom_root, font=("Arial", 14), width=20)
        self.height_entry.pack()

        # Define the callback function
        def apply_custom_resolution(self):
            try:
                width = int(self.width_entry.get())
                height = int(self.height_entry.get())
                if width <= 0 or height <= 0:
                    print("Please enter positive dimensions.")
                    return
                self.custom_root.destroy()  # Close the window
                self.logic.resize_to_custom_resolution(path, width, height)
            except ValueError:
                print("Invalid input. Please enter numeric values.")

        # Button
        button = Button(self.custom_root, text='Create', width=14, font=("Arial", 14), command= lambda: apply_custom_resolution(self))
        button.place(relx=0.5, y=150, anchor="n")

        self.custom_root.mainloop()


        
        
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
        button = Button(self.root, text=text, width=14, font=("Arial", 14), command=command)
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
