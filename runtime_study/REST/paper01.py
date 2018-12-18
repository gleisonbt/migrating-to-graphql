#Decoding the representation of code in the brain: an fMRI study of code review and expertise
import requests
import json



token = 'd94956b99a597b2a6d463f653480da82d55c2f16' #token aline
URL = 'https://api.github.com/'
dir = '/Users/thaismombach/Documents/TESTS_PAPERS/PAPER1'

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


cont = 0
continueRequests = True
#pega lista de pull requests
while continueRequests == True:
    r = restCall('search/repositories?q=stars:0..*+language:c&sort=stars&order=desc&page=1&per_page=100')
    pageObject = r.json()
    continueRequests = r.json()["incomplete_results"]
    print(continueRequests)

cont+=1
writeToJSONFile(dir, 'query_' + str(cont) + '_selected_repos', json.loads(r.content))

repoItems = json.loads(r.text or r.content)['items']

for repo in repoItems:
    #pega os numeros das 1,000 pulls mais recentes para cada repo
    for page in range(1, 10, 1):
        r = restCall('repos/' + repo['full_name'] + '/pulls?&state=all&sort=created&direction=desc&page=' + str(page) + '&per_page=100')
        cont+=1
        writeToJSONFile(dir, 'query_' + str(cont) + '_numPulls', json.loads(r.content))

        pullItems = json.loads(r.content)
        for pull in pullItems:
            numberPull = pull['number']

            #pega o numero de arquivos modificados, linhas modificadas (adicionadas e removidas) e comentarios
            r2 = restCall('repos/' + repo['full_name'] + '/pulls/' + str(numberPull))
            cont+=1
            writeToJSONFile(dir, 'query_' + str(cont) + '_pull_' + str(numberPull) + '_data', json.loads(r2.content))

            #pega os comentarios
            #r3 = restCall('repos/'+repo['full_name']+'/pulls/'+str(numberPull)+'/comments')
            #cont+=1
            #writeToJSONFile(dir, 'query_'+str(cont)+'_comments', json.loads(r3.content))
            #print('query_comments_'+str(cont))
        if len(pullItems) < 100: 
            break



