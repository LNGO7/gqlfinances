import asyncio
import aiohttp
import pandas as pd
import json
import AddMoreData as custom_data
import PrepareFiles as graph

async def getToken(username, password):
    keyurl = "http://localhost:33001/oauth/login3"
    async with aiohttp.ClientSession() as session:
        async with session.get(keyurl) as resp:
            if resp.status != 200:
                raise Exception(f"Failed to get key: {resp.status}")
            keyJson = await resp.json()

        payload = {"key": keyJson["key"], "username": username, "password": password}
        async with session.post(keyurl, json=payload) as resp:
            if resp.status != 200:
                raise Exception(f"Failed to get token: {resp.status}")
            tokenJson = await resp.json()

    return tokenJson.get("token", None)

def query(q, token):
    async def post(variables):
        gqlurl = "http://localhost:33001/api/gql"
        payload = {"query": q, "variables": variables}
        cookies = {'authorization': token}

        async with aiohttp.ClientSession() as session:
            async with session.post(gqlurl, json=payload, cookies=cookies) as resp:
                if resp.status != 200:
                    text = await resp.text()
                    raise Exception(f"Query failed: {resp.status} - {text}")
                return await resp.json()
    return post

username = "john.newbie@world.com"
password = "john.newbie@world.com"
queryStr = """
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
def transform_gql_to_json(gql_query):
    sourceTable = []

    for finance_item in gql_query["financePage"]:
        row = {}
        row["id"] = finance_item["id"]
        row["name"] = finance_item["name"]
        row["amount"] = finance_item["amount"]
        row["valid"] = finance_item["valid"]
        row["lastchange"] = finance_item["lastchange"]
        row["financeTypeName"] = finance_item["financeType"][0]["name"]
        row["projectID"] = finance_item["project"]["id"]
        row["projectName"] = finance_item["project"]["name"]
        row["projectStartDate"] = finance_item["project"]["startdate"]
        row["projectEndDate"] = finance_item["project"]["enddate"]
        row["projectValid"] = finance_item["project"]["valid"]
        row["teamID"] = finance_item["project"]["team"]["id"]
        row["teamName"] = finance_item["project"]["team"]["name"]
        row["changedby"] = finance_item.get("changedby")  # Ensure changedby exists
        
        sourceTable.append(row)

    return sourceTable

async def fullPipe():
    token = await getToken(username, password)
    qfunc = query(queryStr, token)
    response = await qfunc({})

    data = response.get("data")
    if not data:
        raise ValueError("No data found in the response.")
    
    # Use the transform_gql_to_json function to transform the data
    transformed_data = transform_gql_to_json(data)
    
    # Convert to pandas DataFrame
    pandasData = pd.DataFrame(transformed_data)
    return pandasData

# Run the full pipeline asynchronously
if __name__ == "__main__":    
    loop = asyncio.get_event_loop()
    try:
        pandasData = loop.run_until_complete(fullPipe())
        print(pandasData)
        pandasData.to_json('finance_analysis.json', orient='records', lines=True)
        try:
            custom_data.main()
        except Exception as e:
            print("Pri pridavani vlastnich dat doslo k chybe v:")
            print(e)
        try:
            graph.main()
        except Exception as e:
            print("Pri grafovani doslo k chybe v:")
            print(e)
    except Exception as e:
        print(f"An error occurred: {e}")
