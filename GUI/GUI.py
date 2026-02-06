import tkinter as tk
from tkinter import messagebox, ttk

from Classes.Device import Device
from Classes.DeviceManager import DeviceManager
from Storage.CSVstorage import CSVStorage
from Storage.JSONstorage import JSONStorage


class DeviceApp:
    """
    Graafiline kasutajaliides IT-seadmete haldamiseks.
    """

    def __init__(self, root):
        """
        Loob GUI akna ja elemendid.
        """
        self.root = root
        self.root.title("IT-seadmete haldus")

        self.manager = DeviceManager()

        # ---- Sisestusväljad ----
        tk.Label(root, text="Seadme nimi").grid(row=0, column=0, sticky="w")
        tk.Label(root, text="Seadme tüüp").grid(row=1, column=0, sticky="w")
        tk.Label(root, text="Seisund").grid(row=2, column=0, sticky="w")
        tk.Label(root, text="Inventarinumber").grid(row=3, column=0, sticky="w")

        self.name_entry = tk.Entry(root)
        self.type_entry = tk.Entry(root)

        # Rippmenüü seisundi jaoks
        self.status_var = tk.StringVar()
        self.status_dropdown = ttk.Combobox(
            root,
            textvariable=self.status_var,
            values=["available", "in_use", "broken"],
            state="readonly"  # Ei luba käsitsi kirjutada
        )
        self.status_dropdown.current(0)  # Vaikimisi esimene valik

        self.inventory_number_entry = tk.Entry(root)

        self.name_entry.grid(row=0, column=1)
        self.type_entry.grid(row=1, column=1)
        self.status_dropdown.grid(row=2, column=1)
        self.inventory_number_entry.grid(row=3, column=1)

        # ---- Nupud ----
        tk.Button(root, text="Lisa seade", command=self.add_device) \
            .grid(row=4, column=0, columnspan=2, pady=5)

        tk.Button(root, text="Muuda valitud", command=self.edit_device) \
            .grid(row=6, column=0, pady=5)

        tk.Button(root, text="Kustuta valitud", command=self.delete_device) \
            .grid(row=6, column=1, pady=5)

        tk.Button(root, text="Salvesta CSV", command=self.save_csv) \
            .grid(row=7, column=0)

        tk.Button(root, text="Lae CSV", command=self.load_csv) \
            .grid(row=7, column=1)

        tk.Button(root, text="Salvesta JSON", command=self.save_json) \
            .grid(row=8, column=0)

        tk.Button(root, text="Lae JSON", command=self.load_json) \
            .grid(row=8, column=1)

        # ---- Seadmete nimekiri ----
        self.listbox = tk.Listbox(root, width=60)
        self.listbox.grid(row=5, column=0, columnspan=2, pady=5)
        self.listbox.bind('<<ListboxSelect>>', self.on_select)

    def refresh_list(self):
        """
        Uuendab seadmete nimekirja.
        """
        self.listbox.delete(0, tk.END)

        for device in self.manager.devices:
            self.listbox.insert(
                tk.END,
                f"{device.name} | {device.device_type} | "
                f"{device.status} | {device.inventory_number}"
            )

    def clear_entries(self):
        """
        Tühjendab sisestusväljad.
        """
        self.name_entry.delete(0, tk.END)
        self.type_entry.delete(0, tk.END)
        self.status_var.set("available")
        self.inventory_number_entry.delete(0, tk.END)

    def on_select(self, event):
        """
        Kui kasutaja valib seadme nimekirjast, täidetakse väljad selle andmetega.
        """
        selection = self.listbox.curselection()
        if not selection:
            return

        device = self.manager.devices[selection[0]]

        self.name_entry.delete(0, tk.END)
        self.name_entry.insert(0, device.name)

        self.type_entry.delete(0, tk.END)
        self.type_entry.insert(0, device.device_type)

        self.status_var.set(device.status)

        self.inventory_number_entry.delete(0, tk.END)
        self.inventory_number_entry.insert(0, device.inventory_number)

    def add_device(self):
        """
        Lisab uue seadme.
        """
        try:
            device = Device(
                self.name_entry.get(),
                self.type_entry.get(),
                self.status_var.get(),
                self.inventory_number_entry.get()
            )
            self.manager.add_device(device)
            self.refresh_list()
            self.clear_entries()
            messagebox.showinfo("Edu", "Seade lisatud!")
        except ValueError as e:
            messagebox.showerror("Viga", f"Vigane seadme seisund: {e}")

    def edit_device(self):
        """
        Muudab valitud seadme andmeid.
        """
        selection = self.listbox.curselection()
        if not selection:
            messagebox.showwarning("Hoiatus", "Palun vali seade, mida muuta")
            return

        try:
            index = selection[0]
            device = self.manager.devices[index]

            # Uuenda seadme andmeid
            device.name = self.name_entry.get()
            device.device_type = self.type_entry.get()
            device.status = self.status_var.get()
            device.inventory_number = self.inventory_number_entry.get()

            self.refresh_list()
            self.clear_entries()
            messagebox.showinfo("Edu", "Seade uuendatud!")
        except ValueError as e:
            messagebox.showerror("Viga", f"Vigane seadme seisund: {e}")

    def delete_device(self):
        """
           Kustutab valitud seadme.
           """
        selection = self.listbox.curselection()
        if not selection:
            messagebox.showwarning("Hoiatus", "Palun vali seade, mida kustutada")
            return

        index = selection[0]
        device = self.manager.devices[index]

        if self.manager.delete_device(device.name):
            self.refresh_list()
            self.clear_entries()
            messagebox.showinfo("Edu", "Seade kustutatud!")
        else:
            messagebox.showerror("Viga", "Seadme kustutamine ebaõnnestus")

    def save_csv(self):
        """
        Salvestab seadmed CSV-faili.
        """
        csv_storage = CSVStorage("../devices.csv")
        csv_storage.save(self.manager.get_devices_as_dicts())
        messagebox.showinfo("Info", "Andmed salvestatud CSV-faili")

    def load_csv(self):
        """
        Laeb seadmed CSV-failist.
        """
        try:
            csv_storage = CSVStorage("../devices.csv")
            devices_data = csv_storage.load()
            self.manager.load_devices_from_dicts(devices_data)
            self.refresh_list()
            messagebox.showinfo("Info", "Andmed laetud CSV-failist")
        except FileNotFoundError:
            messagebox.showerror("Viga", "CSV-faili ei leitud")

    def save_json(self):
        """
        Salvestab seadmed JSON-faili.
        """
        json_storage = JSONStorage("../devices.json")
        json_storage.save(self.manager.get_devices_as_dicts())
        messagebox.showinfo("Info", "Andmed salvestatud JSON-faili")

    def load_json(self):
        """
        Laeb seadmed JSON-failist.
        """
        try:
            json_storage = JSONStorage("../devices.json")
            devices_data = json_storage.load()
            self.manager.load_devices_from_dicts(devices_data)
            self.refresh_list()
            messagebox.showinfo("Info", "Andmed laetud JSON-failist")
        except FileNotFoundError:
            messagebox.showerror("Viga", "JSON-faili ei leitud")