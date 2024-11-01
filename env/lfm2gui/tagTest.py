import tkinter as tk
from tkinter import ttk

root = tk.Tk()

tree = ttk.Treeview(root)
tree.pack()

tree.insert("", 0, text="Item 1", tags=("tag1",))
tree.insert("", 1, text="Item 2", tags=("tag2",))

# Configure tag1
tree.tag_configure("tag1", foreground="red", background="yellow")

# Configure tag2
tree.tag_configure("tag2", font=("Arial", 12, "bold"))

root.mainloop()