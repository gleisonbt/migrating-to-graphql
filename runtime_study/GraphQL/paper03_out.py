import requests
from json import dump
from json import loads

token = '8d242d19a625e1bc87591a4de6dbf41085284f51' #token aline
dir = '/home/gleison/GraphQLStudy/FilesJson/Paper03_GraphQL'
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

queryJSRepos = """ 
query JSRepos{
  search(query:"stars:0..* language:javascript", type:REPOSITORY, first:100{AFTER}){
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

queryGetIssueOfRepos = """
query getIssueOfRepos($owner:String!, $name:String!){
  repository(owner:$owner, name:$name){
    issues(first:100{AFTER}, states:CLOSED){
      pageInfo{
        hasNextPage
        endCursor
    	}
      nodes{
        number
        body
        title
      }
    }
  }	
}
"""

contCalls = 0


fistQueryJSRepos = queryJSRepos.replace("{AFTER}", "")

json  = {
    "query":fistQueryJSRepos,
    "variables":{}
}


result = run_query(json)

nodesRepo = result['data']['search']['nodes']

contCalls+=1
writeToJSONFile(dir, 'query_repos_'+str(contCalls), result)

next_pageQueryJSRepos = result["data"]["search"]["pageInfo"]["hasNextPage"]

while next_pageQueryJSRepos:
    cursor = result["data"]["search"]["pageInfo"]["endCursor"]
    next_queryQueryJSRepos = queryJSRepos.replace("{AFTER}", ", after: \"%s\"" % cursor)
    json['query'] = next_queryQueryJSRepos
    result = run_query(json)

    nodesRepo += result['data']['search']['nodes']

    contCalls+=1
    writeToJSONFile(dir, 'query_repos_'+str(contCalls), result)
    
    next_pageQueryJSRepos = result["data"]["search"]["pageInfo"]["hasNextPage"]

for repo in nodesRepo:
  nameWithOwner = repo['nameWithOwner'].split('/')

  fistQueryGetIssueOfRepos = queryGetIssueOfRepos.replace("{AFTER}", "")

  json = {
      "query":fistQueryGetIssueOfRepos, "variables":{
        "owner": nameWithOwner[0],
        "name": nameWithOwner[1]
    }
  }

  result =  run_query(json)

  contCalls+=1
  writeToJSONFile(dir, 'query_issues_'+str(contCalls), result)

  next_pageQueryGetIssueOfRepos = result['data']['repository']['issues']['pageInfo']['hasNextPage']

  while next_pageQueryGetIssueOfRepos:
      cursor = result['data']['repository']['issues']['pageInfo']['endCursor']
      
      next_queryGetIssueOfRepos = queryGetIssueOfRepos.replace("{AFTER}", ", after: \"%s\"" % cursor)
      json['query'] = next_queryGetIssueOfRepos
      result = run_query(json)

      contCalls+=1
      writeToJSONFile(dir, 'query_issues_'+str(contCalls), result)

      next_pageQueryGetIssueOfRepos = result['data']['repository']['issues']['pageInfo']['hasNextPage']






###########################################

    # for repo in result['data']['search']['nodes']:
    #     nameWithOwner = repo['nameWithOwner'].split('/')

    #     fistQueryGetIssueOfRepos = queryGetIssueOfRepos.replace("{AFTER}", "")

    #     json = {
    #         "query":fistQueryGetIssueOfRepos, "variables":{
    #             "owner": nameWithOwner[0],
    #             "name": nameWithOwner[1]
    #         }
    #     }

    #     result =  run_query(json)

    #     contCalls+=1
    #     writeToJSONFile(dir, 'query_issues_'+str(contCalls), result)

    #     next_pageQueryGetIssueOfRepos = result['data']['repository']['issues']['pageInfo']['hasNextPage']

    #     while next_pageQueryGetIssueOfRepos:
    #         cursor = result['data']['repository']['issues']['pageInfo']['endCursor']
            
    #         next_queryGetIssueOfRepos = queryGetIssueOfRepos.replace("{AFTER}", ", after: \"%s\"" % cursor)
    #         json['query'] = next_queryGetIssueOfRepos
    #         result = run_query(json)

    #         contCalls+=1
    #         writeToJSONFile(dir, 'query_issues_'+str(contCalls), result)

    #         next_pageQueryGetIssueOfRepos = result['data']['repository']['issues']['pageInfo']['hasNextPage']

    
#################################################
# for repo in result['data']['search']['nodes']:
#     nameWithOwner = repo['nameWithOwner'].split('/')

   
#     fistQueryGetIssueOfRepos = queryGetIssueOfRepos.replace("{AFTER}", "")

#     json = {
#         "query":fistQueryGetIssueOfRepos, "variables":{
#             "owner": nameWithOwner[0],
#             "name": nameWithOwner[1]
#         }
#     }

#     result =  run_query(json)

#     contCalls+=1
#     writeToJSONFile(dir, 'query_issues_'+str(contCalls), result)

#     next_pageQueryGetIssueOfRepos = result['data']['repository']['issues']['pageInfo']['hasNextPage']

#     while next_pageQueryGetIssueOfRepos:
#         cursor = result['data']['repository']['issues']['pageInfo']['endCursor']
    
#         next_queryGetIssueOfRepos = queryGetIssueOfRepos.replace("{AFTER}", ", after: \"%s\"" % cursor)
        
#         json['query'] = next_queryGetIssueOfRepos
#         result = run_query(json)
    
#         contCalls+=1
#         writeToJSONFile(dir, 'query_issues_'+str(contCalls), result)

#         next_pageQueryGetIssueOfRepos = result['data']['repository']['issues']['pageInfo']['hasNextPage']



