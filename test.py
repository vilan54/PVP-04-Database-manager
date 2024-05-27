from tkinter import Tk, Label, font
import tkinter.font as tkfont

root = Tk()

# Lista de fuentes
# gubbi
font_families = tkfont.families()[10:30] 

for fuente in font_families:
    # Crear una etiqueta con la fuente actual
    etiqueta = Label(root, text=fuente, font=(fuente, 12))
    etiqueta.pack()

root.mainloop()