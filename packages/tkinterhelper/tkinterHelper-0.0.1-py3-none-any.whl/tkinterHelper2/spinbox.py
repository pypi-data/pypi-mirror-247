"""
Виджет Spinbox позволяет выбрать значение (чаще число) из некоторого списка.

Основные параметры Spinbox:

values: набор значений виджета в виде списка или кортежа

from_: минимальное значение (тип float)

to: максимальное значение (тип float)

increment: приращение значения (тип float)

textvariable: определяет переменную StringVar, которая хранит текущее значение виджета

command: указывает на функцию, которая вызывается при изменении значения виджета

wrap: при значении True создает зацикленный список, при котором после минимального значения идет максимальное.

background: фоновый цвет

foreground: цвет текста

font: шрифт виджета

justify: выравнивание текста, принимает значения "left" (по левому краю), "right" (по правому краю) и "center" (по центру)

width: ширина виджета

state: состояние виджета

Простейший Spinbox:

from tkinter import *
from tkinter import ttk

root = Tk()
root.title("METANIT.COM")
root.geometry("250x200")

spinbox = ttk.Spinbox(from_=1.0, to=100.0)
spinbox.pack(anchor=NW)

root.mainloop()
"""