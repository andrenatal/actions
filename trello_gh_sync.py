import requests
import json

trello_key = 'xx'
trello_token = 'xx'
id_checkitems = 'xx'
id_card = 'xx'
url_issues = "xx"

def addCheckItem(idCheckList, issueTitle, checked):
    url = "https://api.trello.com/1/checklists/{}/checkItems".format(idCheckList)
    query = {
    'key': trello_key,
    'token': trello_token,
    'name': issueTitle,
    'checked': "false" if checked == "open" else "true"
    }
    response = requests.request(
        "POST",
        url,
        params=query
    )
    return response.text

def getCheckItems(idCheckList):
    url = "https://api.trello.com/1/checklists/{}/checkItems".format(idCheckList)
    query = {
    'key': trello_key,
    'token': trello_token
    }
    response = requests.request(
        "GET",
        url,
        params=query
    )
    return response.text

def readGhIssues(urlIssues):
    response = requests.request(
        "GET",
        urlIssues
    )
    return response.text

def markCheckItemComplete(id_card, id_checkitem):
    url = "https://api.trello.com/1/cards/{}/checkItem/{}".format(id_card, id_checkitem)
    query = {
    'key': trello_key,
    'token': trello_token,
    'state': 'complete'
    }
    response = requests.request(
        "PUT",
        url,
        params=query
    )
    return response.text

# first read the checkitem list for the extension card into a dict
lista = json.loads(getCheckItems(id_checkitems))
dictcheckitems = {"{}".format(item["name"]):item for item in json.loads(getCheckItems(id_checkitems))}

# then we read all the issues in the gh repo into a dict
dictissues = {"{} {}".format(item['title'], item["html_url"]):item["state"] for item in json.loads(readGhIssues(url_issues))}

# then we iterate the list of issues
for issue in dictissues:
    # and check if that item exits in the trello card
    if (issue not in dictcheckitems):
        # if not, then we add
        addCheckItem(id_checkitems, issue, dictissues[issue])
    else:
        # if exists, we check if the issue is closed, and if so, we mark as checked on trello
        if dictissues[issue] == "closed" and dictcheckitems[issue]["state"] != "complete":
            print("close " + issue)
            markCheckItemComplete(id_card, dictcheckitems[issue]["id"])
