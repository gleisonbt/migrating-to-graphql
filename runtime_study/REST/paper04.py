# Exception Evolution in Long-lived Java Systems

import requests
import json

token = 'd94956b99a597b2a6d463f653480da82d55c2f16' #token thais
URL = 'https://api.github.com/'
dir = '/Users/thaismombach/Documents/TESTS_PAPERS/MSR/PAPER1'

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
countStars = 10

for pageCount in range(1, 11, 1):
    continueRequests = True
    while continueRequests == True:
        r = restCall('search/repositories?q=created:<2012-01-01+pushed:>=2016-07-01+stars:>' + str(countStars) + '+size:>1000&page=' + str(pageCount) + '&per_page=100')
        pageObject = r.json()
        continueRequests = pageObject["incomplete_results"]

    cont+=1
    writeToJSONFile(dir, 'query_' + str(cont) + '_collected_repos', json.loads(r.content))





