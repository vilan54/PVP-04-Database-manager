from customtkinter import CTk
from gui.login_screen import LoginScreen
from gui.main_screen import MainScreen
from gui.create_table_screen import CreateTableScreen
from utils.colors import *

class DatabaseApp:
    def __init__(self, root):
        self.root = root    
        self.conn = None
        self.show_login_screen()

    def show_login_screen(self):
        LoginScreen(self.root, self)

    def show_main_screen(self, user, host):
        MainScreen(self.root, self, user, host)

    def show_create_table_screen(self):
        CreateTableScreen(self.root, self)
        

if __name__ == "__main__" :
    root = CTk()
    root.geometry('400x600')
    root.minsize(300, 500)

    root.config(bg=bg_color)
    
    app = DatabaseApp(root)

    root.mainloop()