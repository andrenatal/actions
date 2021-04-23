import requests
import json
import os
import sys
import api_calls

print("read all the issues in the gh repo")
# read all the issues in the gh repo into a dict
dictissues = {"{} {}".format(item['title'], item["html_url"]):{ "state": item["state"], "milestone": item["milestone"] } for item in api_calls.readGhIssues(api_calls.url_issues) if 'pull_request' not in item}

print("clear the current trello list")
api_calls.deleteCheckLists(api_calls.getCheckListsOncard(api_calls.id_card))

# then we iterate the list of issues
for issue in dictissues:
    # discard if the issue is a PR
    if 'pull_request' in dictissues:
        continue
    checklistid = api_calls.getCheckListId(dictissues[issue]["milestone"], issue)
    api_calls.addCheckItem(checklistid, issue, dictissues[issue]["state"])
print("end")
