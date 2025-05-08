from gui.gui_base import GUI
from helper.logic import Logic


if __name__ == "__main__":
    
    logic = Logic()
    gui = GUI(logic)
    
    
    
    
    gui.root.mainloop()