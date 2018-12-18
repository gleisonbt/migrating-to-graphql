#Paper07
#Bug Characteristics in Blockchain Systems: A Large-Scale Empirical Study

import requests
from json import dump
from json import loads

token = 'd94956b99a597b2a6d463f653480da82d55c2f16' #token aline
dir = '/home/gleison/GraphQLStudy/FilesJson/Paper07_GraphQL'
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


querySummaryRepo = """
query summaryRepo($owner:String!, $name:String!){
  repository(owner:$owner, name:$name){
    #releases
    tags:refs(refPrefix:"refs/tags/") {
      totalCount
    }
    primaryLanguage {
      name
    }
    stargazers{
      totalCount
    }
  }
}
"""

querySearchIssues = """
query searchIssues($query:String!){
  search(query:$query, type:ISSUE, first:100{AFTER}){
    pageInfo{
        hasNextPage
        endCursor
    }  
    nodes{
    	... on Issue{
        repository{
          nameWithOwner
        }
        title
        body
        createdAt
      }
    }
  }
}
"""

queryGetIssueComment = """
query getIssueComment($query:String!){
  search(type: ISSUE, query:$query , first: 1) {
    nodes {
      ... on Issue {
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

listRepos = ['bitcoin/bitcoin', 'ethereum/go-ethereum', 'ethereum/mist', 'dogecoin/dogecoin',
'ethereum/cpp-ethereum', 'ripple/ripple-lib', 'steemit/steem', 'AugurProject/augur']

contCalls = 0

for repo in listRepos:
    nameWithOwner = repo.split('/')
    json = {
        "query":querySummaryRepo, "variables":{
            "owner": nameWithOwner[0], "name": nameWithOwner[1]
        }
    }

    result = run_query(json)
    contCalls+=1
    writeToJSONFile(dir, 'query_summary_'+str(contCalls), result)

listIssuesNodes = []

for repo in listRepos:

    firstQuery = querySearchIssues.replace("{AFTER}", "")

    json = {
        "query":firstQuery, "variables":{
            "query":"repo:" + repo + " state:closed created:>2016-11-07 label:bug"
        }
    }

    result = run_query(json)

    contCalls+=1
    writeToJSONFile(dir, 'query_issues_'+str(contCalls), result)
    listIssuesNodes+= result['data']['search']['nodes']

    next_page = result['data']['search']['pageInfo']['hasNextPage']
    while next_page:
        cursor = result['data']['search']['pageInfo']['endCursor']

        next_query = querySearchIssues.replace("{AFTER}", ", after: \"%s\"" % cursor)
        json['query'] = next_query

        result = run_query(json)
        contCalls+=1
        writeToJSONFile(dir, 'query_issues_'+str(contCalls), result)
        listIssuesNodes+= result['data']['search']['nodes']

        next_page = result['data']['search']['pageInfo']['hasNextPage']

for issue in listIssuesNodes:
    if len(issue) != 0:
        firstQuery = queryGetIssueComment.replace("{AFTER}", "")
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

        while next_page:
            cursor = result['data']['search']['nodes'][0]['comments']['pageInfo']['endCursor']

            next_query = queryGetIssueComment.replace("{AFTER}", ", after: \"%s\"" % cursor)
            json['query'] = next_query

            result = run_query(json)
            contCalls+=1
            writeToJSONFile(dir, 'query_issueComment_'+str(contCalls), result)
            next_page = result['data']['search']['nodes'][0]['comments']['pageInfo']['hasNextPage']


    

    
