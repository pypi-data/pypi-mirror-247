import requests
import json
import pandas
import os
import numpy
os.environ["cloudName"] = "mas"
os.environ['securityToken'] = os.environ['MAS_TOKEN']


def get_meta_data():
    url = "https://"+os.environ["cloudName"] + \
        ".app.perfectomobile.com/test-execution-management-webapp/rest/v1/metadata"

    payload = {}
    headers = {
        'Perfecto-Authorization': os.environ['securityToken'],
        'perfecto-tenantid': os.environ["cloudName"] + '-perfectomobile-com'
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    result = json.loads(response.content)
    return result


def get_failure_reason_name_category(result):
    try:
        resultList = result["failureReasons"]
    except TypeError:
        print(result)
    if (len(resultList) > 0):
        return pandas.DataFrame(resultList, columns=['name', 'category'])
    else:
        return pandas.DataFrame()


def get_failure_reason_category(df, name):
    try:
        result = df.loc[df['failureReasonName'] == name, 'category'].iloc[0]
    except IndexError:
        result = ""
    return result


result = get_meta_data()
category_df = get_failure_reason_name_category(result)
category_df.rename(columns={'name': 'failureReasonName'}, inplace=True)
category = get_failure_reason_category(category_df, 'Timeout issue')
print(category)

df = pandas.read_csv(
    '/Users/genesis.thomas/workspace/python/generic/PerfectoCustomReport/src/perfecto/output.csv', low_memory=False)
print(df['failureReasonName'])
total = len(df)
# ----

fail_block = df[(df["status"] == "FAILED") | (df["status"] == "BLOCKED")]
df = fail_block[~fail_block.name.isin(
    ["Interactive session"])]
df = category_df.merge(df, how="inner", on="failureReasonName").pivot_table(
    index=['status', 'category', 'failureReasonName'], aggfunc='size')
df = pandas.DataFrame(df).sort_values(by=0, ascending=False).sort_values(
    by="status", ascending=False).head(10).rename(columns={0: "Total"})
df['%'] = round(df["Total"].div(
    total).mul(100).astype(float), 1).astype(str) + '%'
print(df)
failurecategorytable = {}
failurecategorytable = df.to_html(
    table_id="failurecategory",
    index=True,
    render_links=True,
    escape=False,
)
print(failurecategorytable)
pass
