# main.py
import tkinter as tk
from ui import UIApp  # correct class name from ui.py

def main():
    root = tk.Tk()
    app = UIApp(root)  # instantiate UIApp
    root.mainloop()

if __name__ == "__main__":
    main()
