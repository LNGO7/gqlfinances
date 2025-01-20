from src.utils import flatten, queryGQL
import pandas as pd

#####################################################################################
# github.com/LNGO7/gql_finances
#####################################################################################
query = """query($where: FinanceInputWhereFilter){
  result: financePage (where: $where, limit:1000) {
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

async def resolve_json(variables, cookies):
    assert "where" in variables, f"missing where in parameters"
    jsonresponse = await queryGQL(
        query=query,
        variables=variables,
        cookies=cookies
    )

    # Extract our "result" from the top-level data
    data = jsonresponse.get("data", {"result": None})
    result = data.get("result", None)
    assert result is not None, f"got {jsonresponse}"
    return result

async def resolve_flat_json(variables, cookies):
    """
    Flatten the financePage data into a list of dictionaries that can be pivoted easily.
    """
    jsonData = await resolve_json(variables=variables, cookies=cookies)
    mapper = {
        "finance_id": "id",
        "finance_name": "name",
        "finance_amount": "amount",
        "finance_valid": "valid",
        "finance_lastchange": "lastchange",

        "financeType_id": "financeType.id",
        "financeType_name": "financeType.name",
        
        "project_id": "project.id",
        "project_name": "project.name",
        "project_startdate": "project.startdate",
        "project_enddate": "project.enddate",
        "project_valid": "project.valid",

        "team_id": "project.team.id",
        "team_name": "project.team.name",

        "changedby_id": "changedby.id",
        "changedby_name": "changedby.name"
    }

    pivotdata = list(flatten(jsonData, {}, mapper))
    return pivotdata

async def resolve_df_pivot(variables, cookies):

    pivotdata = await resolve_flat_json(variables=variables, cookies=cookies)
    df = pd.DataFrame(pivotdata)

    # Example pivot: sum of amounts (finance_amount) grouped by financeType_name and project_name
    pdf = pd.pivot_table(
        df,
        values="finance_amount",     # numeric field to aggregate
        index="financeType_name",    # rows
        columns=["project_name"],    # columns
        aggfunc="sum"               # aggregation function
    )
    return pdf


#####################################################################################
# Router definice
#####################################################################################
import string
import openpyxl
from tempfile import NamedTemporaryFile
from fastapi import APIRouter, Request, Query, Response
from ..utils import process_df_as_html_page
import json
import re
import io

def createRouter(prefix):
    mainpath = "/finances"
    tags = ["Finance Data"]

    router = APIRouter(prefix=prefix)
    WhereDescription = "Filtr (where) JSON pro financePage"

    @router.get(f"{mainpath}/table", tags=tags, summary="HTML tabulka z financePage")
    async def finance_data_html(
        request: Request,
        where: str = Query(description=WhereDescription)
    ):
        wherevalue = None if where is None else re.sub(r'{([^:"]*):', r'{"\1":', where)
        wherejson = json.loads(wherevalue)

        pd_data = await resolve_flat_json(
            variables={"where": wherejson},
            cookies=request.cookies
        )
        df = pd.DataFrame(pd_data)
        return await process_df_as_html_page(df)

    @router.get(f"{mainpath}/flatjson", tags=tags, summary="Flattened JSON from financePage")
    async def finance_data_flat_json(
        request: Request,
        where: str = Query(description=WhereDescription),
    ):
        """
        Flattened JSON from financePage
        """
        wherevalue = None if where is None else re.sub(r'{([^:"]*):', r'{"\1":', where)
        wherejson = json.loads(wherevalue)

        pd_data = await resolve_flat_json(
            variables={"where": wherejson},
            cookies=request.cookies
        )
        return pd_data

    @router.get(f"{mainpath}/json", tags=tags, summary="Raw JSON from financePage")
    async def finance_data_json(
        request: Request,
        where: str = Query(description=WhereDescription),
    ):
        """
        Raw JSON (tree structure) from financePage
        """
        wherevalue = None if where is None else re.sub(r'{([^:"]*):', r'{"\1":', where)
        wherejson = json.loads(wherevalue)

        pd_data = await resolve_json(
            variables={"where": wherejson},
            cookies=request.cookies
        )
        return pd_data

    @router.get(f"{mainpath}/xlsx", tags=tags, summary="XLSX soubor doplněný o finance data")
    async def finance_data_xlsx(
        request: Request,
        where: str = Query(description=WhereDescription),
    ):
        wherevalue = None if where is None else re.sub(r'{([^:"]*):', r'{"\1":', where)
        wherejson = json.loads(wherevalue)

        flat_json = await resolve_flat_json(
            variables={"where": wherejson},
            cookies=request.cookies
        )

        with open('./src/xlsx/vzor2.xlsx', 'rb') as f:
            content = f.read()

        memory = io.BytesIO(content)
        resultFile = openpyxl.load_workbook(filename=memory)
        resultFileData = resultFile['data']

        for rid, item in enumerate(flat_json, start=2):
            for col, value in zip(string.ascii_uppercase, item.values()):
                cellname = f"{col}{rid}"
                resultFileData[cellname] = value

        with NamedTemporaryFile() as tmp:
            resultFile.save(tmp)
            tmp.seek(0)
            stream = tmp.read()
            headers = {
                'Content-Disposition': 'attachment; filename="FinanceAnalysis.xlsx"'
            }
            return Response(stream, media_type='application/vnd.ms-excel', headers=headers)

    return router
