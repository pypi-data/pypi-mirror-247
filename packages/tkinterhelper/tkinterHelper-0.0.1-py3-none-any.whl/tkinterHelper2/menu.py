"""
Для создания иерархического меню в tkinter применяется виджет Menu. Основные параметры Menu:

activebackground: цвет активного пункта меню

activeborderwidth: толщина границы активного пункта меню

activeforeground: цвет текста активного пункта меню

background / bg: фоновый цвет

bd: толщина границы

cursor: курсор указателя мыши при наведении на меню

disabledforeground: цвет, когда меню находится в состоянии DISABLED

font: шрифт текста

foreground / fg: цвет текста

tearoff: меню может быть отсоединено от графического окна. В частности, при создании подменю а скриншоте можно увидеть прерывающуюся линию в верху подменю, за которую его можно отсоединить. Однако при значении tearoff=0 подменю не сможет быть отсоединено.

Меню может содержать много элементов, причем эти элементы сами могут представлять меню и содержать другие элементы. В зависимости от того, какой тип элементов мы хотим добавить в меню, будет отличаться метод, используемый для их добавления. В частности, нам доступны следующие методы:

add_command(options): добавляет элемент меню через параметр options

add_cascade(options): добавляет элемент меню, который в свою очередь может представлять подменю

add_separator(): добавляет линию-разграничитель

add_radiobutton(options): добавляет в меню переключатель

add_checkbutton(options): добавляет в меню флажок

Создадим простейшее меню:

from tkinter import *

root = Tk()
root.title("METANIT.COM")
root.geometry("250x150")

main_menu = Menu()
main_menu.add_cascade(label="File")
main_menu.add_cascade(label="Edit")
main_menu.add_cascade(label="View")

root.config(menu=main_menu)
root.mainloop()
Для добавления пунктов меню у объекта Menu вызывается метод add_cascade(). В этот метод передаются параметры пункта меню, в данном случае они представлены текстовой меткой, устанавливаемой через параметр label.

Но просто создать меню - еще недостаточно. Его надо установить для текущего окна с помощью параметра menu в методе config(). В итоге графическое окно будет иметь следующее меню:

Меню в tkinter и Python
Теперь добавим подменю:

from tkinter import *

root = Tk()
root.title("METANIT.COM")
root.geometry("250x150")

main_menu = Menu()

file_menu = Menu()
file_menu.add_command(label="New")
file_menu.add_command(label="Save")
file_menu.add_command(label="Open")
file_menu.add_separator()
file_menu.add_command(label="Exit")

main_menu.add_cascade(label="File", menu=file_menu)
main_menu.add_cascade(label="Edit")
main_menu.add_cascade(label="View")

root.config(menu=main_menu)

root.mainloop()
Здесь определяется подменю file_menu, которое добавляется в первый пункт основного меню благодаря установке опции menu=file_menu:

1
main_menu.add_cascade(label="File", menu=file_menu)
Подменю и сепаратор в tkinter в Python
Но обратите внимание на пунктирную линию в подменю, которая совершенно не нужна и непонятно откуда появляется. Чтобы избавиться от этой линии, надо для нужного пункта меню установить параметр tearoff=0:

1
file_menu = Menu(tearoff=0)
Однако так как подпунктов меню может быть много, чтобы для кажлого не прописывать этот параметр, то проще отключить все это глобально с помощью следующей строки кода

1
root.option_add("*tearOff", FALSE)
Полный код:

from tkinter import *

root = Tk()
root.title("METANIT.COM")
root.geometry("250x150")

root.option_add("*tearOff", FALSE)

main_menu = Menu()

file_menu = Menu()
file_menu.add_command(label="New")
file_menu.add_command(label="Save")
file_menu.add_command(label="Open")
file_menu.add_separator()
file_menu.add_command(label="Exit")

main_menu.add_cascade(label="File", menu=file_menu)
main_menu.add_cascade(label="Edit")
main_menu.add_cascade(label="View")

root.config(menu=main_menu)
root.mainloop()
Подменю и сепаратор в виджете Menu в приложении на tkinter в Python
Подобным образом можно создавать и более глубокие иерархии меню:

from tkinter import *

root = Tk()
root.title("METANIT.COM")
root.geometry("250x150")

root.option_add("*tearOff", FALSE)

main_menu = Menu()
file_menu = Menu()
settings_menu = Menu()

settings_menu.add_command(label="Save")
settings_menu.add_command(label="Open")

file_menu.add_cascade(label="Settings", menu=settings_menu)
file_menu.add_separator()
file_menu.add_command(label="Exit")

main_menu.add_cascade(label="File", menu=file_menu)

root.config(menu=main_menu)
root.mainloop()
Сложные подменю в виджете Menu в приложении на tkinter в Python
Взаимодействие с меню
Отличительной особенностью элементов меню является способность реагировать на нажатия пользователя. Для этого у каждого элемента меню можно задать параметр command, который устанавливает ссылку на функцию, выполняемую при нажатии.

from tkinter import *
from tkinter import messagebox

root = Tk()
root.title("METANIT.COM")
root.geometry("250x150")

root.option_add("*tearOff", FALSE)

def edit_click():
    messagebox.showinfo("GUI Python", "Нажата опция Edit")

main_menu = Menu()

main_menu.add_cascade(label="File")
main_menu.add_cascade(label="Edit", command=edit_click)
main_menu.add_cascade(label="View")

root.config(menu=main_menu)
root.mainloop()
"""