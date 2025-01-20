# GQLFINANCES
- install requirements.txt --> pip install -r requirements.txt

## How to run scripts in order: 
1. Run GetGQL.py -> the output will be finance_analysis.json
2. Run AddMoreData.py -> not required but essential to see how the graphs works
3. Run PrepareFiles.py -> to create xls file with graphs

# What does it do? 

## GetGQL.py

1. **Login to Website**:
   - Loads the login page.
   - Extracts the `key` value from the login form.
   - Submits login credentials via a POST request.

2. **Fetch Financial Data**:
   - Defines a GraphQL query to fetch financial data.
   - Sends the query to the GraphQL endpoint.
   - Returns the retrieved data in JSON format.

3. **Save Data to JSON File**:
   - Saves the retrieved data to a file named `finance_analysis.json`.

## AddMoreData.py

1. **Add Additional Data to Existing JSON File**:
   - Defines new financial data.
   - Loads the existing data from a specified JSON file.
   - Appends the new data to the existing data.
   - Saves the updated data back to the JSON file.
   - Created just to support graphs in PrepareFiles.py part

## PrepareFiles.py

1. **Load JSON Data**:
   - Reads and loads data from a JSON file.

2. **Convert JSON to DataFrame**:
   - Processes the loaded JSON data into a pandas DataFrame.

3. **Save DataFrame to Excel with Charts**:
   - Saves the DataFrame to an Excel file.
   - Adds a pie chart and a sunburst chart to the Excel file.

## __init__.py
   -  Prepared init file from hrbolek/analysis for matching provided query strings, and flattening functionality


