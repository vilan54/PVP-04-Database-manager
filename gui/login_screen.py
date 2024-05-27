from utils.db_connector import connect_database
from utils.colors import *
from customtkinter import *
from tkinter import *
from utils.warnings import show_message
from PIL import Image


class LoginScreen:
    def __init__(self, root, app):
        self.root = root
        self.app = app
        self.root.geometry("400x600")
        self.create_widgets()


    def create_widgets(self):
        self.frame = CTkFrame(master=self.root, fg_color=bg_color)
        self.frame.pack(padx=10, pady=10, fill="both", expand=True)

        self.create_logo()

        self.create_data_label()


    def create_logo(self):
        image_path = "./utils/images/logo.png"  # Ruta de la imagen
        image = CTkImage(light_image=Image.open(image_path),
                            dark_image=Image.open(image_path),
                            size=(100,100))
        self.image_label = CTkLabel(self.frame, image=image, text="")
        self.image_label.pack(pady=20)

    def create_data_label(self):
        self.data_frame = CTkFrame(self.frame, fg_color=bg_color)
        self.data_frame.pack(pady=5)

        self.username_label = CTkLabel(
            master=self.data_frame,
            text="Username",
            width=200,
            height=40,
            fg_color=bg_color,
            text_color=txt_color,
        )
        self.username_label.pack(fill="x", expand=True, pady=(0, 1))

        self.username_entry = CTkEntry(
            master=self.data_frame,
            placeholder_text="Username...",
            width=200,
            height=40,
            border_width=1,
            corner_radius=15,
            fg_color=bg_color,
            text_color=brd_color,
            border_color=brd_color
        )
        self.username_entry.pack(fill="x", expand=True)

        self.password_label = CTkLabel(
            master=self.data_frame,
            text="Password",
            width=200,
            height=40,
            fg_color=bg_color,
            text_color=txt_color,
        )
        self.password_label.pack(fill="x", expand=True, pady=(0, 1))

        self.password_entry = CTkEntry(
            master=self.data_frame,
            placeholder_text="Password...",
            show="*",
            width=200,
            height=40,
            border_width=1,
            corner_radius=15,
            fg_color=bg_color,
            text_color=brd_color,
            border_color=brd_color
        )
        self.password_entry.pack(fill="x", expand=True)

        self.host_label = CTkLabel(
            master=self.data_frame,
            text="Host",
            width=200,
            height=40,
            fg_color=bg_color,
            text_color=txt_color,
        )
        self.host_label.pack(fill="x", expand=True, pady=(0, 1))

        self.host_entry = CTkEntry(
            master=self.data_frame,
            placeholder_text="Host...",
            width=200,
            height=40,
            border_width=1,
            corner_radius=15,
            fg_color=bg_color,
            text_color=brd_color,
            border_color=brd_color
        )
        self.host_entry.pack(fill="x", expand=True, pady=(0, 50))

        login_button = CTkButton(master=self.data_frame, text="Login", command=self.connect_bd, width=125, height=30)
        login_button.pack(side="bottom")

    def connect_bd(self):
        self.user = self.username_entry.get()
        self.password = self.password_entry.get()
        self.host = self.host_entry.get()

        result = connect_database(self.user, self.password, self.host)

        if isinstance(result, dict):
            # Hubo un error al conectar
            error_message = f"Error code: {result['error_code']}\nSQLSTATE value: {result['sqlstate']}\nError message: {result['error_message']}"
            if result['error_code'] == 1045:
                show_message(self.frame, "User or password incorrect", "cancel")
            elif result['error_code'] == 2005:
                show_message(self.frame, "Host incorrect", "cancel")
            else:
                show_message(self.frame, error_message, "cancel")
        elif result:
            self.app.conn = result
            self.frame.destroy()
            self.app.show_main_screen(self.user, self.host)
        else:
            show_message(self.frame, "Something went wrong!!!", "cancel")


