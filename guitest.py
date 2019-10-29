import tkinter as tk

root = tk.Tk()
canvas = tk.Canvas(root, height=500, width=640).pack()
frame = tk.Frame(root, bg='#80c1ff').place(relx=0.05, rely=0.05, relwidth=0.9, relheight=0.9)

label = tk.Label(frame, text='Click this').place(relx=0.05, rely=0.05, relwidth=0.2, relheight=0.2)
button = tk.Button(frame, text='Test', bg='black', fg='white').place(relx=0.05, rely=0.05, relwidth=0.9, relheight=0.9)


entry = tk.Entry(frame).place(relx=0.3, rely=0.3, relwidth=0.1, relheight=0.1)

root.mainloop()
