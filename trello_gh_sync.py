import requests
import json
import os
import sys

trello_key = os.environ['TRELLO_KEY']
trello_token = os.environ['TRELLO_TOKEN']
id_checkitems = os.environ['CHECKITEMS_ID']
id_card = os.environ['CARD_ID'] 
url_issues = os.environ['URL_ISSUES'] 
token = os.environ['GH_TOKEN']

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
    print(response.text)
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
    print(response.text)
    return response.text

def readGhIssues(urlIssues):
    headers = {'Authorization': 'token ' + token}
    empty = False
    pagenum = 1
    issueslist = []
    while not empty:
        print("GH API request")
        response = requests.request(
            "GET",
            urlIssues.format(pagenum),
            headers=headers
        )
        pagenum += 1
        print(response.text)        
        _issuelist = json.loads(response.text)
        if "message" in _issuelist:
            sys.exit(response.text)
        if len(_issuelist) == 0:
            empty = True
        else:
            issueslist.extend(_issuelist)
    return issueslist

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
    print(response.text)
    return response.text

print("read the checkitem list for the extension card")
# first read the checkitem list for the extension card into a dict
lista = json.loads(getCheckItems(id_checkitems))
dictcheckitems = {"{}".format(item["name"]):item for item in json.loads(getCheckItems(id_checkitems))}
print("read all the issues in the gh repo")
# then we read all the issues in the gh repo into a dict
dictissues = {"{} {}".format(item['title'], item["html_url"]):item["state"] for item in readGhIssues(url_issues) if 'pull_request' not in item}
print("iterating the list of issues and matching")
# then we iterate the list of issues
for issue in dictissues:
    # discard if the issue is a PR
    if 'pull_request' in dictissues:
        continue
    # and check if that item exists in the trello card
    if (issue not in dictcheckitems):
        # if not, then we add
        addCheckItem(id_checkitems, issue, dictissues[issue])
    else:
        # if exists, we check if the issue is closed, and if so, we mark as checked on trello
        if dictissues[issue] == "closed" and dictcheckitems[issue]["state"] != "complete":
            print("close " + issue)
            markCheckItemComplete(id_card, dictcheckitems[issue]["id"])
print("end")
