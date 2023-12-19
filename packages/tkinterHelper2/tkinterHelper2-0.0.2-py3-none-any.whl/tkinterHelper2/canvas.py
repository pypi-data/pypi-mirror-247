"""
Виджет Canvas предоставляет возможности рисования двухмерных фигур. Стоит отметить, что Canvas есть только в пакете tkinter, а в пакете tkinter.ttk аналог отсутствует.

Некоторые основные параметры Canvas:

bg / background: фоновый цвет

bd / border: граница

borderwidth: толщина границы

cursor: курсор

height: высота виджета

width: ширина виджета

По умолчанию Canvas представляет прямоугольную область:

from tkinter import *

root = Tk()
root.title("METANIT.COM")
root.geometry("300x300")

canvas = Canvas(bg="white", width=250, height=250)
canvas.pack(anchor=CENTER, expand=1)

root.mainloop()
Canvas в Tkinter и Python
Для двухмерного рисования Canvas предоставляет ряд методов:

create_line(): рисует линию

create_rectangle(): рисует прямоугольник

create_oval(): рисует овал

create_arc(): рисует дугу

create_polygon(): рисует многоугольник

create_text(): добавляет текст

create_image(): добавляет изображение

create_window(): добавляет виджет

В качестве результата все эти методы возвращают идентифтикатор добавленного элемента. Этот идентификатор в дальнейшем может использоваться для управления элементом. Рассмотрим применение этих методов.

Создание линии
Для рисования линии применяется метод create_line(). Для вывода линии необходимо как минимум задать координаты точек, например:

1
create_line(__x0: float, __y0: float, __x1: float, __y1: float)
Параметры __x0 и __y0 представляют координаты начальной точки линии, а __x1 и __y1 - конечной.

Началом координат в Canvas считается верхней левый угол виджета - это точка с координатами (0,0). Таким образом, ось X направлена вправо, а ось Y - вниз.

Нарисуем простейшую линию:

from tkinter import *

root = Tk()
root.title("METANIT.COM")
root.geometry("300x300")

canvas = Canvas(bg="white", width=250, height=250)
canvas.pack(anchor=CENTER, expand=1)

canvas.create_line(10, 10, 200, 50)

root.mainloop()
Создание линии на Canvas в Tkinter и Python
Кроме того у данного метода можно выделить ряд дополнительных параметров:

arrow: помещает стрелку в начале линии (значение first), в конце (last) или на обоих концах (both)

arrowshape: позволяет изменить форму стрелки

capstyle: если линия не имеет стрелки, то устанавливает, как завершается линия. Принимает значения: butt (по умолчанию), projecting и round

joinstyle: управляет соединением сегметов линии. Принимает значения: round (по умолчанию), bevel и miter

smooth: если значение "true" или "bezier", сглаживает сегменты линии

splinesteps: управляет сглаживанием изогнутых линий

Параметры отрисовки
Методы отрисовки имеют ряд параметров, которые позволяют настроить стилизацию фигур. Некоторые из этих параметров:

fill: цвет заполнения фигуры

width: ширина линий

outline: для заполненных фигур цвет контура

dash: устанавливает пунктирную линию

stipple: устанавливает шаблон для заполнения фигуры (например, gray75, gray50, gray25, gray12)

activefill: цвет заполнения фигуры при наведении курсора

activewidth: ширина линий при наведении курсора

activestipple: шаблон заполнения фигуры при наведении курсора

Применим некоторые параметры:

from tkinter import *

root = Tk()
root.title("METANIT.COM")
root.geometry("300x250")

canvas = Canvas(bg="white", width=250, height=200)
canvas.pack(anchor=CENTER, expand=1)

canvas.create_line(10, 10, 200, 50, activefill="red", fill="blue", dash=2)
canvas.create_line(10, 50, 200, 90, activefill="red", fill="blue", dash=2)

root.mainloop()
В данном случае нарисованы две параллельные линии пунктиром синим цветом. При наведении на них указателя мыши, они окрашиваются в красный цвет.

окраска фигур и линий в tkinter и python
Создание прямоугольника
Для отрисовки прямоугольника применяется метод create_rectangle(), которому обязательно передаются координаты верхнего левого и правого нижнего угла:

1
create_rectangle(__x0: float, __y0: float, __x1: float, __y1: float)
Применение метода:

from tkinter import *

root = Tk()
root.title("METANIT.COM")
root.geometry("300x250")

canvas = Canvas(bg="white", width=250, height=200)
canvas.pack(anchor=CENTER, expand=1)

canvas.create_rectangle(10, 20, 200, 60, fill="#80CBC4", outline="#004D40")

root.mainloop()
отрисовка прямоугольника на Canvas в tkinter и python
Отрисовка овала
Для отрисовки овала применяется метод create_oval(). В качестве обязательных параметров он принимает координаты прямоугольника, в который будет вписан овал. :

1
create_oval(__x0: float, __y0: float, __x1: float, __y1: float)
Пример использования метода:

from tkinter import *

root = Tk()
root.title("METANIT.COM")
root.geometry("300x250")

canvas = Canvas(bg="white", width=250, height=200)
canvas.pack(anchor=CENTER, expand=1)

canvas.create_oval(10, 10, 200, 50, fill="#80CBC4", outline="#004D40")
canvas.create_rectangle(10, 10, 200, 50)

root.mainloop()
Для наглядности здесь также отрисован прямоугольник, чтобы было видно как вписывается овал:

отрисовка овала на Canvas в tkinter и python
Отрисовка многоугольника
Для создания многоугольника применяется метод create_polygon(). Он принимает в качестве обязательных параметров набор координатов точек:

from tkinter import *

root = Tk()
root.title("METANIT.COM")
root.geometry("300x250")

canvas = Canvas(bg="white", width=250, height=200)
canvas.pack(anchor=CENTER, expand=1)

canvas.create_polygon(10, 30, 200, 200, 200, 30, fill="#80CBC4", outline="#004D40")

root.mainloop()
В данном случае передаются координаты трех точек, которые в итоге станут вершинами треугольника

отрисовка многоугольника на Canvas в tkinter и python
Для упрощения также можно передавать набор кортежей, где каждый кортеж представляет отдельную точку:

points = (
    (10, 30),
    (200, 200),
    (200, 30),
)
canvas.create_polygon(*points, fill="#80CBC4", outline="#004D40")
Отрисовка дуги
Для отрисовки дуги применяется метод create_arc(), который принимает набор точек:

from tkinter import *

root = Tk()
root.title("METANIT.COM")
root.geometry("300x250")

canvas = Canvas(bg="white", width=250, height=200)
canvas.pack(anchor=CENTER, expand=1)

canvas.create_arc((10, 10), (200, 200), fill="#80CBC4", outline="#004D40")

root.mainloop()
отрисовка дуги на Canvas в tkinter и python
Отображение текста
Для вывода текста применяется метод create_text(). Ключевыми его параметрами являются координаты точки вывода текста, а также параметр text - сам выводимый текст:

1

При выводе текста стоит учитывать, что по умолчанию указанные координаты представляют центральную точку вывода текста. Но это поведение можно изменить с помощью опции anchor.

from tkinter import *

root = Tk()
root.title("METANIT.COM")
root.geometry("300x250")

canvas = Canvas(bg="white", width=250, height=200)
canvas.pack(anchor=CENTER, expand=1)

canvas.create_text(50, 50, text="Hello METANIT.COM", fill="#004D40")

canvas.create_text(50, 100, anchor=NW, text="Hello METANIT.COM", fill="#004D40")

root.mainloop()
Здесь два раза выводится один и тот же текст. И в обоих случаях совпадает X-координата. Но во втором случае установлен параметр anchor: его значение "NW" указывает, что координаты будут представлять верхний левый угол прямогольной области, в которой выводится текст

вывод текста на Canvas в tkinter и python
С помощью параметра font можно задать шрифт, в том числе его высоту:

1
canvas.create_text(10, 10, font="Arial 14", anchor=NW, text="Hello METANIT.COM", fill="#004D40")
Вывод изображения
Для вывода изображения применяется метод create_image(), который в качестве обязательно параметра принимает координаты изображения. Для установки самого изображения в метод через параметр image передается ссылка на изображение:

from tkinter import *

root = Tk()
root.title("METANIT.COM")
root.geometry("300x250")

canvas = Canvas(bg="white", width=250, height=200)
canvas.pack(anchor=CENTER, expand=1)

python_image = PhotoImage(file="python.png")

canvas.create_image(10, 10, anchor=NW, image=python_image)

root.mainloop()
В данном случае координаты представлены точкой с x=10 и y=10, а изображение представляет объект PhotoImage (здесь предполагается, что в одной папке с файлом программы находится файл "python.png"). Но как и в случае с выводом текста, следует учитывать, что по умолчанию координаты представляют центр изображения. Чтобы настроить положение изображения относительно координат, применяется параметр anchor. Так, в данном случае значение "NW" означает, что координата представляет верхний левый угол изображения.

вывод изображения на Canvas в tkinter и python
Добавление виджетов
Одной из замечательных особенностей Canvas является то, что он позволяет добавлять другие виджеты и таким образом создавать сложные по композиции интерфейсы. Для этого применяется метод create_window().

1
2
create_window(__x: float, __y: float, *, anchor: _Anchor = ..., height: _ScreenUnits = ..., state: Literal['normal', 'active', 'disabled'] = ..., tags: str | list[str] | tuple[str, ...] = ..., width: _ScreenUnits = ..., window: Widget = ...) -> _CanvasItemId
create_window(__coords: tuple[float, float] | list[int] | list[float], *, anchor: _Anchor = ..., height: _ScreenUnits = ..., state: Literal['normal', 'active', 'disabled'] = ..., tags: str | list[str] | tuple[str, ...] = ..., width: _ScreenUnits = ..., window: Widget = ...) -> _CanvasItemId
Параметры

_x и _y или __coords: координаты точки размещения виджета. По умолчанию представляет центр виджета

_anchor: устанавливает положение виджета относительно координат

height: высота виджета

width: ширина виджета

state: состояние виджета

tags: набор тегов, связанных с виджетом

В качестве результата этот метод возвращает идентификатор добавленного метода.

Например, добавим кнопку:

from tkinter import *
from tkinter import ttk

root = Tk()
root.title("METANIT.COM")
root.geometry("300x250")

canvas = Canvas(bg="white", width=250, height=200)
canvas.pack(anchor=CENTER, expand=1)

btn = ttk.Button(text="Click")
canvas.create_window(10, 20, anchor=NW, window=btn, width=100, height=50)

root.mainloop()
В данном случае верхний левый угол кнопки будет иметь координаты (x=10, y=20), а сама кнопка имеет ширину 100 и высоту 50 единиц. Если ширина и высота явным образом не указаны, то они имеют значения по умолчанию.

Добавление виджетов в Canvas в Tkinter и Python
Создание прокрутки
Для создания прокрутки виджет Canvas предоставляет параметр , который позволяет установить прокручиваемую область:

from tkinter import *
from tkinter import ttk

root = Tk()
root.title("METANIT.COM")
root.geometry("250x200")

h = ttk.Scrollbar(orient=HORIZONTAL)
v = ttk.Scrollbar(orient=VERTICAL)
canvas = Canvas(scrollregion=(0, 0, 1000, 1000), bg="white", yscrollcommand=v.set, xscrollcommand=h.set)
h["command"] = canvas.xview
v["command"] = canvas.yview

canvas.grid(column=0, row=0, sticky=(N,W,E,S))
h.grid(column=0, row=1, sticky=(W,E))
v.grid(column=1, row=0, sticky=(N,S))
root.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(0, weight=1)

canvas.create_rectangle(10,10, 300, 300, fill="red")

root.mainloop()
В данном случае устанавливается прокручиваемая область 1000х1000:

1
canvas = Canvas(scrollregion=(0, 0, 1000, 1000), ....

"""