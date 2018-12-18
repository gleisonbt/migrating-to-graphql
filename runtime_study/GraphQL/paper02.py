#Precise condition synthesis for program repair

import requests
from json import dump
from json import loads

token = '8d242d19a625e1bc87591a4de6dbf41085284f51' #token aline
dir = '/home/gleison/GraphQLStudy/FilesJson/Paper02_GraphQL'
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


queryRepos = """
query findRepos{
  search(query:"stars:0..* language:java", type:REPOSITORY, first:5){
    nodes{
      ... on Repository{
        nameWithOwner
        url
      }
    }
  }
}
"""

json = {
    "query":queryRepos, "variables":{}
}

result = run_query(json)

cont = 0

writeToJSONFile(dir, 'query_repos'+str(cont), result)


