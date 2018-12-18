#Decoding the representation of code in the brain: an fMRI study of code review and expertise

import requests
from json import dump
from json import loads
import time

token = '70bcf707863eddb862f10283cc3937467b442ca3' #token gleison
dir = '/home/gleison/GraphQLStudy/FilesJson/Paper01_GraphQL'
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
        raise Exception("Query failed to run by returning code of {}. {}. {}".format(request.status_code, json['query'], json['variables']))


queryRepos = """
query searchRepos{
  search(query:"stars:0..* language:c", type: REPOSITORY,first:100){
    nodes{
      ... on Repository{
        nameWithOwner
      }
    }
  }
}
"""

queryPullsByRepo = """
query pullsByRepos($owner: String!, $name: String!){
  repository(owner:$owner, name:$name){
    pullRequests(first:100{AFTER}, orderBy:{field:CREATED_AT, direction:DESC}){
            pageInfo{
                hasNextPage
                endCursor
            }    
          nodes{
            repository{
              nameWithOwner
            }
            title
            number
            changedFiles
          }
        }
  }
}
"""

queryGetPullComment = """
query getPullComment($query:String!){
  search(type: ISSUE, query:$query , first: 1) {
    nodes {
      ... on PullRequest {
        comments(first:100{AFTER}){
              pageInfo{
                hasNextPage
                endCursor
              }
              nodes{
                bodyText
              }
          }
      }
    }
  }
}
"""



contCalls = 0

json = {
    "query":queryRepos, "variables":{}
}

result = run_query(json)

contCalls+=1
writeToJSONFile(dir, 'query_repos_'+str(contCalls), result)

listIssuesNodes = []


def commentsPulls(issue):
  global contCalls
  if len(issue) != 0:
        firstQuery = queryGetPullComment.replace("{AFTER}", "")
        print(issue['repository']['nameWithOwner'])

        json = {
            "query":firstQuery,
            "variables": {
                "query":"repo:" + issue['repository']['nameWithOwner'] + " in:title " + issue['title']
            }
        }

        result = run_query(json)

        contCalls+=1
        writeToJSONFile(dir, 'query_issueComment_'+str(contCalls), result)

        next_page = False

        if  len(result['data']['search']['nodes']) ==1 and len(result['data']['search']['nodes'][0]) == 1:
            next_page = result['data']['search']['nodes'][0]['comments']['pageInfo']['hasNextPage']

        #next_page = result['data']['search']['nodes'][0]['comments']['pageInfo']['hasNextPage']
        print("cont call2")
        print(contCalls)
        while next_page:
            cursor = result['data']['search']['nodes'][0]['comments']['pageInfo']['endCursor']

            next_query = queryGetPullComment.replace("{AFTER}", ", after: \"%s\"" % cursor)
            json['query'] = next_query

            result = run_query(json)
            contCalls+=1
            writeToJSONFile(dir, 'query_issueComment_'+str(contCalls), result)
            next_page = result['data']['search']['nodes'][0]['comments']['pageInfo']['hasNextPage']





for repo in result['data']['search']['nodes']:
    nameWithOwner = repo['nameWithOwner'].split('/')

    first_query = queryPullsByRepo.replace("{AFTER}", "")
    json = {
      "query":first_query,
      "variables":{
        "owner": nameWithOwner[0], "name": nameWithOwner[1]
      }
    }

    result = run_query(json)
    contCalls+=1
    writeToJSONFile(dir, 'query_pulls_'+str(contCalls), result)

    listIssuesNodes+=result['data']['repository']['pullRequests']['nodes']

    print("cont call")
    print(contCalls)
    for issue in result['data']['repository']['pullRequests']['nodes']:
      commentsPulls(issue)

    next_pagePull = result["data"]["repository"]["pullRequests"]["pageInfo"]["hasNextPage"]

    while next_pagePull:
      cursor = result["data"]["repository"]["pullRequests"]["pageInfo"]["endCursor"]

      next_query = queryPullsByRepo.replace("{AFTER}", ", after: \"%s\"" % cursor)

      json['query'] = next_query
      result = run_query(json)
      contCalls+=1
      writeToJSONFile(dir, 'query_pulls_'+str(contCalls), result)
      
      listIssuesNodes+=result['data']['repository']['pullRequests']['nodes']

      for issue in result['data']['repository']['pullRequests']['nodes']:
        commentsPulls(issue)

      next_pagePull = result["data"]["repository"]["pullRequests"]["pageInfo"]["hasNextPage"]

      




# for issue in listIssuesNodes:
#     if len(issue) != 0:
#         firstQuery = queryGetPullComment.replace("{AFTER}", "")
#         print(issue['repository']['nameWithOwner'])

#         json = {
#             "query":firstQuery,
#             "variables": {
#                 "query":"repo:" + issue['repository']['nameWithOwner'] + " in:title " + issue['title']
#             }
#         }

#         result = run_query(json)

#         contCalls+=1
#         writeToJSONFile(dir, 'query_issueComment_'+str(contCalls), result)

#         next_page = False

#         if  len(result['data']['search']['nodes']) ==1 and len(result['data']['search']['nodes'][0]) == 1:
#             next_page = result['data']['search']['nodes'][0]['comments']['pageInfo']['hasNextPage']

#         #next_page = result['data']['search']['nodes'][0]['comments']['pageInfo']['hasNextPage']

#         while next_page:
#             cursor = result['data']['search']['nodes'][0]['comments']['pageInfo']['endCursor']

#             next_query = queryGetPullComment.replace("{AFTER}", ", after: \"%s\"" % cursor)
#             json['query'] = next_query

#             result = run_query(json)
#             contCalls+=1
#             writeToJSONFile(dir, 'query_issueComment_'+str(contCalls), result)
#             next_page = result['data']['search']['nodes'][0]['comments']['pageInfo']['hasNextPage']