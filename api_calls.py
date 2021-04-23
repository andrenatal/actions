
import requests
import json
import os
import sys

trello_key = os.environ['TRELLO_KEY']
trello_token = os.environ['TRELLO_TOKEN']
id_card = os.environ['CARD_ID']
url_issues = os.environ['URL_ISSUES']
token = os.environ['GH_TOKEN']
milestonesListIds = {}

def addCheckItem(idCheckList, issueTitle, checkedOrNot):
    url = "https://api.trello.com/1/checklists/{}/checkItems".format(idCheckList)
    query = {
        'key': trello_key,
        'token': trello_token,
        'name': issueTitle,
        'checked': "false" if checkedOrNot == "open" else "true"
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
    return response.text

def getCheckListsOncard(id_card):
    url = "https://api.trello.com/1/cards/{}/checklists".format(id_card)
    query = {
        'key': trello_key,
        'token': trello_token,
    }
    response = requests.request(
        "GET",
        url,
        params=query
    )
    return response.text

def deleteCheckLists(checklists):
    for checklist in json.loads(checklists):
        url = "https://api.trello.com/1/cards/{}/checklists/{}".format(id_card, checklist["id"])
        query = {
            'key': trello_key,
            'token': trello_token,
        }
        response = requests.request(
            "DELETE",
            url,
            params=query
        )
        print(response.text)
    return True

def getCheckListId(milestoneDict, issue):
    milestoneTitle = ""
    if not milestoneDict :
        milestoneTitle = "Untriaged"
    else:
        milestoneTitle = milestoneDict["title"]

    if milestoneTitle in milestonesListIds:
        return milestonesListIds[milestoneTitle]
    else:
        url = "https://api.trello.com/1/cards/{}/checklists".format(id_card)
        query = {
            'key': trello_key,
            'token': trello_token,
            'name': milestoneTitle
        }
        response = requests.request(
            "POST",
            url,
            params=query
        )
        milestonesListIds[milestoneTitle] = json.loads(response.text)["id"]
        return id
