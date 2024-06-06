import requests
from bs4 import BeautifulSoup
import json

def login_and_get_session():
    login_url = "http://localhost:33001/oauth/login2?redirect_uri=/"

    # Načtení přihlašovací stránky
    response = requests.get(login_url)
    if response.status_code != 200:
        print("Nepodařilo se načíst přihlašovací stránku")
        return None

    # Extrakce hodnoty 'key' ze stránky
    soup = BeautifulSoup(response.text, 'html.parser')
    key_input = soup.find('input', {'name': 'key'})
    if not key_input:
        print("Nepodařilo se najít 'key' ve formuláři")
        return None

    key = key_input['value']

    # Přihlašovací údaje
    data = {
        "username": "nora.newbie@world.com",
        "password": "nora.newbie@world.com",
        "key": key
    }

    # Odeslání POST požadavku s přihlašovacími údaji
    session = requests.Session()
    response = session.post(login_url, data=data)
    if response.status_code == 200:
        print("Přihlášení bylo úspěšné")
        return session
    else:
        print(f"Přihlášení selhalo: {response.status_code} - {response.text}")
        return None

def fetch_finance_analysis_data(session):
    # Nastavení URL GraphQL endpointu
    graphql_url = "http://localhost:33001/api/gql"

    # Definice dotazu GraphQL
    query = """
    query FinanceAnalysis {
        financePage {
            id
            name
            amount
            valid
            lastchange
            financeType {
                id
                name
            }
            project {
                id
                name
                startdate
                enddate
                valid
                team {
                    id
                    name
                }
            }
            changedby {
                id
                name
            }
        }
    }
    """

    # Hlavičky pro GraphQL požadavek
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    # Odeslání dotazu
    response = session.post(graphql_url, json={'query': query}, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Chyba při odesílání dotazu: {response.status_code} - {response.text}")
        return None

def save_data_to_json(data, filename):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)

def main():
    session = login_and_get_session()
    if session:
        data = fetch_finance_analysis_data(session)
        if data:
            save_data_to_json(data, 'finance_analysis.json')
            print("Data byla uložena do finance_analysis.json")
        else:
            print("Nepodařilo se získat data")

if __name__ == "__main__":
    main()
