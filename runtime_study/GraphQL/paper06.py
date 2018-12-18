#Paper06
#Extracting Build Changes with BUILDDIFF

import requests
from json import dump
from json import loads

token = '1baee390be22fca3b244974f0ed3b36bf2e8b2ab' #token gleison
dir = '/home/gleison/GraphQLStudy/FilesJson/Paper06_GraphQL'
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
    

querySearchRepos = """
query searchRepos01{
  search(query:"stars:>1000", type:REPOSITORY, first:100{AFTER}){
    pageInfo{
        hasNextPage
        endCursor
    }  
    nodes{
      ... on Repository{
        nameWithOwner
      }
    }
  }
}
"""

queryTotalCountCommitsByRepo = """
query totalCountCommitsByRepo($owner:String!, $name:String!){
  repository(owner:$owner, name:$name){
    ref(qualifiedName:"master"){
          target{
            ... on Commit{
              history{
                totalCount
              }
            }
        }
    }
  }
}
"""

contCalls = 0

fistQuery = querySearchRepos.replace("{AFTER}", "")

json = {
    "query":fistQuery, "variables":{}
}

result = run_query(json)
contCalls+=1
writeToJSONFile(dir, 'query_repos_'+str(contCalls), result)


nodesRepos = result['data']['search']['nodes']

next_page = result['data']['search']['pageInfo']['hasNextPage']
while next_page:
    cursor = result['data']['search']['pageInfo']['endCursor']
    next_query = querySearchRepos.replace("{AFTER}", ", after: \"%s\"" % cursor)

    json['query'] = next_query
    result = run_query(json)
    contCalls+=1
    writeToJSONFile(dir, 'query_repos_'+str(contCalls), result)

    nodesRepos+=result['data']['search']['nodes']

    next_page = result['data']['search']['pageInfo']['hasNextPage']

for repo in nodesRepos:
    nameWithOwner = repo['nameWithOwner'].split('/')

    json = {
        "query":queryTotalCountCommitsByRepo, "variables":{
            "owner":nameWithOwner[0], "name":nameWithOwner[1]
        }
    }

    result = run_query(json)
    contCalls+=1
    writeToJSONFile(dir, 'query_commitCount_'+str(contCalls), result)

