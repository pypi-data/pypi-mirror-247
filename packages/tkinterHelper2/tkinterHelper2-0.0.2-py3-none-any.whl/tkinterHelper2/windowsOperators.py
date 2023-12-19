"""
По умолчанию приложение Tkinter имеет одно главное окно, которое представляет класс tkinter.Tk. Запуск приложение приводит к запуску главного окно, в рамках которого помещаются все виджеты. Закрытие главного окна приводит к завершению работы приложения. Однако в рамках главного окна также можно запускать вторичные, неглавные окна. Например, октроем новое окно по нажатию на кнопку:

from tkinter import *
from tkinter import ttk

root = Tk()
root.title("METANIT.COM")
root.geometry("250x200")

def click():
    window = Tk()
    window.title("Новое окно")
    window.geometry("250x200")

button = ttk.Button(text="Создать окно", command=click)
button.pack(anchor=CENTER, expand=1)

root.mainloop()
Здесь по нажатию на кнопку создается новый объект window, у него устанавливается заголовок и размеры.

Создание окон в Tkinter и Python
Стоит отметить, что приложение завершит работу, когда будут закрыты все его окна.

Как и главное окно, вторичные окна могут иметь виджеты. Например, определим на новом окне метку:

from tkinter import *
from tkinter import ttk

root = Tk()
root.title("METANIT.COM")
root.geometry("250x200")

def click():
    window = Tk()
    window.title("Новое окно")
    window.geometry("250x200")
    label=ttk.Label(window, text="Принципиально новое окно")
    label.pack(anchor=CENTER, expand=1)

button = ttk.Button(text="Создать окно", command=click)
button.pack(anchor=CENTER, expand=1)

root.mainloop()
Единственное не надо забывать у добавляемых виджетов устанавливать окно в качестве родительского контейнера

Создание окон Tk в Tkinter и Python
Удаление окна
Для удаления окна применяется меnод destroy()

from tkinter import *
from tkinter import ttk

root = Tk()
root.title("METANIT.COM")
root.geometry("250x200")

def click():
    window = Tk()
    window.title("Новое окно")
    window.geometry("250x200")
    close_button = ttk.Button(window, text="Закрыть окно", command=lambda: window.destroy())
    close_button.pack(anchor="center", expand=1)

open_button = ttk.Button(text="Создать окно", command=click)
open_button.pack(anchor="center", expand=1)

root.mainloop()
В данном случае в новом окне по нажатию на кнопку close_button срабатывает метод window.destroy(), который закрывает окно и по сути аналогичен нажатию на крестик в верхнем правом углу окна.

Определение окна в объектно-ориентированном стиле
В примере выше новое окно, его параметры и вложенные виджеты определялись внутри функции, однако это приводит к разбуханию кода функции. И гораздо проще вынести определение окна в отдельный класс:

from tkinter import *
from tkinter import ttk

class Window(Tk):
    def __init__(self):
        super().__init__()

        # конфигурация окна
        self.title("Новое окно")
        self.geometry("250x200")

        # определение кнопки
        self.button = ttk.Button(self, text="закрыть")
        self.button["command"] = self.button_clicked
        self.button.pack(anchor="center", expand=1)

    def button_clicked(self):
        self.destroy()

root = Tk()
root.title("METANIT.COM")
root.geometry("250x200")

def click():
    window = Window()

open_button = ttk.Button(text="Создать окно", command=click)
open_button.pack(anchor="center", expand=1)

root.mainloop()
Здесь определение окна вынесено в отдельный класс Window, который наследуется от класса tkinter.Tk. Благодаря этому мы можем вынести весь код определения окна в отдельную структурную единицу - класс, что позволит упростить управление кодом.

Окно поверх других окон
Для создания диалогового окна, которое располагается поверх главного окна, применяется класс Toplevel:

from tkinter import *
from tkinter import ttk

root = Tk()
root.title("METANIT.COM")
root.geometry("250x200")

def dismiss(window):
    window.grab_release()
    window.destroy()

def click():
    window = Toplevel()
    window.title("Новое окно")
    window.geometry("250x200")
    window.protocol("WM_DELETE_WINDOW", lambda: dismiss(window)) # перехватываем нажатие на крестик
    close_button = ttk.Button(window, text="Закрыть окно", command=lambda: dismiss(window))
    close_button.pack(anchor="center", expand=1)
    window.grab_set()       # захватываем пользовательский ввод

open_button = ttk.Button(text="Создать окно", command=click)
open_button.pack(anchor="center", expand=1)

root.mainloop()
Toplevel по сути то же самое окно Tk, которое располагается поверх других окон. В примере выше оно также имеет кнопку. Но кроме того, чтобы пользователь не мог перейти обратно к главному окну пока не закроет это диалоговое окно, применяется ряд методов. Прежде всего захватываем весь пользовательский ввод с помощью метода grab_set():

1
window.grab_set()
В функции dismiss(), которая закрывает окно, освобождаем ввод с помощью метода grab_release()
"""