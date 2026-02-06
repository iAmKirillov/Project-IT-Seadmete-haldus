"""
IT-seadme klass.
"""
class Device:

    # Siin on nimekiri lubatud seisunditest
    VALID_STATUSES = ['Available', 'In use', 'Broken']

    def __init__(self, name, device_type, status, inventory_number):
        self.name = name
        self.device_type = device_type
        self.inventory_number = inventory_number

        # Kontrollime, et seisund oleks lubatud
        if status not in self.VALID_STATUSES:
            raise ValueError(f"Vigane seisund '{status}'")

        self.status = status

    def change_status(self, new_status): #Muudab seadme seisundit.

        if new_status not in self.VALID_STATUSES:
            raise ValueError(
                f"Vigane seisund '{new_status}'. "
                f"Lubatud: {', '.join(self.VALID_STATUSES)}"
            )
        self.status = new_status

    def to_dict(self): #Teisendab seadme objekti sõnastikuks (dict).
        return {
            'name': self.name,
            'device_type': self.device_type,
            'status': self.status,
            'inventory_number': self.inventory_number
        }

    def __str__(self): #Tagastab seadme inimloetava kirjelduse.
        return (f"{self.name} ({self.device_type}) - "
                f"Seisund: {self.status}, "
                f"Inventarinumber: {self.inventory_number}")