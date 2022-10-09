import time

# from tkinter import *
#
# a = int(input('Enter the first number'))
# r = int(input('Enter the first number'))
# N = int(input('Enter the first number'))
#
#
# def geometric_progression(a, r, n):
#     tk = Tk()
#     options_list = ['Get the ith value in a GP', 'Show all values in a GP']
#     face = StringVar()
#     face.set(options_list[0])
#     entry_a = Entry(tk)
#     entry_a.place(relheight=0.1, relwidth=0.4, rely=0.4)
#     tk.geometry("500x800")
#
#     options = OptionMenu(tk, face, *options_list)
#     options.pack()
#     print(face.get())
#     if face.get() == 'Get the ith value in a GP':
#         def printer():
#             return a + (n - 1) * r
#         label = Label(tk, bg='blue')
#         label.place(relheight=0.2, relwidth=1, rely=0.45)
#         label['text'] = printer()
#         button = Button(tk, text='Get', command=printer())
#         button.place(relheight=0.4, relwidth=0.2)
#     tk.mainloop()
#
#     return 1
#
#
# geometric_progression(a, r, N)
import tkinter


def printer(a, n, r, lab: tkinter.Label):
    if lab:
        lab.destroy()
    val = a + (n - 1) * r
    lab = tk.Label()
    lab['text'] = val
    lab.pack()


import tkinter as tk
from tkinter import *

window = Tk()

window.geometry('500x800')

OptionList = ['Get the ith value in a GP', 'Show all values in a GP', 'Show walk_through']


class App:

    def __init__(self, master):

        self.choice_var = tk.StringVar()
        self.choice_var.set(OptionList[0])

        opt = OptionMenu(window, self.choice_var, *OptionList, command=self.switch)
        opt.config(width=90, font=('Calbri', 12))
        opt.pack(side="top")

        self.random_label1 = tk.Label(window, text="This is the first page")
        self.random_label2 = tk.Label(window, text="This is the second page")
        self.random_label3 = tk.Label(window, text="This is the page")

        self.sum_label = Label(window, bg='blue')

        self.image = PhotoImage(file='logo1.png')
        self.frame = Frame(bg='green')
        self.frame.pack()
        self.label = Label(self.frame, image=self.image)
        self.label.pack()

        self.a = IntVar()
        self.r = IntVar()
        self.n = IntVar()
        self.entry_a = Entry(window, textvariable=self.a)
        self.entry_r = Entry(window, textvariable=self.r)
        self.entry_n = Entry(window, textvariable=self.n)

        self.entry_a.pack()
        self.entry_r.pack()
        self.entry_n.pack()
        self.button_1 = Button(window, text='Get', bg='blue')

        self.random_label1.pack()
        self.random_label2.pack()
        self.random_label3.pack()

        self.label_info1 = self.random_label1.pack_info()
        self.label_info2 = self.random_label2.pack_info()
        self.label_info3 = self.random_label3.pack_info()
        self.entry_n_info = self.entry_n.pack_info()
        self.entry_a_info = self.entry_n.pack_info()
        self.entry_r_info = self.entry_n.pack_info()
        # self.button_1_info = self.button_1.pack_info()

        self.switch()

    def switch(self, *args):
        var = str(self.choice_var.get())
        if var == "Get the ith value in a GP":
            def get_the_ith(a, n, r):
                val = a + (n - 1) * r
                self.lab = Label()
                self.sum_label['text'] = val
                self.sum_label.pack()
                frame = Frame(window, bg='green')
                frame.place(rely=0.25, relx=0.5)

            self.random_label1.pack(self.label_info1)
            self.random_label2.pack_forget()
            self.random_label3.pack_forget()
            self.entry_n.pack(self.entry_n_info)
            self.entry_r.pack(self.entry_r_info)
            self.entry_a.pack(self.entry_a_info)
            self.button_1.pack()

            self.button_1.configure(command=lambda: get_the_ith(self.a.get(), self.n.get(), self.r.get()))

        if var == "Show all values in a GP":
            self.random_label2.pack(self.label_info2)
            self.random_label1.pack_forget()
            self.random_label3.pack_forget()
            # self.lab.pack_forget()
            self.sum_label.pack_forget()
            self.entry_a.pack_forget()
            self.entry_r.pack_forget()
            self.entry_n.pack_forget()
            self.button_1.pack_forget()

            # self.button_1.configure(text= 'Get all', command=lambda: self.get_the_ith(self.a.get(), self.n.get(), self.r.get()))

        if var == "Show walk_through":
            self.random_label3.pack(self.label_info3)
            self.random_label2.pack_forget()
            self.random_label1.pack_forget()
            self.sum_label.pack_forget()
            self.entry_a.pack_forget()
            self.entry_r.pack_forget()
            self.entry_n.pack_forget()
            self.button_1.pack_forget()




myApp = App(window)
window.mainloop()
