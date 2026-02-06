"""
CSV andmete salvestamise ja laadimise moodul.
Kasutab Eesti CSV formaati: semikoolon (;) eraldajana.
"""
import csv
from Classes.Device import Device

class CSVStorage: #Klass andmete salvestamiseks ja laadimiseks CSV formaadis.

    def __init__(self, filename='devices.csv'): #Loob uue CSV salvestuse objekti.

        self.filename = filename
    def save(self, devices_data): #Salvestab seadmete andmed CSV faili.

        # Kui andmeid pole, loome tühja faili päisega
        if not devices_data:
            with open(self.filename, 'w', encoding='utf-8', newline='') as file:
                writer = csv.writer(file, delimiter=';')
                writer.writerow(['name', 'device_type', 'status', 'inventory_number'])
            return

        # Avame faili kirjutamiseks
        with open(self.filename, 'w', encoding='utf-8', newline='') as file:
            # Võtame väljade nimed esimesest seadmest
            fieldnames = list(devices_data[0].keys())

            # Loome CSV kirjutaja semikooloniga
            writer = csv.DictWriter(file, fieldnames=fieldnames, delimiter=';')

            # Kirjutame päise (esimene rida)
            writer.writeheader()

            # Kirjutame kõik seadmed
            writer.writerows(devices_data)

    def load(self): #Laadib seadmete andmed CSV failist.
        try:
            with open(self.filename, 'r', encoding='utf-8', newline='') as file:
                reader = csv.DictReader(file, delimiter=';')
                return list(reader)
        except FileNotFoundError:
            return []