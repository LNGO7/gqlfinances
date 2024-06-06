import json
import os

# Funkce pro přidání dodatečných dat do stávajícího JSON souboru
def add_additional_data(json_file):
    # Definice nových dat
    additional_data = [
        {
            "id": "f911230f-7e1f-4e9b-90a9-b921996ceb88",
            "name": "komplet2",
            "amount": 200000,
            "valid": False,
            "lastchange": "2024-06-07T13:41:14.491289",
            "financeType": [
                {
                    "id": "9e37059c-de2c-4112-9009-559c8b0396f2",
                    "name": "firemní náklady"
                }
            ],
            "project": {
                "id": "43dd2ff1-5c17-42a5-ba36-8b30e2a243bc",
                "name": "Nukleární reaktor pro budovy 2",
                "startdate": "2023-01-01T17:27:12",
                "enddate": "2025-12-31T17:27:12",
                "valid": True,
                "team": {
                    "id": "2d9dcd22-a4a2-11ed-b9df-0242ac120004",
                    "name": "Uni 2"
                }
            },
            "changedby": None
        },
        {
            "id": "f911230f-7e1f-4e9b-90a9-b921996ceb89",
            "name": "komplet3",
            "amount": 300000,
            "valid": True,
            "lastchange": "2024-06-08T13:41:14.491289",
            "financeType": [
                {
                    "id": "9e37059c-de2c-4112-9009-559c8b0396f3",
                    "name": "dopravní náklady"
                }
            ],
            "project": {
                "id": "43dd2ff1-5c17-42a5-ba36-8b30e2a243bd",
                "name": "Nukleární reaktor pro budovy 3",
                "startdate": "2023-01-01T17:27:12",
                "enddate": "2025-12-31T17:27:12",
                "valid": True,
                "team": {
                    "id": "2d9dcd22-a4a2-11ed-b9df-0242ac120005",
                    "name": "Uni 3"
                }
            },
            "changedby": None
        },
        {
            "id": "f911230f-7e1f-4e9b-90a9-b921996ceb90",
            "name": "komplet4",
            "amount": 400000,
            "valid": True,
            "lastchange": "2024-06-09T13:41:14.491289",
            "financeType": [
                {
                    "id": "9e37059c-de2c-4112-9009-559c8b0396f4",
                    "name": "technické náklady"
                }
            ],
            "project": {
                "id": "43dd2ff1-5c17-42a5-ba36-8b30e2a243be",
                "name": "Nukleární reaktor pro budovy 4",
                "startdate": "2023-01-01T17:27:12",
                "enddate": "2025-12-31T17:27:12",
                "valid": True,
                "team": {
                    "id": "2d9dcd22-a4a2-11ed-b9df-0242ac120006",
                    "name": "Uni 4"
                }
            },
            "changedby": None
        }
    ]

    # Načtení stávajících dat ze souboru
    with open(json_file, 'r') as file:
        data = json.load(file)

    # Přidání nových dat do seznamu "financePage"
    data["data"]["financePage"].extend(additional_data)

    # Uložení aktualizovaných dat zpět do souboru
    with open(json_file, 'w') as file:
        json.dump(data, file, indent=4)

# Hlavní funkce pro spuštění skriptu
def main():
    # Nastavení cesty k souboru finance_analysis.json
    json_file = "finance_analysis.json"

    # Pokud soubor existuje, přidej do něj dodatečná data
    if os.path.exists(json_file):
        add_additional_data(json_file)
        print("Dodatečná data byla úspěšně přidána.")
    else:
        print("Soubor finance_analysis.json neexistuje.")

# Spuštění hlavní funkce
if __name__ == "__main__":
    main()
