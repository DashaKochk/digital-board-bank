from tkinter import *

root = Tk()
root.title("Практическая работа №21")
root.geometry("500x400")

c = Canvas(root, width=500, height=400, bg='white')
c.pack()

c.create_oval(350, 30, 450, 130, fill='orange', outline='orange')

c.create_rectangle(180, 180, 320, 300, fill='skyblue', outline='skyblue')
c.create_polygon(160, 180, 250, 110, 340, 180, fill='skyblue', outline='skyblue')

for x in range(0, 500, 10):
    c.create_line(x, 300, x + 5, 400, fill='green', width=2)

root.mainloop()