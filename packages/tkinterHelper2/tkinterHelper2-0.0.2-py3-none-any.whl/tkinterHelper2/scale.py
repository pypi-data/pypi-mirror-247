"""
Scale представляет ползунок со шкалой, на которой можно выбрать одно из числовых значений.

Среди параметров Scale следует отметить следующие:

orient: направление виджета. Может принимать значения HORIZONTAL/"horizontal" и VERTICAL/"vertical"

from_: начальное значение шкалы виджета, представляет тип float

to: конечное значение шкалы виджета, представляет тип float

length: длина виджета

command: функция, которая выполняется при изменении текущего значения

value: текущее значение шкалы виджета, представляет тип float

variable: переменная IntVar или DoubleVar, к которой привязано текущее значение виджета

Простейший Scale в горизонтальной и вертикальной ориентации:

from tkinter import *
from tkinter import ttk

root = Tk()
root.title("METANIT.COM")
root.geometry("250x250")

verticalScale = ttk.Scale(orient=VERTICAL, length=200, from_=1.0, to=100.0, value=50)
verticalScale.pack()

horizontalScale = ttk.Scale(orient=HORIZONTAL, length=200, from_=1.0, to=100.0, value=30)
horizontalScale.pack()

root.mainloop()
"""