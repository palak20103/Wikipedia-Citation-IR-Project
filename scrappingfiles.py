import re
import requests
import bs4

def getCitationsQuery(currenturl,Query):
    querySplit = re.split(r']|\[', Query)
    CitationsIntData = []
    citationList = []#list of cite no
    queryString = ""#Query
    for term in querySplit:
        if term.isdigit():
            citationList.append(int(term))
        else:
            queryString = queryString+(term.strip())

    #getting all ext cited urls
    res = requests.get(currenturl)
    wiki = bs4.BeautifulSoup(res.text, "lxml")
    citations = wiki.find_all("li", {'id': re.compile(r'^cite_note')})
    # creating citations url dictionary in lines
    citeNo = 1
    i = 0
    lines = {}
    for cite in citations:
        url = []
        for a in cite.find_all('a', href=True):
            if a['href'].startswith('/wiki'):
                links = 'https://en.wikipedia.org' + a['href']
                if len(links.split('/')[0]) < 3:
                    links = 'http:' + links
                url.append(links)
            elif not a['href'].startswith('#'):
                url.append(a['href'])
        lines[citeNo] = url
        citeNo += 1

    #now we have all the citations links ie external citations
    CitationsExtData = []
    for i in citationList:
        flines = {}
        urlofciten = lines[i][0]
        res2 = requests.get(urlofciten)
        urls = []
        if res2 == False:
            print('Exception')
        else:
            wiki = bs4.BeautifulSoup(res2.text, "lxml")
            urls.append(wiki)
            flines[i] = urls
        for k in flines[i]:
            CitationsExtData.extend(['\n'.join([i.getText() for i in k.select('p')])])





    return CitationsExtData, CitationsIntData, queryString
# Query = "The transition from fossil fuels to electric cars features prominently in most climate change mitigation scenarios,[6] such as Project Drawdown's 100 actionable solutions for climate change.[7]"
#
# data1,data2,query = getCitationsQuery("https://en.wikipedia.org/wiki/Car",Query)
# print(data1)
# print(query)