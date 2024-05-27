from CTkMessagebox import CTkMessagebox
from utils.colors import *

def show_message(frame, message, icon):
        msg = CTkMessagebox(
                title="Error",
                message=message,
                justify="center",
                icon=icon,
                option_1="OK",
                width=100,
                height=200,
                fg_color=bg_color,
            )
        msg_x = (frame.winfo_rootx()) + (frame.winfo_width()//2) - (msg.winfo_width()//2)
        msg_y = (frame.winfo_rooty()) + (frame.winfo_height()//2) - (msg.winfo_height()//2)
        msg.geometry(f'+{msg_x}+{msg_y}')