"1"
"""
from tkinter import *
from tkinter.ttk import *
from PIL import ImageTk, Image
import mysql.connector


cursor = con.cursor()

tk = Tk()
tk.title('prod')
style = Style()
style.configure('Treeview', rowheight=80)
frame = Frame(tk)
frame.pack(anchor='w')
frame_price = Frame(frame)
frame_price.pack(side=LEFT, padx=10)
label = Label(frame_price, text='От')
label.pack(anchor='w')
var = IntVar(tk)
listbox = Combobox(frame_price, textvariable=var, values=(500, 1000,2000))
listbox.pack(anchor='w')


def get_selected(eventObject):
    print(listbox.get())
    z = int(listbox.get())
    tree.delete(*tree.get_children())
    tree.tag_configure('pass', background='purple')
    cursor.execute()
    products_new = cursor.fetchall()
    for y in range(len(products_new)):
        tag = 'pass' if int(products_new[y][1]) > z else 'fail'
        img_new = ImageTk.PhotoImage(Image.open('Stack.jpg').resize((50, 50)))
        tree.insert('', 'end', image=img_new, values=(products_new[y][0], products_new[y][1]), tags=tag)
        garbage.append(img_new)


listbox.bind('<<ComboboxSelected>>', get_selected)


frame_filter = Frame(frame)
frame_filter.pack(side=LEFT, padx=10)
label1 = Label(frame_filter, text='Фильтр')
label1.pack(anchor='w')
var1 = StringVar(tk)
listbox1 = Combobox(frame_filter, textvariable=var1, width=40, values=('Без фильтра', 'По убыванию цены', 'По возрастанию цены'))
listbox1.pack(anchor='w')


def get_filter(eventObject):
    z = listbox1.get()
    tree.delete(*tree.get_children())
    cursor.execute()
    products_new = cursor.fetchall()
    if z == 'Без фильтра':
        for y in range(len(products_new)):
            img_new = ImageTk.PhotoImage(Image.open('Stack.jpg').resize((50, 50)))
            tree.insert('', 'end', image=img_new, values=(products_new[y][0], products_new[y][1]))
            garbage.append(img_new)
    elif z == 'По убыванию цены':
        sorted_prod = sorted(products_new, key=lambda q: int(q[1]))
        for y in range(len(sorted_prod)):
            img_new = ImageTk.PhotoImage(Image.open('Stack.jpg').resize((50, 50)))
            tree.insert('', 'end', image=img_new, values=(sorted_prod[y][0], sorted_prod[y][1]))
            garbage.append(img_new)
    elif z == 'По возрастанию цены':
        sorted_prod = sorted(products_new, key=lambda q: int(q[1]), reverse=True)
        for y in range(len(sorted_prod)):
            img_new = ImageTk.PhotoImage(Image.open('Stack.jpg').resize((50, 50)))
            tree.insert('', 'end', image=img_new, values=(sorted_prod[y][0], sorted_prod[y][1]))
            garbage.append(img_new)



listbox1.bind('<<ComboboxSelected>>', get_filter)

tree = Treeview(tk, columns=('A', 'B'), selectmode='browse')
tree.pack()

tree.column('A', anchor=CENTER)
tree.column('B', anchor=CENTER)
tree.heading('#0', text='picture')
tree.heading('#1', text='name')
tree.heading('#2', text='cost')

columns = ('#0', '#1', '#2')

cursor.execute()
products = cursor.fetchall()
garbage = []
for x in range(len(products)):
    img = ImageTk.PhotoImage(Image.open('Stack.jpg').resize((50, 50)))
    tree.insert('', 'end', image=img, values=(products[x][0], products[x][1]))
    garbage.append(img)
tk.mainloop()

"""

"2"
"""
import tkinter as tk
from tkinter import ttk

import mysql.connector
from PIL import ImageTk, Image


cur = connector.cursor()
cur.execute("SELECT * FROM Books")
books = cur.fetchall()

#--------------------Sort----------------------------
def sort_down():
    cur.execute("SELECT * FROM Books ORDER BY id DESC")
    books = cur.fetchall()
    for i in tree.get_children():
        tree.delete(i)
    for book in books:
        img = ImageTk.PhotoImage(Image.open('фото_товара/' + book[2]).resize((50, 50)))
        tree.insert('', tk.END, image=img, value=(book[0], book[1]))
        img_arr.append(img)

def sort_up():
    cur.execute("SELECT * FROM Books")
    books = cur.fetchall()
    for i in tree.get_children():
        tree.delete(i)
    for book in books:
        img = ImageTk.PhotoImage(Image.open('фото_товара/' + book[2]).resize((50, 50)))
        tree.insert('', tk.END, image=img, value=(book[0], book[1]))
        img_arr.append(img)

#-----------------Select from combobox----------------------------
def selected(event):
    selection = combobox.get()
    print(selection)
    if selection == '1..3':
        cur.execute("SELECT * FROM Books WHERE id > 0 and id<=3")
        books = cur.fetchall()
        for i in tree.get_children():
            tree.delete(i)
        for book in books:
            img = ImageTk.PhotoImage(Image.open('фото_товара/' + book[2]).resize((50, 50)))
            tree.insert('', tk.END, image=img, value=(book[0], book[1]))
            img_arr.append(img)
    elif selection == '4..6':
        cur.execute("SELECT * FROM Books WHERE id > 3 and id<=6")
        books = cur.fetchall()
        for i in tree.get_children():
            tree.delete(i)
        for book in books:
            img = ImageTk.PhotoImage(Image.open('фото_товара/' + book[2]).resize((50, 50)))
            tree.insert('', tk.END, image=img, value=(book[0], book[1]))
            img_arr.append(img)
    else:
        cur.execute("SELECT * FROM Books WHERE id > 6 and id<=10")
        books = cur.fetchall()
        for i in tree.get_children():
            tree.delete(i)
        for book in books:
            img = ImageTk.PhotoImage(Image.open('фото_товара/' + book[2]).resize((50, 50)))
            tree.insert('', tk.END, image=img, value=(book[0], book[1]))
            img_arr.append(img)

window = tk.Tk()
window.geometry('800x500')
window.title('demo!!!')

frame = tk.Frame(window)
sort_lab = tk.Label(frame, text='sort')
sort_lab.pack()

sort_but = tk.Button(frame, text='sort_down', command=sort_down)
sort_but.pack()

sort1_but = tk.Button(frame, text='sort_up', command=sort_up)
sort1_but.pack()


filtr_lab = tk.Label(frame, text='filtr')
filtr_lab.pack()

fil = ["1..3", "4..6", "7..10"]
combobox = ttk.Combobox(frame,values=fil)
combobox.pack()
combobox.bind('<<ComboboxSelected>>',selected)

frame.pack()

style = ttk.Style()
style.configure('Treeview', rowheight=80)

tree = ttk.Treeview(window, column=('A', 'B'), selectmode='none', height=800)
tree.pack(pady=10, padx=10)

columns = ('#0', '#1', '#2')
tree.heading('#0', text='Photo')
tree.heading('#1', text='Id')
tree.heading('#2', text='Name')
#-----------------Color---------------------
tree.tag_configure('red', background='red')
tree.tag_configure('green', background='green')
img_arr = []
tag = ''
for book in books:
    if book[0] % 2 ==0:
        tag = 'green'
    else:
        tag = 'red'
    img = ImageTk.PhotoImage(Image.open('фото_товара/' + book[2]).resize((50, 50)))
    tree.insert('', tk.END, image=img, value=(book[0], book[1]),tags=(tag))
    img_arr.append(img)

window.mainloop()

"""