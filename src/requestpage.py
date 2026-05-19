# -*- coding: utf-8 -*-

# This module is to support `makegraph.py`.

import requests, re, sys

# A common filter rule for pages
# This is based on the wiki's convention
# on testing modules
def validPageFilterRule(page):
    return page.find("Sandbox") < 0 and \
        page.find("sandbox") < 0 and \
        not "doc" in page.split("/") and \
        page.strip() != "" and \
        page.find("%") < 0

# A common name standardization for pages
def standardizeName(name):
    name = name.replace("Module:", "").replace("_", " ").strip()
    return name if len(name) < 1 else name[0].upper() + name[1:]

# Perform get request for the page list for one time
def makePageListRequest(apcontinue, apnamespace):
    payload = {
        "action": "query",
        "format": "json",
        "list": "allpages",
        "apfilterredir": "nonredirects",
        "aplimit": "1000",
        "apcontinue": apcontinue,
        "apnamespace": apnamespace,
        "maxlag": 5,
    }
    try:
        resp = requests.get("https://hypixelskyblock.minecraft.wiki/api.php", params=payload)
        data = resp.json()
        pageList = [page["title"] for page in data["query"]["allpages"]]
    except Exception as e:
        print("Errored in requesting list from page: " + apcontinue)
        print(e)
        print(resp)
        print("Exiting")
        sys.exit()

    return pageList

# Make as many requests as needed to get a list of all pages in namespace
def requestListOfAllPages(namesapceId, namespaceStr = ""):
    apcontinue = ""
    tempList = makePageListRequest("", namesapceId)
    pageList = [] + tempList
    while (len(tempList) > 1):
        apcontinue = tempList[-1].replace(" ", "_").replace(namespaceStr, "")
        tempList = makePageListRequest(apcontinue, namesapceId)
        pageList += tempList
    pageList = [page.replace("Module:", "") for page in set(pageList)]
    pageList.sort()
    return list(filter(validPageFilterRule, pageList))

# Perform get request for a page
# Returns a tuple (content, isMissing)
def makePageContentRequest(page):
    payload = {
        "action": "query",
        "format": "json",
        "prop": "revisions",
        "titles": page.replace(" ", "_"),
        "formatversion": 2,
        "rvprop": "content",
        "rvslots": "*",
        "maxlag": 5,
    }
    try:
        resp = requests.get("https://hypixelskyblock.minecraft.wiki/api.php", params=payload)
        data = resp.json()
        if "missing" in data["query"]["pages"][0]:
            returnedContent = ("", True)
        else:
            returnedContent = (data["query"]["pages"][0]["revisions"][0]["slots"]["main"]["content"], False)
    except Exception as e:
        print("Errored in requesting page: " + page)
        print(e)
        print(data)
        print("Exiting")
        sys.exit()

    return returnedContent

# require(...)
# loader.require(...)
# loader.lazy.require(...)
lineFormats = [
    r'(?<!\.)require\((.*?)\)',
    r'loader\.require\((.*?)\)',
    r'loader\.lazy\.require\((.*?)\)',
]

# mw.loadData(...)
# loader.loadData(...)
# loader.lazy.loadData(...)
dataLineFormats = [
    r'mw\.loadData\((.*?)\)',
    r'loader\.loadData\((.*?)\)',
    r'loader\.lazy\.loadData\((.*?)\)',
]

# "..."
# '...'
# [[...]]
importFormats = [
    r'"([^"]+)"',
    r"'([^']+)'",
    r"\[\[(.+)\]\]",
]

# scan page, return all required modules
# returns a tuple (normal_pages_detected, data_pages_detected, is_external_page)
def findDependencies(page):
    page = page.replace("Module:", "")

    # Get page from API
    content, isMissing = makePageContentRequest("Module:" + page)

    # Search for all require/loadData calls in the content
    callStrings = []
    dataCallStrings = []

    for line in content.split("\n"):
        is_comment = line.strip().startswith("--")
        if is_comment:
            continue

        for pattern in lineFormats:
            callStrings += re.findall(pattern, line)

        for pattern in dataLineFormats:
            dataCallStrings += re.findall(pattern, line)

    # Match the page names
    pageNames = []
    for match in callStrings:
        for pattern in importFormats:
            pageNames += re.findall(pattern, match)

    dataPageNames = []
    for match in dataCallStrings:
        for pattern in importFormats:
            dataPageNames += re.findall(pattern, match)

    # Return a list with all "Module:" removed, and then with all empty string removed
    return (
        list(filter(validPageFilterRule, [standardizeName(name) for name in pageNames])),
        list(filter(validPageFilterRule, [standardizeName(name) for name in dataPageNames])),
        isMissing,
    )

if __name__ == "__main__":
    print(findDependencies("Api/Item/Aliases"))
