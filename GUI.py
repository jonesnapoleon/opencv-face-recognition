import tkinter as tk
from tkinter import filedialog

r = tk.Tk()
r.title('Face Matching')

r.resizable(width = "false", height = "false")

r.minsize(width=300, height=50)
r.maxsize(width=300, height=50)
button = tk.Button(r, text = 'Close', width=25, command=r.destroy)
button.pack()
r.mainloop()