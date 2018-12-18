#To type or not to type: quantifying detectable bugs in JavaScript

import requests
import json

# token = 'd94956b99a597b2a6d463f653480da82d55c2f16'
# URL = 'https://api.github.com/'
# dir = '/home/gleison/GraphQLStudies/FilesJson/Paper01'

token = 'd94956b99a597b2a6d463f653480da82d55c2f16' #token aline
URL = 'https://api.github.com/'
dir = '/Users/thaismombach/Documents/TESTS_PAPERS/PAPER3'

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

# def restCall2(query):
#     r = requests.get(URL + query, auth=('gleisonbt', 'Aleister93'))
#     print(r.status_code)

#     return r

print_rate_limit()

#all js repos
contRepos = 2

cont = 1

for contRepos in range(1, 10, 1):
    print('page: ' + str(contRepos))
    continueRequests = True

    #top 100 JavaScript repositories
    while continueRequests == True:
        r1 = restCall('search/repositories?q=stars:0..*+language:javascript&sort=stars&order=desc&page='+str(contRepos)+'&per_page=100')
        pageObject = r1.json()
        continueRequests = r1.json()["incomplete_results"]

    writeToJSONFile(dir, 'query_'+str(cont)+'_repo', json.loads(r1.content or r1.text))

    itemsRepo = json.loads(r1.content)['items']

    for repo in itemsRepo:

        closedIssuesURL = 'repos/'+repo['full_name']+'/issues?state=closed&page=1&per_page=100'
        hasNextPage = True
        while hasNextPage:
            hasNextPage = False
            r2 = restCall(closedIssuesURL)
            cont += 1
            writeToJSONFile(dir, 'query_' + str(cont) + '_repo_'+ repo['full_name'].replace("/", "_") +'_closed_issues', json.loads(r2.content))

            if r2.status_code == 200: 
                if 'Link' in r2.headers and r2.headers['Link'].find('rel="next"') != -1:
                        link = r2.headers['Link'] 
                        lastPosition = link.find('rel="next"')
                        nextURLBegin = link.rfind('<', 0, lastPosition) + 24
                        nextURLEnd = link.rfind('>', 0, lastPosition)
                        closedIssuesURL = link[nextURLBegin:nextURLEnd]
                        hasNextPage = True

        #r2 = restCall('repos/'+repo['full_name']+'/issues?state=closed')
        #writeToJSONFile(dir, 'query_'+str(cont)+'_issue', json.loads(r2.content))

        commitsURL = 'repos/'+repo['full_name']+'/commits?&page=1&per_page=100'
        hasNextPage = True
        while hasNextPage:
            hasNextPage = False
            r3 = restCall(commitsURL)
            cont += 1

            if r3.status_code == 200: 
                writeToJSONFile(dir, 'query_' + str(cont) + '_repo_'+ repo['full_name'].replace("/", "_") +'_commits', json.loads(r3.content))
                itemsCommit  = json.loads(r3.content)
                for commit in itemsCommit:
                    r4 = restCall('repos/'+repo['full_name']+'/commits/'+commit['sha'])
                    cont += 1
                    writeToJSONFile(dir, 'query_'+str(cont)+'_commitItem', json.loads(r4.content))

                if 'Link' in r3.headers and r3.headers['Link'].find('rel="next"') != -1:
                        link = r3.headers['Link'] 
                        lastPosition = link.find('rel="next"')
                        nextURLBegin = link.rfind('<', 0, lastPosition) + 24
                        nextURLEnd = link.rfind('>', 0, lastPosition)
                        commitsURL = link[nextURLBegin:nextURLEnd]
                        hasNextPage = True

        #r3 = restCall('repos/'+repo['full_name']+'/commits')
        #writeToJSONFile(dir, 'query_'+str(cont)+'_commits', json.loads(r3.content))

    # while len(json.loads(r.content)['items']) == 100 and contRepos <= 10:    
    #     contRepos+=1
    #     cont+=1
    #     print(cont)
    #     r = restCall('search/repositories?q=stars:0..*+language:javascript&sort=stars&order=desc&page='+str(contRepos)+'&per_page=100')
    #     writeToJSONFile(dir, 'query_'+str(cont)+'_repo', json.loads(r.content))

    #     itemsRepo = json.loads(r.content)['items']
    #     for repo in itemsRepo:
    #         cont+=1
    #         r2 = restCall('repos/'+repo['full_name']+'/issues?state=closed') #adicionar paginação
    #         writeToJSONFile(dir, 'query_'+str(cont)+'_issue', json.loads(r2.content))


    #         cont+=1
    #         r3 = restCall('repos/'+repo['full_name']+'/commits') #adicionar paginação
    #         writeToJSONFile(dir, 'query_'+str(cont)+'_commits', json.loads(r3.content))

    #         itemsCommit  = json.loads(r3.content)
    #         for commit in itemsCommit:
    #             r4 = restCall('repos/'+repo['full_name']+'/commits/'+commit['sha'])
    #             writeToJSONFile(dir, 'query_'+str(cont)+'_commitItem', json.loads(r4.content))











