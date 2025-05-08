from tkinter import *
import tkinter as tk
from tkinter import *
import tkinter as tk
from typing import Callable

path='path'

class GUI:
    def __init__(self, logic):
        self.logic=logic
        self._config_screen()
        self._screen()
        
    def _config_screen(self) -> None:
        self.root = tk.Tk()  
        self.root.geometry('500x300')
        self.root.title('Resolution change')  
    
    def _screen(self) -> None:
        self.create_button('choose_File', 'Choose File',            lambda: self.logic.click('a'), 0.25, 20)
        self.create_button('output_File', 'Output File',            lambda: self.logic.click, 0.75, 20)
        self.create_button('create_Thumbnail', 'Create Thumbnail',  lambda: self.logic.thumbnail_Resolution(path), 0.25, 100)
        self.create_button('create_2x', 'Create 2x',                lambda: self.logic.increase_Resolution(path, 2), 0.75, 100)
        self.create_button('create_4x', 'Create 4x',                lambda: self.logic.increase_Resolution(path, 4), 0.75, 150)
        self.create_button('create_8x', 'Create 8x',                lambda: self.logic.increase_Resolution(path, 8), 0.75, 200)

        
    def create_button(self, name_Button: str, text: str, command: Callable[[], None], x: float, y: int) -> None:
        button = Button(self.root, text=text, width=12, font=("Arial", 14), command=command)
        button.place(relx=x, y=y, anchor="n")
        setattr(self, name_Button, button)  # Optional: store the button by name
            
    def label(self) -> None:
        label = tk.Label(self.root, text='Start', font=("Arial", 24, "bold"))
        label.place(relx=0.25, y=10, anchor="n")        
    
    def click_test(self) -> None:
        print('test')



#Resolution 2, 4, 8
#Resolution Thumbnail
# choose IMG
# choose output