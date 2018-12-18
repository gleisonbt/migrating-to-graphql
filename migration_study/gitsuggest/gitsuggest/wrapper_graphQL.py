import requests
from requests.auth import HTTPBasicAuth

def __run_query(self, query):
        URL = 'https://api.github.com/graphql'

        request = requests.post(URL, json=query,auth=HTTPBasicAuth('gleisonbt', 'Aleister93'))

        if request.status_code == 200:
            return request.json()
        else:
            raise Exception("Query failed to run by returning code of {}. {}".format(request.status_code, query))

def user_get_starred(self, username):
    query = """
        query userGetStarred($username: String!){
            user(login: $username){
                starredRepositories(first:100){
                nodes{
                    nameWithOwner
                    description
                    stargazers{
                    totalCount
                    }
                }
                }
                following(first:100){
                nodes{
                    starredRepositories(first:100){
                        nodes{
                            nameWithOwner
                        description
                        stargazers{
                        totalCount
                        }
                        }
                        }
                }
                }
            }
        }
        """

    json = {
        "query": query, "variables":{
            "username": username
        }
    }

    return __run_query(self, json)

def repos_for_query(self, query):
    query2 = """
            query queryByItems($queryString: String!){
                search(query:$queryString, type:REPOSITORY, first: 100){
                    nodes{
                    ... on Repository{
                        nameWithOwner
                            description
                            stargazers{
                            totalCount
                            }
                        }
                    }
                }
            }
        """

    json = {
        "query": query2, "variables":{
            "queryString": query
        }
    }

    return __run_query(self, json)


