import tkinter as tk
from tkinter import messagebox, ttk

from Classes.Device import Device
from Classes.DeviceManager import DeviceManager
from Storage.CSVstorage import CSVStorage
from Storage.JSONstorage import JSONStorage


class DeviceApp: # GRAAFILINE AKEN

    def __init__(self, root):
        self.root = root
        self.root.title("IT-seadmete haldus")
        self.root.geometry("620x750")
        self.root.configure(bg="#f0f0f0")

        self.manager = DeviceManager()
        self.selected_index = None  # Hoiab meeles valitud seadme indeksit

        # Pealkiri
        title_label = tk.Label(
            root,
            text="IT-seadmete haldussüsteem KriSep",
            font=("Arial", 18, "bold"),
            bg="#f0f0f0",
            fg="#2c3e50"
        )
        title_label.grid(row=0, column=0, columnspan=2, pady=20)

        # Sisestuskastid
        input_frame = tk.Frame(root, bg="#f0f0f0")
        input_frame.grid(row=1, column=0, columnspan=2, padx=20, pady=10)

        labels = ["Seadme nimi:", "Seadme tüüp:", "Seisund:", "Inventarinumber:"]

        for i, label_text in enumerate(labels):
            label = tk.Label(
                input_frame,
                text=label_text,
                font=("Arial", 11),
                bg="#f0f0f0",
                fg="#34495e"
            )
            label.grid(row=i, column=0, sticky="w", pady=8, padx=(0, 10))

        self.name_entry = tk.Entry(input_frame, font=("Arial", 11), width=30)
        self.type_entry = tk.Entry(input_frame, font=("Arial", 11), width=30)

        # Rippmenüü seisundite jaoks
        self.status_var = tk.StringVar()
        self.status_dropdown = ttk.Combobox(
            input_frame,
            textvariable=self.status_var,
            values=["available", "in_use", "broken"],
            state="readonly",
            font=("Arial", 11),
            width=28
        )
        self.status_dropdown.current(0)

        self.inventory_number_entry = tk.Entry(input_frame, font=("Arial", 11), width=30)

        self.name_entry.grid(row=0, column=1, pady=8)
        self.type_entry.grid(row=1, column=1, pady=8)
        self.status_dropdown.grid(row=2, column=1, pady=8)
        self.inventory_number_entry.grid(row=3, column=1, pady=8)

        # Nupud
        button_frame = tk.Frame(root, bg="#f0f0f0")
        button_frame.grid(row=2, column=0, columnspan=2, pady=15)

        # Peamised nupud
        add_btn = tk.Button(
            button_frame,
            text="Lisa seade",
            command=self.add_device,
            bg="#27ae60",
            fg="white",
            font=("Arial", 10, "bold"),
            width=20,
            cursor="hand2",
            relief="flat",
            bd=0,
            padx=10,
            pady=8
        )
        add_btn.grid(row=0, column=0, columnspan=2, pady=5, padx=5)

        edit_btn = tk.Button(
            button_frame,
            text="Muuda",
            command=self.edit_device,
            bg="#3498db",
            fg="white",
            font=("Arial", 10, "bold"),
            width=20,
            cursor="hand2",
            relief="flat",
            bd=0,
            padx=10,
            pady=8
        )
        edit_btn.grid(row=1, column=0, pady=5, padx=5)

        delete_btn = tk.Button(
            button_frame,
            text="Kustuta",
            command=self.delete_device,
            bg="#e74c3c",
            fg="white",
            font=("Arial", 10, "bold"),
            width=20,
            cursor="hand2",
            relief="flat",
            bd=0,
            padx=10,
            pady=8
        )
        delete_btn.grid(row=1, column=1, pady=5, padx=5)

        # Failihalduse nupud
        file_frame = tk.Frame(button_frame, bg="#f0f0f0")
        file_frame.grid(row=2, column=0, columnspan=2, pady=10)

        tk.Label(
            file_frame,
            text="Failihaldus:",
            font=("Arial", 10, "bold"),
            bg="#f0f0f0",
            fg="#7f8c8d"
        ).grid(row=0, column=0, columnspan=4, pady=(10, 5))

        save_csv_btn = tk.Button(
            file_frame,
            text="Salvesta CSV",
            command=self.save_csv,
            bg="#95a5a6",
            fg="white",
            font=("Arial", 9),
            width=15,
            cursor="hand2",
            relief="flat",
            bd=0,
            pady=5
        )
        save_csv_btn.grid(row=1, column=0, padx=3)

        load_csv_btn = tk.Button(
            file_frame,
            text="Lae CSV",
            command=self.load_csv,
            bg="#7f8c8d",
            fg="white",
            font=("Arial", 9),
            width=15,
            cursor="hand2",
            relief="flat",
            bd=0,
            pady=5
        )
        load_csv_btn.grid(row=1, column=1, padx=3)

        save_json_btn = tk.Button(
            file_frame,
            text="Salvesta JSON",
            command=self.save_json,
            bg="#95a5a6",
            fg="white",
            font=("Arial", 9),
            width=15,
            cursor="hand2",
            relief="flat",
            bd=0,
            pady=5
        )
        save_json_btn.grid(row=1, column=2, padx=3)

        load_json_btn = tk.Button(
            file_frame,
            text="Lae JSON",
            command=self.load_json,
            bg="#7f8c8d",
            fg="white",
            font=("Arial", 9),
            width=15,
            cursor="hand2",
            relief="flat",
            bd=0,
            pady=5
        )
        load_json_btn.grid(row=1, column=3, padx=3)

        # Seadmete nimekiri
        list_label = tk.Label(
            root,
            text="Lisatud seadmed:",
            font=("Arial", 11, "bold"),
            bg="#f0f0f0",
            fg="#2c3e50"
        )
        list_label.grid(row=3, column=0, columnspan=2, pady=(15, 5))

        # Kast lisatud seadmete loeteluks
        list_frame = tk.Frame(root, bg="#f0f0f0")
        list_frame.grid(row=4, column=0, columnspan=2, padx=20, pady=5)

        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.listbox = tk.Listbox(
            list_frame,
            width=70,
            height=12,
            font=("Courier", 10),
            yscrollcommand=scrollbar.set,
            selectmode=tk.SINGLE,
            relief="solid",
            bd=1
        )
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH)
        scrollbar.config(command=self.listbox.yview)

        self.listbox.bind('<<ListboxSelect>>', self.on_select)

    def refresh_list(self): # Uuendab nimekirja
        self.listbox.delete(0, tk.END)

        for device in self.manager.devices:
            self.listbox.insert(
                tk.END,
                f"{device.name} | {device.device_type} | "
                f"{device.status} | {device.inventory_number}"
            )

        # Taasta valik, kui on olemas
        if self.selected_index is not None and self.selected_index < len(self.manager.devices):
            self.listbox.selection_set(self.selected_index)

    def clear_entries(self): # Tühjendab väljad
        self.name_entry.delete(0, tk.END)
        self.type_entry.delete(0, tk.END)
        self.status_var.set("available")
        self.inventory_number_entry.delete(0, tk.END)
        self.selected_index = None

    def on_select(self, event): # Seadmel klikk toob andmed väljadesse
        selection = self.listbox.curselection()
        if not selection:
            return

        self.selected_index = selection[0]
        device = self.manager.devices[self.selected_index]

        self.name_entry.delete(0, tk.END)
        self.name_entry.insert(0, device.name)

        self.type_entry.delete(0, tk.END)
        self.type_entry.insert(0, device.device_type)

        self.status_var.set(device.status)

        self.inventory_number_entry.delete(0, tk.END)
        self.inventory_number_entry.insert(0, device.inventory_number)

    def add_device(self): #Seadme lisamine ja kontroll, kas kõik väljad on täidetud
        name = self.name_entry.get().strip()
        device_type = self.type_entry.get().strip()
        inventory_number = self.inventory_number_entry.get().strip()

        # Valideeri sisend
        if not name or not device_type or not inventory_number:
            return

        # Lisa seade
        try:
            device = Device(
                name,
                device_type,
                self.status_var.get(),
                inventory_number
            )
            self.manager.add_device(device)
            self.refresh_list()
            self.clear_entries()
        except ValueError:
            pass

    def edit_device(self): # Lisatud andmete muutmine ja kontroll, kas kõik väljad on täidetud
        if self.selected_index is None:
            return

        name = self.name_entry.get().strip()
        device_type = self.type_entry.get().strip()
        inventory_number = self.inventory_number_entry.get().strip()

        # Valideeri sisend
        if not name or not device_type or not inventory_number:
            return

        try:
            device = self.manager.devices[self.selected_index]

            # Uuendab andmeid
            device.name = name
            device.device_type = device_type
            device.status = self.status_var.get()
            device.inventory_number = inventory_number

            self.refresh_list()
            # EI tühjenda välju, jätab valiku aktiivseks
        except (ValueError, IndexError):
            pass

    def delete_device(self): #Valitud seadme kustutamine
        if self.selected_index is None:
            return

        try:
            device = self.manager.devices[self.selected_index]
            if self.manager.delete_device(device.name):
                self.refresh_list()
                self.clear_entries()
        except IndexError:
            pass

    def save_csv(self): # CSV salvestus
        try:
            csv_storage = CSVStorage("./devices.csv")
            csv_storage.save(self.manager.get_devices_as_dicts())
        except Exception:
            pass

    def load_csv(self): # CSV laadimine
        try:
            csv_storage = CSVStorage("./devices.csv")
            devices_data = csv_storage.load()
            self.manager.load_devices_from_dicts(devices_data)
            self.refresh_list()
        except FileNotFoundError:
            pass

    def save_json(self): # JSON salvestus
        try:
            json_storage = JSONStorage("./devices.json")
            json_storage.save(self.manager.get_devices_as_dicts())
        except Exception:
            pass

    def load_json(self): # JSON laadimine
        try:
            json_storage = JSONStorage("./devices.json")
            devices_data = json_storage.load()
            self.manager.load_devices_from_dicts(devices_data)
            self.refresh_list()
        except FileNotFoundError:
            pass