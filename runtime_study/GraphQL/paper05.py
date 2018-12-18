#Paper05
#How Open Source Projects use 
#Static Code Analysis Tools in Continuous Integration Pipelines

import requests
from json import dump
from json import loads

token = '1baee390be22fca3b244974f0ed3b36bf2e8b2ab' #token gleison
dir = '/home/gleison/GraphQLStudy/FilesJson/Paper05_GraphQL'
headers = {"Authorization": "Bearer " + token} 

def writeToJSONFile(path, fileName, data):
    filePathNameWExt =  path + '/' + fileName + '.json'
    with open(filePathNameWExt, 'w') as fp:
        dump(data, fp, ensure_ascii=True)


def run_query(json): # A simple function to use requests.post to make the API call. Note the json= section.
    request = requests.post('https://api.github.com/graphql', json=json, headers=headers)
    if request.status_code == 200:
        return request.json()
    else:
        raise Exception("Query failed to run by returning code of {}. {}".format(request.status_code, json['query']))


queryNumStars = """
query numStars($owner:String!, $name:String!){
  repository(owner:$owner, name:$name){
    stargazers{
      totalCount
    }
  }
}
"""

listRepos = ['ReactiveX/RxJava', 'square/retrofit', 'square/okhttp', 'bumptech/glide', 'square/picasso',
'zxing/zxing', 'square/dagger', 'dropwizard/dropwizard', 'dropwizard/metrics', 'google/auto', 
'roboguice/roboguice', 'checkstyle/checkstyle', 'MorphiaOrg/morphia', 'springfox/springfox', 
'BuildCraft/BuildCraft', 'elastic/elasticsearch-hadoop', 'SpongePowered/SpongeAPI', 'embulk/embulk',
'openMF/mifosx', 'griffon/griffon']

contCalls = 0

for repo in listRepos:
    nameWithOwner = repo.split('/')

    json = {
        "query":queryNumStars, "variables":{
            "owner":nameWithOwner[0], "name":nameWithOwner[1]
        }
    }

    result = run_query(json)

    contCalls+=1
    writeToJSONFile(dir, 'query_stars_'+str(contCalls), result)