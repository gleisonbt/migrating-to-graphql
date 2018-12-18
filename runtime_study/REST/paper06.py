# Extracting Build Changes with BUILDDIFF

import requests
import json

token = 'd94956b99a597b2a6d463f653480da82d55c2f16' #token thais
URL = 'https://api.github.com/'
dir = '/Users/thaismombach/Documents/TESTS_PAPERS/MSR/PAPER3'

def writeToJSONFile(path, fileName, data):
    filePathNameWExt =  path + '/' + fileName + '.json'
    with open(filePathNameWExt, 'w') as fp:
        json.dump(data, fp, ensure_ascii=True)

def print_rate_limit():
    print(json.loads(
        requests.get(URL + 'rate_limit', 
        headers={'Authorization': 'Bearer '+ token}
        ).content)['rate']['remaining'])

def restCall(query, token=token):
    r = requests.get(URL + query, headers={'Authorization': 'Bearer '+ token})
    print(r.status_code)
    return r

# def restCall2(query):
#     r = requests.get(URL + query, auth=('gleisonbt', 'Aleister93'))
#     print(r.status_code)

#     return r

print_rate_limit()

cont = 0
countStars = 1000
 
for pageCount in range(1, 11, 1):
    continueRequests = True
    # get java repos with more than 1000 stars
    while continueRequests == True:
        r = restCall('search/repositories?q=language:java+stars:>=' + str(countStars) + '&page=' + str(pageCount) + '&per_page=100')
        continueRequests = r.json()["incomplete_results"]

    cont+=1
    writeToJSONFile(dir, 'query_' + str(cont) + '_collected_repos', json.loads(r.content))

    # for each project calculate the number of commits
    repos = json.loads(r.content)['items']
    for repo in repos: 
        r = restCall('repos/' + repo['full_name'] + '/commits?q=&page=1&per_page=100')
        cont += 1
        writeToJSONFile(dir, 'query_' + str(cont) + '_commit_first_page_content', json.loads(r.content))
        numberOfPages = 0
        writeToJSONFile(dir, 'query_' + str(cont) + '_commit_first_page_headers', json.dumps(r.headers.__dict__))

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
            writeToJSONFile(dir, 'query_' + str(cont) + '_commit_last_page_content', json.loads(r.content))






