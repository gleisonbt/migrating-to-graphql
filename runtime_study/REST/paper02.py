#Precise condition synthesis for program repair

import requests
import json

token = 'd94956b99a597b2a6d463f653480da82d55c2f16' #token aline
URL = 'https://api.github.com/'
dir = '/home/gleison/GraphQLStudies/FilesJson/Paper02'

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
continueRequests = True

#top 5 C repositories by stars
while continueRequests == True:
    r = restCall('search/repositories?q=stars:0..*+language:java&sort=stars&order=desc&page=1&per_page=5')
    pageObject = r.json()
    continueRequests = r.json()["incomplete_results"]

cont+=1
writeToJSONFile(dir, 'query_'+str(cont), json.loads(r.content))





