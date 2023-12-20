"""
Виджет Combobox представляет выпадающий список, из которого пользователь может выбрать один элемент. Фактически он представляет комбинацию виджетов Entry и Listbox.

Основные параметры конструктора Combobox:

values: список строк для отображения в Combobox

background: фоновый цвет

cursor: курсор указателя мыши при наведении на текстовое поле

foreground: цвет текста

font: шрифт текста

justify: устанавливает выравнивание текста. Значение LEFT выравнивает текст по левому краю, CENTER - по центру, RIGHT - по правому краю

show: задает маску для вводимых символов

state: состояние элемента, может принимать значения NORMAL (по умолчанию) и DISABLED

textvariable: устанавливает привязку к элементу StringVar

height: высота элемента

width: ширина элемента

Определим простейший выпадающий список:

from tkinter import *
from tkinter import ttk

root = Tk()
root.title("METANIT.COM")
root.geometry("250x200")

languages = ["Python", "C#", "Java", "JavaScript"]
combobox = ttk.Combobox(values=languages)
combobox.pack(anchor=NW, padx=6, pady=6)

root.mainloop()
"""