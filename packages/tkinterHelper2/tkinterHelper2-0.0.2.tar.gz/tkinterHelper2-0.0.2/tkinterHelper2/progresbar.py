"""
Виджет Progressbar предназначен для отображения хода выполнения какого-либо процесса. Основные параметры Progressbar:

value: текущее значение виджета (тип float)

maximum: максимальное значение (тип float)

variable: определяет переменную IntVar/DoublerVar, которая хранит текущее значение виджета

mode: определяет режим, принимает значения "determinate" (конечный) и "indeterminate" (бесконечный)

orient: определяет ориентацию виджета, принимает значения "vertical" (вертикальый) и "horizontal" (горизонтальный)

length: длина виджета

Определим вертикальный и горизонтальный Progressbar:

from tkinter import *
from tkinter import ttk

root = Tk()
root.title("METANIT.COM")
root.geometry("250x150")

# вертикальный Progressbar
ttk.Progressbar(orient="vertical", length=100, value=40).pack(pady=5)

# горизонтальный Progressbar
ttk.Progressbar(orient="horizontal", length=150, value=20).pack(pady=5)

root.mainloop()
"""