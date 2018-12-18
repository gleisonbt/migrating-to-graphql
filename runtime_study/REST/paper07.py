#Bug Characteristics in Blockchain Systems: A Large-Scale Empirical Study

import requests
import json



token = 'd94956b99a597b2a6d463f653480da82d55c2f16' #token thais
URL = 'https://api.github.com/'
dir = '/Users/thaismombach/Documents/TESTS_PAPERS/PAPER4_NEW'

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

# def restCall2(query):
#     r = requests.get(URL + query, auth=('gleisonbt', 'Aleister93'))
#     print(r.status_code)

#     return r

repos = listRepos = ['bitcoin/bitcoin', 'ethereum/go-ethereum', 'ethereum/mist', 'dogecoin/dogecoin',
'ethereum/cpp-ethereum', 'ripple/ripple-lib', 'steemit/steem', 'AugurProject/augur']

for repo in repos:
	# Collect number of stars and repo language
    r = restCall('repos/' + repo)
    cont += 1
    writeToJSONFile(dir, 'query_' + str(cont) + '_repo_'+ repo.replace("/", "_") +'_number_stars', json.loads(r.content))

    # Collect number of relases
    r = restCall('repos/' + repo + 'releases?q=&page=1&per_page=100')
    cont += 1
    writeToJSONFile(dir, 'query_' + str(cont) + '_releases_first_page_content', json.loads(r.content))
    numberOfPages = 0
    writeToJSONFile(dir, 'query_' + str(cont) + '_releases_first_page_headers', json.dumps(r.headers.__dict__))

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
        writeToJSONFile(dir, 'query_' + str(cont) + '_releases_last_page_content', json.loads(r.content))

# title, body, date of creation and comments of closed issues with tag bug of the projects in Table I. 
# Issues created after 7-Nov-2016. Also stars, contributors, releases, and language
	# get closed issues for each repository along with its title, body, data of creation and date when it was closed 
    closedIssuesURL = 'repos/' + repo + '/issues?q=labels:bug+state:closed+created:>2016-11-07&page=1&per_page=100'
    while True:
        r = restCall(closedIssuesURL)
        cont += 1
        writeToJSONFile(dir, 'query_' + str(cont) + '_repo_'+ repo.replace("/", "_") +'_closed_issues', json.loads(r.content))

        issues = json.loads(r.content)

        # get comments for each issue
        for issue in issues: 
            commentsURL = 'repos/' + repo + '/issues/' + str(issue['number']) + '/comments?&page=1&per_page=100'
            while True: 
                r1 = restCall(commentsURL)
                cont += 1 
                writeToJSONFile(dir, 'query_' + str(cont) + '_repo_'+ repo.replace("/", "_") +'_closed_issue_' + str(issue['number']) + '_comments', json.loads(r1.content))

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




