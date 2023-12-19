"""
from tkinter import *
from tkinter import ttk

import mysql.connector
from PIL import Image, ImageTk

connection = mysql.connector.connect(
            host="192.168.13.100",
            user="user13",
            password="41225",
            database="user13")

cursor = connection.cursor()
cursor.execute("Select * from Books")
print(cursor.fetchall())


tk = Tk()
tk.title("books shop")
tk.geometry("700x700")


def add_product_at_db(name, photo,window):
    connection = mysql.connector.connect(
        host="192.168.13.100",
        user="user13",
        password="41225",
        database="user13"
    )
    print("Connection to MySQL DB successful")
    cursor = connection.cursor()
    val = (name, photo,)
    sql = ("INSERT INTO Books(name,image) VALUES (%s,%s)")
    cursor.execute(sql, val)
    connection.commit()

    cursor = connection.cursor()
    cursor.execute("Select * from Books")
    books = cursor.fetchall()
    for i in tree.get_children():
        tree.delete(i)
    for product in books:
        print(product)
        img = ImageTk.PhotoImage(Image.open("фото_товара/" + product[2]).resize((50, 50)))
        tree.insert('', 'end', image=img,
                    value=(product[0], product[1]))
        qwe.append(img)

    tree.bind("<Button-3>")
    connection.close()
    window.destroy()

def add_product_window():
    add_window = Toplevel(tk)
    add_window.geometry('500x500')

    name_label = Label(add_window, text='Наименование')
    name_label.pack()
    name_entry = Entry(add_window)
    name_entry.pack()

    photo_label = Label(add_window, text='Изображение')
    photo_label.pack()
    photo_entry = Entry(add_window)
    photo_entry.pack()

    add_button = Button(add_window, text='Добавить',
                           command=lambda: add_product_at_db(name_entry.get(),photo_entry.get(),add_window))

    add_button.pack()
    add_window.transient(tk)
    add_window.grab_set()
    add_window.focus_set()
    add_window.wait_window()


def go_to_admin():
    code = name_entry.get()
    if code == '0000':
        add_prod_button.pack(pady=10, side="left")

        menu = Menu(tk, tearoff=0)
        menu.add_command(label='delete', command=print_to_console)

        def show(event):
            menu.post(event.x_root, event.y_root)

        tree.bind("<Button-3>", show)


def call_back(stv, books, tree):
    for i in tree.get_children():
        tree.delete(i)

    for book in books:
        if str(stv.get()) in str(book[1]):
            img = ImageTk.PhotoImage(Image.open("фото_товара/" + book[2]).resize((50, 50)))
            tree.insert('', 'end', image=img,
                        value=(book[0], book[1]))
            qwe.append(img)


frame = Frame(tk)
# Обработка админа
name_entry = Entry(frame)
name_but = Button(frame, text="Войти", command=go_to_admin)
name_entry.pack(pady=10, padx=10,side="left")
name_but.pack(pady=10, padx=10,side="left")

add_prod_button = Button(frame, text='Добавить товар',command=add_product_window)
add_prod_button.pack_forget()

sv = StringVar()
sv.trace('w', lambda name, index, mode, stv=sv: call_back(sv, books, tree))
s_lab = Label(frame, text="Поиск")
s_lab.pack()
search_entry = Entry(frame,textvariable=sv)
search_entry.pack()


frame.pack()

style = ttk.Style()
style.configure('Treeview', rowheight=80)


tree = ttk.Treeview(tk, column=('A', 'B'), selectmode='none', height=800)
tree.pack(padx=10, pady=10)

columns = ("#0", "#1", "#2")

# Setup column heading
tree.heading('#0', text=' Pic')

tree.heading('#1', text=' Id')
tree.heading('#2', text=' Name')

def print_to_console():
    selected = tree.focus()
    item = tree.item(selected, 'values')
    sql = ("Delete from Books where id = %s")
    val = (item[0],)
    cursor.execute(sql,val)
    connection.commit()
    cursor.execute("select * from Books")
    print(cursor.fetchall())
    tree.delete(selected)


for col in columns:
    tree.column(col, stretch=YES, width=166)


cursor = connection.cursor()
cursor.execute("Select * from Books")
books = cursor.fetchall()
qwe = []
for product in books:
    img = ImageTk.PhotoImage(Image.open("фото_товара/"+ product[2]).resize((50, 50)))
    tree.insert('', 'end', image=img,
                value=(product[0], product[1]))
    qwe.append(img)



tk.mainloop()
"""
