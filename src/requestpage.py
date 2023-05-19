# -*- coding: utf-8 -*-

import requests, re, sys

# This module is to support `makegraph.py`.

# Since we have no loadlib support,
# loadlib dependencies has to be added to this list
# Example: for Module:Name with dependencies Module:Name1 and Module:Name2,
# ["Name"] = ["Name1", "Name2"]
additionalDependenciesList = {

}

def requestPage(page):
    payload = {
        "action": "query",
        "format": "json",
        "prop": "revisions",
        "titles": page.replace(" ", "_"),
        "formatversion": 2,
        "rvprop": "content",
        "rvslots": "*",
    }
    try:
        resp = requests.get("https://hypixel-skyblock.fandom.com/api.php", params=payload)
        data = resp.json()
        content = "" if "missing" in data["query"]["pages"][0] else data["query"]["pages"][0]["revisions"][0]["slots"]["main"]["content"]
    except Exception as e:
        print("Errored in requesting page: " + page)
        print(e)
        print(data)
        print("Exiting")
        sys.exit()

    return content

# scan page, return all required modules
# require('Module:Arguments')
# loader.require('Module:Arguments')
# loader.lazy.require('Module:Arguments')
# mw.loadData('Module:Arguments')
# loader.loadData('Module:Arguments')
# loader.lazy.loadData('Module:Arguments')
lineFormats = [
    r'(?<!\.)require\((.*?)\)',
    r'mw\.loadData\((.*?)\)',
    r'loader\.require\((.*?)\)',
    r'loader\.lazy\.require\((.*?)\)',
    r'loader\.loadData\((.*?)\)',
    r'loader\.lazy\.loadData\((.*?)\)',
]
importFormats = [
    r'"([^"]+)"',
    r"'([^']+)'",
    r"\[\[(.+)\]\]",
]
def findDependencies(page):
    page = page.replace("Module:", "")

    # Get page from API
    content = requestPage("Module:" + page)

    # Search for all require/loadData calls in the content
    callStrings = []
    for pattern in lineFormats:
        callStrings += re.findall(pattern, content)

    # Match the page names
    pageNames = []
    for match in callStrings:
        for pattern in importFormats:
            pageNames += re.findall(pattern, match)

    # Get additional dependencies
    additional = []
    if page in additionalDependenciesList:
        additional = additionalDependenciesList[page]
    if ("Module:" + page) in additionalDependenciesList:
        additional = additionalDependenciesList["Module:" + page]

    # Return a list with all "Module:" removed, and then with all empty string removed
    return list(filter(lambda s: s.strip() != "", [name.replace("Module:", "") for name in (pageNames + additional)]))

if __name__ == "__main__":
    print(findDependencies("Module:VarsCacheMap"))