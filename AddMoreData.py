import json
import os

def add_additional_data(json_file):
    # Pridame data pro lepsi ukazku grafu
    additional_data = [
        {
            "id": "f911230f-7e1f-4e9b-90a9-b921996ceb88",
            "name": "komplet2",
            "amount": 200000,
            "valid": False,
            "lastchange": "2024-06-07T13:41:14.491289",
            "financeTypeName": "firemní náklady",
            "projectID": "43dd2ff1-5c17-42a5-ba36-8b30e2a243bc",
            "projectName": "Nukleární reaktor pro budovy 2",
            "projectStartDate": "2021-01-01T17:27:12",
            "projectEndDate": "2022-12-31T17:27:12",
            "projectValid": True,
            "teamID": "2d9dcd22-a4a2-11ed-b9df-0242ac120004",
            "teamName": "Uni 2",
            "changedby": None
        },
        {
            "id": "f911230f-7e1f-4e9b-90a9-b921996ceb89",
            "name": "komplet3",
            "amount": 300000,
            "valid": True,
            "lastchange": "2024-06-08T13:41:14.491289",
            "financeTypeName": "dopravní náklady",
            "projectID": "43dd2ff1-5c17-42a5-ba36-8b30e2a243bd",
            "projectName": "Nukleární reaktor pro budovy 3",
            "projectStartDate": "2026-01-01T17:27:12",
            "projectEndDate": "2027-03-20T17:27:12",
            "projectValid": True,
            "teamID": "2d9dcd22-a4a2-11ed-b9df-0242ac120005",
            "teamName": "Uni 3",
            "changedby": None
        },
        {
            "id": "f911230f-7e1f-4e9b-90a9-b921996ceb90",
            "name": "komplet4",
            "amount": 400000,
            "valid": True,
            "lastchange": "2024-06-09T13:41:14.491289",
            "financeTypeName": "technické náklady",
            "projectID": "43dd2ff1-5c17-42a5-ba36-8b30e2a243be",
            "projectName": "Nukleární reaktor pro budovy 4",
            "projectStartDate": "2024-01-01T17:27:12",
            "projectEndDate": "2024-11-29T17:27:12",
            "projectValid": True,
            "teamID": "2d9dcd22-a4a2-11ed-b9df-0242ac120006",
            "teamName": "Uni 4",
            "changedby": None
        }
    ]

    with open(json_file, 'r') as file:
        data = json.load(file)

    if isinstance(data, dict):  # Zajistime, aby jsme pracovali s listem
        data = [data]
    data.extend(additional_data)

    with open(json_file, 'w') as file:
        json.dump(data, file, indent=4)

def main():
    # Cesta k souboru
    json_file = "finance_analysis.json"
    if os.path.exists(json_file):
        add_additional_data(json_file)
        print("Additional data successfully added.")
    else:
        print("File finance_analysis.json does not exist.")

if __name__ == "__main__":
    main()
