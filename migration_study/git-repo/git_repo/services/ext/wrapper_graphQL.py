import arrow
import requests
from requests.auth import HTTPBasicAuth

def __run_query(self, query):
        URL = 'https://api.github.com/graphql'

        request = requests.post(URL, json=query,auth=HTTPBasicAuth(self.username, self._privatekey))

        if request.status_code == 200:
            return request.json()
        else:
            raise Exception("Query failed to run by returning code of {}. {}".format(request.status_code, query))

def find_user_repos(self, user):
    query = """
            query finfUserRepos($user:String!){
                user(login:$user){
                    repositories(first:100){
                    totalCount
                    nodes{
                        isFork
                        isPrivate
                        object(expression:"master") {
                            ... on Commit {
                                history {
                                totalCount
                                }
                            }
                        }
                        pullRequests{
                        totalCount
                        }
                        issues{
                        totalCount
                        }
                        forks{
                        totalCount
                        }
                        collaborators{
                        totalCount
                        }
                        watchers{
                        totalCount
                        }
                        stargazers{
                        totalCount
                        }
                        primaryLanguage{
                        name
                        }   
                        nameWithOwner
                        updatedAt
                        }
                    }
                }
            }
        """

    json = {
        "query": query, "variables":{
            "user":user
        }
    }

    return __run_query(self, json)

def git_list(self, user_login):
    query = """
        query findGistsByUser($user:String!){
            user(login:$user){
            
            gists(first:100){
            nodes{
                name
                description
            }
            }
        }
        }
        """

    json = {
        "query": query, "variables":{
            "user":user_login
        }
    }

    return __run_query(self, json)

def get_parent_project(self, user, project):
    query = """
            query parentProject($user:String!, $repo:String!){
                repository(owner:$user, name:$repo){
                    parent{
                    name
                    owner{
                        login
                    }
                    }
                }
            }
        """

    json = {
        "query": query, "variables":{
            "user":user, "repo":project
        }
    }

    return __run_query(self, json)

def get_project_default_branch(self, user, name):
    query = """
        query defaultBranch($user:String!, $repo:String!){
            repository(owner:$user, name:$repo){
            defaultBranchRef{
                name
                }
            }
        }
        """

    json = {
        "query": query, "variables":{
            "user":user, "repo":name
        }
    }

    return __run_query(self, json)

def request_list(self, user, repo):
        query = """
         query requestList($user:String!, $repo:String!){
            repository(owner:$user, name:$repo){
                pullRequests(first:100){
                nodes{
                    number
                    title
                    url
                }
                }
            }
        }
        """

        json = {
            "query": query, "variables":{
                "user":user, "repo":repo
            }
        }

        return __run_query(self, json)