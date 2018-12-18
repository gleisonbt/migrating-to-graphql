import requests
from json import dump
from json import loads

token = '1baee390be22fca3b244974f0ed3b36bf2e8b2ab' #token gleison
dir = '/home/gleison/GraphQLStudies/FilesJson/Paper04_GraphQL'
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
    #number of commits
    ref(qualifiedName:"master"){
      target{
        ... on Commit{
          history{
            totalCount
          }
        }
      }
    }
    #number of branchs
    refs(first: 0, refPrefix: "refs/heads/") {
      totalCount
    }
    #number of bugs
    issues(labels:["defect", "bug", "Bug", "confirmed bug", "11 - Bug	"]){
      totalCount
    }
    #number of releases
    tags:refs(refPrefix:"refs/tags/") {
      totalCount
    }
  }
  #number of devs
  organization(login:$owner){
    members{
      totalCount
    } 
  }
}
"""

queryIssuesByRepo="""
query issuesByRepo($owner:String!, $name:String!){
  repository(owner:$owner, name:$name){
    issues(labels:["defect", "bug", "Bug", "confirmed bug", "11 - Bug	"], states:CLOSED, first:100{AFTER}){
      pageInfo{
        hasNextPage
        endCursor
      }
      totalCount
        nodes{
          title
          body
        }
    	}
  }
}
"""

queryCommentsByIssue="""
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



listRepositories = ['astropy/astropy', 'ipython/ipython', 'matplotlib/matplotlib', 
    'numpy/numpy', 'pandas-dev/pandas', 'scikit-learn/scikit-learn', 'scipy/scipy']

contCalls = 0

for repo in listRepositories:
  nameWithOwner = repo.split('/')
  json  = {
      "query":querySummaryRepo,
      "variables":{
          "owner": nameWithOwner[0],"name": nameWithOwner[1]}
  }

  result = run_query(json)
  
  contCalls+=1
  writeToJSONFile(dir, 'query_summary_'+str(contCalls), result)


for repo in listRepositories:
  nameWithOwner = repo.split('/')
    
  fistQuery = queryIssuesByRepo.replace("{AFTER}", "")

  json = {
      "query":fistQuery, "variables":{
          "owner": nameWithOwner[0],
          "name": nameWithOwner[1]
      }
  }

  result = run_query(json)

  contCalls+=1
  writeToJSONFile(dir, 'query_issues_'+str(contCalls), result)

  nodesIssues = result['data']['repository']['issues']['nodes'] 
  
  next_page = result['data']['repository']['issues']['pageInfo']['hasNextPage']

  while next_page:
    cursor = result['data']['repository']['issues']['pageInfo']['endCursor']
    next_query = queryIssuesByRepo.replace("{AFTER}", ", after: \"%s\"" % cursor)
    json['query'] = next_query

    result = run_query(json)
    contCalls+=1
    writeToJSONFile(dir, 'query_issues_'+str(contCalls), result)

    nodesIssues += result['data']['repository']['issues']['nodes'] 

    next_page = result['data']['repository']['issues']['pageInfo']['hasNextPage']

  for issue in nodesIssues:
    fistQuery = queryCommentsByIssue.replace("{AFTER}", "")

    json = {
      "query":fistQuery,
      "variables": {
        "query":"repo:" + repo + " in:title " + issue['title']
      }
    }

    result = run_query(json)
    contCalls+=1
    writeToJSONFile(dir, 'query_comments_'+str(contCalls), result)

    next_page = False
    
    if len(result['data']['search']['nodes']) ==1 and len(result['data']['search']['nodes'][0]) == 1:
      next_page = result['data']['search']['nodes'][0]['comments']['pageInfo']['hasNextPage']

    while next_page:
      cursor = result['data']['search']['nodes'][0]['comments']['pageInfo']['endCursor']

      next_query = queryCommentsByIssue.replace("{AFTER}", ", after: \"%s\"" % cursor)

      json['query'] = next_query


      result = run_query(json)
      contCalls+=1
      writeToJSONFile(dir, 'query_comments_'+str(contCalls), result)





