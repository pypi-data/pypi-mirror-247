"""
Окна сообщений
Tkinter имеет ряд встроенных окон для разных ситуаций, в частности, окна сообщений, функционал которых заключен в модуле tkinter.messagebox. Для отображения сообщений этот модуль предоставляет следующие функции:

showinfo(): предназначена для отображения некоторой информации

showerror(): предназначена для отображения ошибок

showwarrning(): предназначена для отображения предупреждений

Все эти функции принимают три параметра:

showinfo(title, message, **options)
showerror(title, message, **options)
showwarrning(title, message, **options)
title: заголовок окна

message: отображаемое сообщение

options: настройки окна

В реальности различие между этими типами сообщений заключается лишь в изображении, которое отображается рядом с текстом сообщения:

from tkinter import *
from tkinter import ttk
from tkinter.messagebox import showerror, showwarning, showinfo

root = Tk()
root.title("METANIT.COM")
root.geometry("250x200")

def open_info():
    showinfo(title="Информация", message="Информационное сообщение")

def open_warning():
    showwarning(title="Предупреждение", message="Сообщение о предупреждении")

def open_error():
    showerror(title="Ошибка", message="Сообщение об ошибке")

info_button = ttk.Button(text="Информация", command=open_info)
info_button.pack(anchor="center", expand=1)

warning_button = ttk.Button(text="Предупреждение", command=open_warning)
warning_button.pack(anchor="center", expand=1)

error_button = ttk.Button(text="Ошибка", command=open_error)
error_button.pack(anchor="center", expand=1)

root.mainloop()
Здесь по нажатию на каждую из трех кнопок отображается соответствующее сообщение:

Окна с сообщениями messagebox в Tkinter и Python
Окна подтверждения операции
Модуль tkinter.messagebox также предоставляет ряд функций для подтверждения операции, где пользователю предлагается нажать на одну из двух кнопок:

askyesno()

askokcancel()

askretrycancel()

Все эти функции принимают те же три параметра title, message и options. Отличие между ними только в том, что кнопки имеют разный текст. В случае нажатия на кнопку подтверждения, функция возвращает значение True, иначе возвращается False

from tkinter import *
from tkinter import ttk
from tkinter.messagebox import showinfo, askyesno

root = Tk()
root.title("METANIT.COM")
root.geometry("250x200")

def click():
    result = askyesno(title="Подтвержение операции", message="Подтвердить операцию?")
    if result: showinfo("Результат", "Операция подтверждена")
    else: showinfo("Результат", "Операция отменена")

ttk.Button(text="Click", command=click).pack(anchor="center", expand=1)

root.mainloop()
В данном случае по нажатию на кнопку вызывается функция askyesno(), которая отображает диалоговое окно с двумя кнопками "Да" и "Нет". В зависимости от того, на какую кнопку нажмет пользователь, функция возвратит True или False. Получив результат функции, мы можем проверить его и выполнить те или иные действия.

Диалоговые окна в Tkinter и Python
Особняком стоит функция askquestion - она также отображает две кнопки для подтверждения или отмены действия (кнопки "Yes"(Да) и "No"(Нет)), но в зависимости от нажатой кнопки возвращает строку: "yes" или "no".

Также отдельно стоит функция askyesnocancel() - она отображает три кнопки: Yes (возвращает True), No (возвращает False) и Cancel (возвращает None):

from tkinter import *
from tkinter import ttk
from tkinter.messagebox import showinfo, askyesnocancel

root = Tk()
root.title("METANIT.COM")
root.geometry("250x200")

def click():
    result =  askyesnocancel(title="Подтвержение операции", message="Подтвердить операцию?")
    if result==None: showinfo("Результат", "Операция приостановлена")
    elif result: showinfo("Результат", "Операция подтверждена")
    else : showinfo("Результат", "Операция отменена")

ttk.Button(text="Click", command=click).pack(anchor="center", expand=1)

root.mainloop()
В этом случае диалоговое окно предоставит выбор из трех альтернатив

Диалоговые окна подтверждения операции в Tkinter и Python
Настройка окон
Дополнительно все вышерассмотренные функции принимают ряд параметров, которые могут применяться для настройки окон. Некоторые из них:

detail: дополнительный текст, который отображается под основным сообщением

icon: иконка, которая отображается рядом с сообщением. Должна представлять одно из втроенных изображений: info, error, question или warning

default: кнопка по умолчанию. Должна представлять одно из встроенных значений: abort, retry, ignore, ok, cancel, no, yes

from tkinter import *
from tkinter import ttk
from tkinter.messagebox import OK, INFO, showinfo

root = Tk()
root.title("METANIT.COM")
root.geometry("250x200")

def click():
    showinfo(title="METANIT.COM", message="Добро пожаловать на сайт METANIT.COM",
            detail="Hello World!", icon=INFO, default=OK)

ttk.Button(text="Click", command=click).pack(anchor="center", expand=1)

root.mainloop()
"""