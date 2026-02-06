"""
JSON andmete salvestamise ja laadimise moodul.
"""

import json


class JSONStorage: # Klass andmete salvestamiseks ja laadimiseks JSON formaadis.

    def __init__(self, filename='devices.json'): #Loob uue JSON salvestuse objekti.
        self.filename = filename

    def save(self, devices_data): #Salvestab seadmete andmed JSON faili.
        with open(self.filename, 'w', encoding='utf-8') as file:
            # Salvestame JSON formaadis
            # indent=2 teeb faili loetavamaks (kaunistab)
            # ensure_ascii=False võimaldab eesti tähti
            json.dump(devices_data, file, ensure_ascii=False, indent=2)

    def load(self): #Laadib seadmete andmed JSON failist.
        try:
            with open(self.filename, 'r', encoding='utf-8') as file:
                return json.load(file)
        except FileNotFoundError:
            # Kui faili ei ole, tagastame tühja nimekirja
            return []