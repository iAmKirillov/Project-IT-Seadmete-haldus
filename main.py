import tkinter as tk
from tkinter import messagebox, ttk

from Classes.Device import Device
from Classes.DeviceManager import DeviceManager
from GUI.GUI import DeviceApp
from Storage.CSVstorage import CSVStorage
from Storage.JSONstorage import JSONStorage


if __name__ == "__main__":
    root = tk.Tk()
    app = DeviceApp(root)
    root.mainloop()