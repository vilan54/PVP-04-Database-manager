from customtkinter import *
from utils.colors import *
from utils.db_connector import *
from PIL import Image
from utils.warnings import show_message
from utils.ctk_xyframe import *


class MainScreen:
    def __init__(self, root, app, user, host):
        self.root = root
        self.app = app
        self.user = user
        self.host = host
        self.root.minsize(750, 500)
        self.root.geometry("1000x600")
        self.create_frames()
        self.show_header()
        self.show_options(table=None)

    def create_frames(self):
        self.frame = CTkFrame(master=self.root, fg_color=bg_color)
        self.frame.pack(fill="both", expand=True)
        
        self.header_frame = CTkFrame(master=self.frame, fg_color=bg_color)
        self.header_frame.pack(fill="x", side="top")

        self.options_frame = CTkFrame(master=self.frame, fg_color=bg_color, border_color=tbg_color, border_width=1)
        self.options_frame.pack(padx=10, pady=10, side="bottom", fill="x")
        
        self.tables_frame = CTkScrollableFrame(master=self.frame, fg_color=bg_color, width=300, scrollbar_fg_color=tbg_color,
                                               border_width=1, border_color=tbg_color, corner_radius=10)
        self.tables_frame.pack(padx=10, pady=10, side="left", fill="y")
        
        self.details_frame = CTkFrame(master=self.frame, fg_color=bg_color, border_color=tbg_color, border_width=1)
        self.details_frame.pack(padx=10, pady=10, side="left", fill="both", expand=True)

    def show_header(self):

        image_path = "./utils/images/logo.png"  # Ruta de la imagen
        image = CTkImage(light_image=Image.open(image_path),
                            dark_image=Image.open(image_path),
                            size=(50,50))
        self.image_label = CTkLabel(self.header_frame, image=image, text="")
        self.image_label.pack(side="left", padx=(30, 0), pady=(6, 0))

        username_placeholder = CTkLabel(master=self.header_frame, text="Username:", fg_color=bg_color, text_color=tbg_color)
        username_placeholder.pack(side="left", padx=(30, 0), pady=(6, 0))

        username_label = CTkLabel(master=self.header_frame, text=self.user, fg_color=bg_color, text_color=hd_color)
        username_label.pack(side="left", padx=(5, 0), pady=(6, 0))

        current_font = username_label.cget("font")
        new_font = (current_font, 12, "bold")
        username_label.configure(font=new_font)

        host_placeholder = CTkLabel(master=self.header_frame, text="Host:", fg_color=bg_color, text_color=tbg_color)
        host_placeholder.pack(side="left", padx=(30, 0), pady=(6, 0))

        host_label = CTkLabel(master=self.header_frame, text=self.host, fg_color=bg_color, text_color=hd_color)
        host_label.pack(side="left", padx=(5, 0), pady=(6, 0))

        current_font = host_label.cget("font")
        new_font = (current_font, 12, "bold")
        host_label.configure(font=new_font)

        databases_raw = load_databases(self.app.conn)
        databases = [db[0] for db in databases_raw]

        self.combobox = CTkComboBox(master=self.header_frame, values=databases, width=200, border_color=tbg_color, 
                        fg_color=bg_color, border_width=1, text_color=hd_color, dropdown_text_color=tbg_color,
                        dropdown_fg_color=bg_color, justify="center", command=self.get_tables)
        self.combobox.pack(side="left", padx=(30, 0), pady=(6, 0))

        exit_button = CTkButton(master=self.header_frame, text="Exit", width=50, command=self.back_login)
        exit_button.pack(side="right", padx=20)

        self.get_tables(self.combobox.get())
    
    def back_login(self):
        self.frame.destroy()
        self.app.show_login_screen()

    def get_tables(self, database):
        tables_raw = load_tables(conn=self.app.conn, database=database)
        
        if isinstance(tables_raw, dict):
            # Hubo un error al conectar
            error_message = f"Error code: {tables_raw['error_code']}\nSQLSTATE value: {tables_raw['sqlstate']}\nError message: {tables_raw['error_message']}"
            show_message(self.frame, error_message, "cancel")
        elif tables_raw:
            tables = [db[0] for db in tables_raw]
            self.show_tables(tables)
        else:
            show_message(self.frame, "Something went wrong!!!", "cancel")

    def show_tables(self, tables):
        for widget in self.tables_frame.winfo_children():
            widget.destroy()

        for table in tables:
            self.table_label = CTkButton(master=self.tables_frame, text=table, fg_color=bg_color, text_color=tbg_color, command=lambda t=table: self.show_data(t))
            current_font = self.table_label.cget("font")
            new_font = (current_font, 10)
            self.table_label.configure(font=new_font)
            self.table_label.pack()

    def show_data(self, table):
        for widget in self.details_frame.winfo_children():
            widget.destroy()

        top_frame = CTkFrame(master=self.details_frame, fg_color=bg_color)
        top_frame.pack(side="top", padx=15, pady=5, fill="x")

        username_placeholder = CTkLabel(master=top_frame, text="Table:", fg_color=bg_color, text_color=tbg_color)
        username_placeholder.grid(row=0, column=0, padx=(1, 0), pady=(1, 0))

        username_label = CTkLabel(master=top_frame, text=table, fg_color=bg_color, text_color=hd_color)
        username_label.grid(row=0, column=1, padx=(5, 0), pady=(1, 0))

        current_font = username_label.cget("font")
        new_font = (current_font, 12, "bold")
        username_label.configure(font=new_font)

        data_frame = CTkXYFrame(master=self.details_frame, fg_color=bg_color, scrollbar_fg_color=tbg_color,
                                        border_color=tbg_color, border_width=1)
        data_frame.pack(padx=10, pady=10, fill="both", expand=True)


        columns_raw = get_columns_name(self.app.conn, table)
        columns = [column[0] for column in columns_raw]

        column_frame = CTkFrame(master=data_frame, fg_color=bg_color, height=30)
        column_frame.pack(side="top", padx=5, pady=2)

        data = get_data(self.app.conn, table)


        if data:
            column_widths = [len(str(attribute)) if attribute else 1 for attribute in data[0]]
        else:
            column_widths = [1] * len(columns)

        for row in data[1:]:
            for index, attribute in enumerate(row):
                if column_widths[index] < len(str(attribute)):
                    column_widths[index] = len(str(attribute))

        column_widths = [width * 7 for width in column_widths]

        for index, (column, width) in enumerate(zip(columns, column_widths)):
            table_button = CTkButton(master=column_frame, text=column, fg_color=cl_color, corner_radius=25,
                                    text_color=tbg_color, border_color=cl_color, border_width=1, width=width)
            current_font = table_button.cget("font")
            new_font = (current_font, 10, "bold")
            table_button.configure(font=new_font)
            table_button.pack(side="left", fill="x", expand=True, padx=5, pady=5)

        for line_index, line in enumerate(data):
            line_frame = CTkFrame(master=data_frame, fg_color=bg_color, height=30, border_color=tbg_color, border_width=1, corner_radius=20)
            line_frame.pack(side="top", fill="x", padx=5, pady=2)

            for index, (attribute, width) in enumerate(zip(line, column_widths)):
                attribute_label = CTkLabel(master=line_frame, text=attribute, fg_color=None, text_color=tbg_color, width=width, anchor="w", corner_radius=20)  # Usa `width` calculado
                attribute_label.pack(side="left", fill="x", expand=True, padx=10, pady=1)

        self.show_options(table)
                
    def show_options(self, table):
        for widget in self.options_frame.winfo_children():
            widget.destroy()

        create_table_button = CTkButton(master=self.options_frame, text="Create Table", command=self.create_table)
        create_table_button.pack(side="right", padx=20, pady=10)

        if table is not None:
            add_data_button = CTkButton(master=self.options_frame, text="Add Data")
            add_data_button.pack(side="right", pady=10)

    def create_table(self):
        self.options_frame.destroy()
        self.tables_frame.destroy()
        self.details_frame.destroy()
        self.header_frame.destroy()
        self.frame.destroy()
        self.app.show_create_table_screen()

    
                




        
