"""
Seadmete haldamise klass.
"""
from .Device import Device

class DeviceManager:
    """
    Klass seadmete haldamiseks.
    Hoiab kõiki seadmeid ja võimaldab neid hallata.
    """

    def __init__(self): #Loob uue seadmehalduri tühja seadmete nimekirjaga.
        self.devices = []

    def add_device(self, device): #Lisab uue seadme nimekirja.
        self.devices.append(device)

    def get_all_devices(self):  #Tagastab kõik seadmed.
        return self.devices

    def find_device_by_name(self, name): #Otsib seadet nime järgi.
        for device in self.devices:
            if device.name == name:
                return device
        return None

    def delete_device(self, name): #Kustutab seadme nime järgi.

        device = self.find_device_by_name(name)
        if device:
            self.devices.remove(device)
            return True
        return False

    def change_device_status(self, name, new_status): #Muudab seadme seisundit.

        device = self.find_device_by_name(name)
        if device:
            device.change_status(new_status)
            return True
        return False

    def get_devices_as_dicts(self): #        Tagastab kõik seadmed sõnastike nimekirjana.
        return [device.to_dict() for device in self.devices]

    def load_devices_from_dicts(self, devices_data): #Laadib seadmed sõnastike nimekirjast.

        self.devices = []
        for data in devices_data:
            device = Device(
                name=data['name'],
                device_type=data['device_type'],
                status=data['status'],
                inventory_number=data['inventory_number']
            )
            self.devices.append(device)