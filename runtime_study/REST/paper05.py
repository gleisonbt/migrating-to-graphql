# How Open Source Projects use Static Code Analysis Tools in Continuous Integration Pipelines
import requests
import json



token = 'd94956b99a597b2a6d463f653480da82d55c2f16' #token thais
URL = 'https://api.github.com/'
dir = '/Users/thaismombach/Documents/TESTS_PAPERS/MSR/PAPER2'

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

repos = ['ReactiveX/RxJava', 'square/retrofit', 'square/okhttp', 'bumptech/glide', 'square/picasso',
'zxing/zxing', 'square/dagger', 'dropwizard/dropwizard', 'dropwizard/metrics', 'google/auto', 
'roboguice/roboguice', 'checkstyle/checkstyle', 'MorphiaOrg/morphia', 'springfox/springfox', 
'BuildCraft/BuildCraft', 'elastic/elasticsearch-hadoop', 'SpongePowered/SpongeAPI', 'embulk/embulk',
'openMF/mifosx', 'griffon/griffon']

for repo in repos:
    r = restCall('repos/' + repo)
    cont += 1
    writeToJSONFile(dir, 'query_' + str(cont) + '_repo_'+ repo.replace("/", "_") +'_number_stars', json.loads(r.content))




