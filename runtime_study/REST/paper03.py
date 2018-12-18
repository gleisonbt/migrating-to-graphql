#How do Developers Fix Cross-project Correlated Bugs? A case study on the GitHub scientific Python ecosystem
import requests
import json



token = 'd94956b99a597b2a6d463f653480da82d55c2f16'
URL = 'https://api.github.com/'
dir = '/home/gleison/GraphQLStudies/FilesJson/Paper04'

def writeToJSONFile(path, fileName, data):
    filePathNameWExt =  path + '/' + fileName + '.json'
    with open(filePathNameWExt, 'w') as fp:
        json.dump(data, fp, ensure_ascii=True)


def print_rate_limit(token=token):
    print(json.loads(
        requests.get(URL + 'rate_limit', 
        headers={'Authorization': 'Bearer '+ token}
        ).content)['rate']['remaining'])

def restCall(query, token=token):
    r = requests.get(URL + query, headers={'Authorization': 'Bearer '+ token})
    print(r.status_code)
    return r

cont = 0

def countNumberOfInstances(query, dataType):
    global cont
    r = restCall(query + '&page=1&per_page=100')
    cont += 1
    writeToJSONFile(dir, 'query_' + str(cont) + '_' + dataType + '_first_page_content', json.loads(r.content))
    numberOfPages = 0
    writeToJSONFile(dir, 'query_' + str(cont) + '_' + dataType + '_first_page_headers', json.dumps(r.headers.__dict__))

    if r.status_code == 200 and 'Link' in r.headers: 
        link = r.headers['Link']
        lastURLBegin = link.rfind('<') + 24
        lastURLEnd = link.rfind('>')
        lastURL = link[lastURLBegin:lastURLEnd]
        numberOfPagesIndexBegin = lastURL.find('page=') + 5
        numberOfPagesIndexEnd = lastURL.find('&', numberOfPagesIndexBegin)
        numberOfPages = int(lastURL[numberOfPagesIndexBegin:numberOfPagesIndexEnd])
        r = restCall(lastURL)
        cont += 1
        writeToJSONFile(dir, 'query_' + str(cont) + '_' + dataType + '_last_page_content', json.loads(r.content))

    return numberOfPages*100 + len(r.json()) 

# def restCall2(query):
#     r = requests.get(URL + query, auth=('gleisonbt', 'Aleister93'))
#     print(r.status_code)

#     return r

repoToBugLabel = {'astropy/Astropy': 'Bug','ipython/Ipython': 'bug','matplotlib/Matplotlib': 'confirmed bug','numpy/NumPy': '11 - Bug','pydata/Pandas': 'Bug','scikit-learn/Scikit-learn': 'Bug','scipy/SciPy': 'defect'}
for repo in ['astropy/Astropy','ipython/Ipython','matplotlib/Matplotlib','numpy/NumPy','pydata/Pandas','scikit-learn/Scikit-learn','scipy/SciPy']:
    # TO CHECK: check if will store a JSON file with calculated values, or JSON files for data returned on each request
    #data = '{'
    # get number of contributors
    numberOfCotributors = countNumberOfInstances('repos/' + repo + '/contributors?q=', 'contributors')
    #data += '"numberOfCotributors": ' + str(numberOfCotributors) + ','

    # get number of commits
    numberOfCommits = countNumberOfInstances('repos/' + repo + '/commits?q=', 'commits')
    #data += '"numberOfCommits": ' + str(numberOfCommits) + ','

    # get number of branches
    numberOfBranches = countNumberOfInstances('repos/' + repo + '/branches?q=', 'branches')
    #data += '"numberOfBranches": ' + str(numberOfBranches) + ','

    #get number of releases
    numberOfReleases = countNumberOfInstances('repos/' + repo + '/releases?q=', 'releases')
    #data += '"numberOfReleases": ' + str(numberOfReleases) + ','

    # get number of closed bug issues
    numberOfIssues = countNumberOfInstances('repos/' + repo + '/issues?q=&state=closed&labels=' + repoToBugLabel[repo], 'issues')
    #data += '"numberOfClosedIssues": ' + str(numberOfIssues) + ','

    # get number of devs
    numberOfContributorsFromOrg = countNumberOfInstances('orgs/' + repo[0:repo.find('/')] + '/members?q=', 'members_from_organization')
    #data += '"numberOfDevs": ' + str(numberOfContributorsFromOrg)

    #data += '}'

    #writeToJSONFile(dir, 'query_' + str(cont) + '_repo_'+ repo.replace("/", "_") +'_data', json.loads(data))
    # get data to calculate start date
    r = restCall('repos/' + repo + '/issues?q=&state=closed&labels=' + repoToBugLabel[repo] + '&sort=created&direction=asc&page=1&per_page=1')
    cont += 1
    writeToJSONFile(dir, 'query_' + str(cont) + '_repo_'+ repo.replace("/", "_") +'_start_date', json.loads(r.content))

    # get closed issues for each repository. TO CHECK: will we also request comments for each issue? 
    closedIssuesURL = 'repos/' + repo + '/issues?q=&state=closed&labels=' + repoToBugLabel[repo] + '&sort=created&direction=asc&page=1&per_page=100'
    while True:
        r = restCall(closedIssuesURL)
        cont += 1
        writeToJSONFile(dir, 'query_' + str(cont) + '_repo_'+ repo.replace("/", "_") +'_closed_issues', json.loads(r.content))

        issues = json.loads(r.content)

        for issue in issues: 
            commentsURL = 'repos/' + repo + '/issues/' + str(issue['number']) + '/comments?&page=1&per_page=100'
            while True: 
                r1 = restCall(commentsURL)
                cont += 1 
                writeToJSONFile(dir, 'query_' + str(cont) + '_repo_'+ repo.replace("/", "_") +'_closed_issue_' + str(issue['number']), json.loads(r1.content))

                if r1.status_code == 200 and 'Link' in r1.headers and r1.headers['Link'].find('rel="next"') != -1:
                            link = r1.headers['Link'] 
                            lastPosition = link.find('rel="next"')
                            nextURLBegin = link.rfind('<', 0, lastPosition) + 24
                            nextURLEnd = link.rfind('>', 0, lastPosition)
                            commentsURL = link[nextURLBegin:nextURLEnd]
                else: 
                    break


        if r.status_code == 200 and 'Link' in r.headers and r.headers['Link'].find('rel="next"') != -1:
            link = r.headers['Link'] 
            lastPosition = link.find('rel="next"')
            nextURLBegin = link.rfind('<', 0, lastPosition) + 24
            nextURLEnd = link.rfind('>', 0, lastPosition)
            closedIssuesURL = link[nextURLBegin:nextURLEnd]
        else: 
            break 



