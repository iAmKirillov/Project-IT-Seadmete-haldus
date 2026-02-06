import tkinter as tk
from tkinter import messagebox

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
        self.status_entry = tk.Entry(root)
        self.inventory_number_entry = tk.Entry(root)

        self.name_entry.grid(row=0, column=1)
        self.type_entry.grid(row=1, column=1)
        self.status_entry.grid(row=2, column=1)
        self.inventory_number_entry.grid(row=3, column=1)

        # ---- Nupud ----
        tk.Button(root, text="Lisa seade", command=self.add_device)\
            .grid(row=4, column=0, columnspan=2, pady=5)

        tk.Button(root, text="Kustuta valitud", command=self.delete_device)\
            .grid(row=6, column=0, columnspan=2, pady=5)

        tk.Button(root, text="Salvesta CSV", command=self.save_csv)\
            .grid(row=7, column=0)

        tk.Button(root, text="Lae CSV", command=self.load_csv)\
            .grid(row=7, column=1)

        tk.Button(root, text="Salvesta JSON", command=self.save_json)\
            .grid(row=8, column=0)

        tk.Button(root, text="Lae JSON", command=self.load_json)\
            .grid(row=8, column=1)

        # ---- Seadmete nimekiri ----
        self.listbox = tk.Listbox(root, width=60)
        self.listbox.grid(row=5, column=0, columnspan=2, pady=5)

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

    def add_device(self):
        """
        Lisab uue seadme.
        """
        try:
            device = Device(
                self.name_entry.get(),
                self.type_entry.get(),
                self.status_entry.get(),
                self.inventory_number_entry.get()
            )
            self.manager.add_device(device)
            self.refresh_list()
        except ValueError:
            messagebox.showerror("Viga", "Vigane seadme seisund")

    def delete_device(self):
        """
        Kustutab valitud seadme.
        """
        selection = self.listbox.curselection()
        if not selection:
            return

        self.manager.delete_device(selection[0])
        self.refresh_list()

    def save_csv(self):
        """
        Salvestab seadmed CSV-faili.
        """
        CSVStorage.save("devices.csv", self.manager.devices)
        messagebox.showinfo("Info", "Andmed salvestatud CSV-faili")

    def load_csv(self):
        """
        Laeb seadmed CSV-failist.
        """
        self.manager.devices = CSVStorage.load("devices.csv")
        self.refresh_list()

    def save_json(self):
        """
        Salvestab seadmed JSON-faili.
        """
        JSONStorage.save("devices.json", self.manager.devices)
        messagebox.showinfo("Info", "Andmed salvestatud JSON-faili")

    def load_json(self):
        """
        Laeb seadmed JSON-failist.
        """
        self.manager.devices = JSONStorage.load("devices.json")
        self.refresh_list()


if __name__ == "__main__":
    root = tk.Tk()
    app = DeviceApp(root)
    root.mainloop()

#TEST
