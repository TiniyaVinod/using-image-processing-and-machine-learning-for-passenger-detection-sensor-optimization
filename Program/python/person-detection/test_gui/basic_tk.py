import tkinter as tk

window = tk.Tk()


greetings = tk.Label(
    text="Hello World", foreground="black", background="red", width=100, height=5
)

button = tk.Button(
    text="Click Me", foreground="black", background="red", width=100, height=5
)

entry = tk.Entry(foreground="black", background="red", width=100)

greetings.pack()
button.pack()
entry.pack()

window.mainloop()
