import json
import os
import pandas as pd
os.environ["PLOTLYJS"] = "/usr/lib/python3/dist-packages/plotly/package_data/plotly.min.js"
import openpyxl
from openpyxl.chart import PieChart, Reference
from openpyxl.utils.dataframe import dataframe_to_rows  
import plotly.express as px

def nacti_json_soubor(soubor):
    """Načte JSON soubor a vrátí jeho obsah."""
    with open(soubor, 'r', encoding='utf-8') as soubor:
        return json.load(soubor)

def preved_json_na_dataframe(data):
    """Převede data z JSON na DataFrame."""
    finance_stranky = data['data']['financePage']
    zpracovana_data = {
        'ID': [],
        'Název': [],
        'Částka': [],
        'Typ financí': [],
        'Název projektu': [],
        'Datum zahájení': [],
        'Datum ukončení': []
    }

    for stranka in finance_stranky:
        zpracovana_data['ID'].append(stranka['id'])
        zpracovana_data['Název'].append(stranka['name'])
        zpracovana_data['Částka'].append(stranka['amount'])
        zpracovana_data['Typ financí'].append(stranka['financeType'][0]['name'])
        zpracovana_data['Název projektu'].append(stranka['project']['name'])
        zpracovana_data['Datum zahájení'].append(stranka['project']['startdate'])
        zpracovana_data['Datum ukončení'].append(stranka['project']['enddate'])

    return pd.DataFrame(zpracovana_data)

def uloz_do_excelu(dataframe, excel_soubor):
    """Uloží DataFrame do Excel souboru včetně grafů."""
    wb = openpyxl.Workbook()
    ws = wb.active

    for radek in dataframe_to_rows(dataframe, index=False, header=True):
        ws.append(radek)

    # Vytvoř koláčový graf
    kolac = PieChart()
    popisky = Reference(ws, min_col=4, min_row=2, max_row=len(dataframe)+1)
    data = Reference(ws, min_col=3, min_row=2, max_row=len(dataframe)+1)
    kolac.add_data(data, titles_from_data=True)
    kolac.set_categories(popisky)
    kolac.title = "Analýza financí - Koláčový graf"
    ws.add_chart(kolac, "G1")

    # Vytvoř Sunburst graf
    sunburst_graf = px.sunburst(dataframe, path=['Typ financí', 'Název projektu'], values='Částka', title='Analýza financí - Sunburst graf')
    sunburst_graf.update_traces(textinfo='label+percent entry')
    sunburst_graf.write_image("sunburst_graf.png")
    obrazek = openpyxl.drawing.image.Image("sunburst_graf.png")
    ws.add_image(obrazek, 'G10')

    wb.save(excel_soubor)

def main():
    json_soubor = 'finance_analysis.json'
    excel_soubor = 'finance_data.xlsx'

    # Načti JSON soubor
    data = nacti_json_soubor(json_soubor)

    # Převeď JSON data na DataFrame
    df = preved_json_na_dataframe(data)

    # Ulož DataFrame do Excelu s grafy
    uloz_do_excelu(df, excel_soubor)

if __name__ == "__main__":
    main()
