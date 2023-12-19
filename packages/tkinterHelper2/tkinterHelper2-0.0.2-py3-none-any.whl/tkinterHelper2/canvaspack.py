"""
Удаление элемента
Для удаления применяется метод delete(), который в качестве параметра принимает идентификатор удаляемого элемента.

from tkinter import *
from tkinter import ttk

root = Tk()
root.title("METANIT.COM")
root.geometry("300x250")

canvas = Canvas(bg="white", width=250, height=200)
canvas.pack(anchor=CENTER, expand=1)


def remove_button():
    canvas.delete(btnId)

btn = ttk.Button(text="Click", command=remove_button)
btnId = canvas.create_window(10, 20, anchor=NW, window=btn, width=100, height=50)

root.mainloop()
Здесь по нажатию на кнопку удаляется сама кнопка. В качестве аргумента в метод delete() передается идентификатор, который мы получаем при добавлении кнопки.

Управление координатами
Для получения/изменения координат элеимента применяется метод coords():

# получение координат
coords(__tagOrId: str | _CanvasItemId, /) -> list[float]

# изменение координат
coords(__tagOrId: str | _CanvasItemId, __args: list[int] | list[float] | tuple[float, ...], /) -> None
coords(__tagOrId: str | _CanvasItemId, __x1: float, __y1: float, *args: float) -> None
Первая версия возвращает координаты в виде списка значений для элемента с определенным идентификатором.

Вторая и третья версии изменяют позицию, получая в качестве второго/третьего параметра(ов) новые координаты.

Например, динамически изменим координаты:

from tkinter import *
from tkinter import ttk

root = Tk()
root.title("METANIT.COM")
root.geometry("300x250")

y = 0
direction = -10
btn_height = 40
canvas_height = 200

canvas = Canvas(bg="white", width=250, height=canvas_height)
canvas.pack(anchor=CENTER, expand=1)

def cliked_button():
    global y, direction
    if y >= canvas_height - btn_height or y <=0: direction = direction * -1
    y = y + direction
    canvas.coords(btnId, 10, y)

btn = ttk.Button(text="Click", command=cliked_button)
btnId = canvas.create_window(10, y, anchor=NW, window=btn, width=100, height=btn_height)

root.mainloop()
Здесь по нажатию на кнопку к координате y добавляется +-10. Когда кнопка достигает границ Canvas, то изменяем знак приращения на противоположный, и таким образом, кнопка изменяет направление движения.

Изменение параметров элемента
Для изменения параметров элемента на Canvas применяется метод itemconfigure(). В качестве обязательного параметра он принимает идентифкатор изменяемого элемента, а второй параметр - набор устанавливаемых параметров:

1
itemconfigure: (tagOrId: str | _CanvasItemId, cnf: dict[str, Any] | None = ..., **kw: Any)
Например, изменим цвет линии:

from tkinter import *
from tkinter import ttk

root = Tk()
root.title("METANIT.COM")
root.geometry("300x250")

red = "red"
blue= "blue"

selected_color = StringVar(value=red)

canvas = Canvas(bg="white", width=250, height=150)
canvas.pack(anchor=CENTER, expand=1)

def select():
    canvas.itemconfigure(line, fill=selected_color.get())

red_btn = ttk.Radiobutton(text=red, value=red, variable=selected_color, command=select, padding=6)
red_btn.pack(anchor=NW)
blue_btn = ttk.Radiobutton(text=blue, value=blue, variable=selected_color, command=select, padding=6)
blue_btn.pack(anchor=NW)

line = canvas.create_line(10, 10, 200, 100, fill=selected_color.get())

root.mainloop()
"""