"""
Привязка виджетов к переменным
Последнее обновление: 23.09.2022

Одной из примечательных особенностей Tkinter является то, что он позволяет привязать к ряду виджетов переменные определенных типов. При изменении значения виджета автоматически будет изменяться и значение привязанной переменной. Для привязки может использоваться переменная следующих типов:

StringVar

IntVar

BooleanVar

DoubleVar

Простейший пример:
from tkinter import *
from tkinter import ttk

root = Tk()
root.title("METANIT.COM")
root.geometry("250x150")

message = StringVar()

label = ttk.Label(textvariable=message)
label.pack(anchor=NW, padx=6, pady=6)

entry = ttk.Entry(textvariable=message)
entry.pack(anchor=NW, padx=6, pady=6)

button = ttk.Button(textvariable=message)
button.pack(side=LEFT, anchor=N, padx=6, pady=6)

root.mainloop()
В данном случае определяется переменная message, которая представляет класс StringVar, то есть такая переменная, которая хранит некоторую строку.
"""