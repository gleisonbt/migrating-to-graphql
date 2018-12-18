import requests

from requests.auth import HTTPBasicAuth

import arrow


class Issue:
    def __init__(self, number=None, title=None, comments_count=None, state=None, assignee=None, user=None, created_at=None, repository=None, id=None):
        self.title = title
        self.number = number
        self.comments_count = comments_count
        self.state = state
        self.assignee = assignee
        self.user = user
        self.created_at = created_at
        self.repository = repository
        self.id = id

class Repo:
    def __init__(self, owner=None, name=None, language=None, stargazers_count=None, forks_count=None, updated_at=None, clone_url=None, full_name=None, description=None):
        self.owner = owner
        self.name = name
        self.language = language
        self.stargazers_count = stargazers_count
        self.forks_count = forks_count
        self.updated_at = updated_at
        self.clone_url = clone_url
        self.full_name = full_name
        self.description = description

def __run_query(self, query):
        URL = 'https://api.github.com/graphql'
        #headers = {"Authorization": "Bearer e1a886a63a2e7cb1b3486dbc8a939b79b0be1c6c"}
        headers = {"Authorization": "Bearer "+self.config.user_token}

        request = requests.post(URL, json=query,headers=headers)

        if request.status_code == 200:
            return request.json()
        else:
            raise Exception("Query failed to run by returning code of {}.")

def create_comment(self, user, repo, number, text):
    query = """
            query findIssue($query:String!){
                search(query:$query, type:ISSUE, first:100){
                    nodes{
                    ... on Issue{
                        id
                        number
                        repository{
                        name
                        }
                    }
                    }
                }
            }
        """

    json = {
        "query": query, "variables":{
            "query": "is:issue user:" + user + " repo:" + repo
        }
    }


    result = __run_query(self,json)


    nodes = result["data"]["search"]["nodes"]


    for node in nodes:
        if node["number"] == int(number) and node["repository"]["name"] == repo:
            issue_id = node["id"]

    mutation = """
        mutation addCommentIssue($subjectId:ID!, $body:String!, $clientMutationId:String!){
            addComment(input:{subjectId:$subjectId, body:$body, clientMutationId:$clientMutationId}){
                commentEdge{
                node{
                    body
                }
                }
            }
        }
    """

    json = {
        "query": mutation, "variables":{
            "subjectId": issue_id,
            "body": text,
            "clientMutationId": "1"
        }
    }

    return __run_query(self,json)

def followers_list(self, user, pager=False):
    query = """
            query userFollowers($user:String!){
                user(login: $user){
                    followers(first:100){
                    nodes{
                        login
                    }
                    }
                }
            }
        """

    json = {
        "query": query, "variables":{
            "user": user
        }
    }


    return __run_query(self, json)

def following_list(self, user, pager=False):
    query = """
            query userFollowing($user:String!){
                user(login: $user){
                    following(first:100){
                    nodes{
                        login
                    }
                    }
                }
            }
        """

    json = {
        "query": query, "variables":{
            "user": user
        }
    }


    return __run_query(self,json)

def issues_list(self, issue_filter='subscribed', issue_state='open',
                     limit=1000, pager=False):
    if issue_filter == 'subscribed':
            issue_filter = 'involves'
    elif issue_filter == 'assigned':
        issue_filter = 'assignee'
    elif issue_filter == 'created':
        issue_filter = 'author'
    elif issue_filter == 'mentioned':
        issue_filter = 'mentions'


    query = """
        query FindIssues($query:String!){
            search(query:$query, type:ISSUE, first:100){
            nodes{
            ... on Issue{
                number
                author{
                login
                }
                title
                url
                state
                comments{
                totalCount
                }
                assignees(first:1){
                nodes{
                    login
                }
                }
                createdAt
                repository{
                owner{
                    login
                }
                name
                }
            }
            }
        }
        }
    """

    json = {
        "query": query, "variables":{
        "query": "is:issue is:" + issue_state + " " + issue_filter + ":"+self.config.user_login
        }
    }

    return __run_query(self,json)

def findRepos01(self):
    query1 = """
        query findRepos{
        viewer{
            repositories(first:100){
            nodes{
                nameWithOwner
                pullRequests{
                totalCount
                }
            }
            }
            organizations(first:100){
            nodes{
                repositories(first:100){
                    nodes{
                    nameWithOwner
                    pullRequests{
                    totalCount
                    }
                    }  
                }
            }
            }
        }
        }
        """


    json1 = {
    "query": query1, "variables":{
    }
    }

    return __run_query(self,json1)

def findPullRequests(self, reposWithPRs):
    query2 = """
        query findPullRequests($query:String!){
        search(query:$query, first:100, type:ISSUE){
            nodes{
            ... on PullRequest{
                number
                            author{
                            login
                            }
                            title
                            url
                            state
                            comments{
                            totalCount
                            }
                            assignees(first:1){
                            nodes{
                                login
                            }
                            }
                            createdAt
                            repository{
                            owner{
                                login
                            }
                            name
                            }
            }
            }
        }
        }
        """

    json2 = {}
    issues_list = []

    for repo in reposWithPRs:
        json2 = {
            "query": query2, "variables":{
            "query": "is:pr repo:"+repo
            }
        } 
        result = __run_query(self,json2)
        nodes = result["data"]["search"]["nodes"]

        for node in nodes:
            number = node["number"]
            title = node["title"]
            comments_count = node["comments"]["totalCount"]
            state = node["state"]
            if not node["assignees"]["nodes"]:
                assignee = None
            else:
                assignee = node["assignees"]["nodes"][0]["login"]
            user =  node["author"]["login"]
            created_at = arrow.get(node["createdAt"]).datetime
            repository = (node["repository"]["owner"]["login"],node["repository"]["name"])
            issues_list.append(Issue(number, title, comments_count, state, assignee, user, created_at, repository))

    return issues_list

def findRepos02(self):
    query = """
        query findRepos{
            viewer{
                repositories(first:100){
                nodes{
                    owner{
                    login
                    }
                    name
                    primaryLanguage{
                    name
                    }
                    stargazers{
                    totalCount
                    }
                    forks{
                    totalCount
                    }
                    updatedAt
                    url
                    nameWithOwner
                    description
                }
                }
                organizations(first:100){
                nodes{
                    repositories(first:100){
                        nodes{
                    owner{
                    login
                    }
                    name
                    primaryLanguage{
                    name
                    }
                    stargazers{
                    totalCount
                    }
                    forks{
                    totalCount
                    }
                    updatedAt
                    url
                    nameWithOwner
                    description
                }  
                    }
                }
                }
            }
        }
        """

    json = {
        "query": query, "variables":{
        }    
    }

    return __run_query(self,json)

def findIssues(self, query):
    query1="""
        query searchIssues($query:String!){
            search(query:$query, type:ISSUE, first:100){
                nodes{
                ... on Issue{
                    number
                                author{
                                login
                                }
                                title
                                url
                                state
                                comments{
                                totalCount
                                }
                                assignees(first:1){
                                nodes{
                                    login
                                }
                                }
                                createdAt
                                repository{
                                owner{
                                    login
                                }
                                name
                                }
                }
                }
            }
        }
        """

    json = {
        "query": query1, "variables":{
        "query": query
        }
    }

    return __run_query(self,json)


def findRepos03(self, query, sort):
    query1 = """
        query searchRepositories($query:String!){
            search(query:$query, type:REPOSITORY, first:100){
            nodes{
            ... on Repository{
                owner{
                            login
                            }
                            name
                            primaryLanguage{
                            name
                            }
                            stargazers{
                            totalCount
                            }
                            forks{
                            totalCount
                            }
                            updatedAt
                            url
                            nameWithOwner
                            description
            }
            }
        }
        }
        """

    json = {
        "query": query1, "variables":{
            "query": query+" sort:"+sort
        }    
    }

    return __run_query(self,json)

def findStarred(self):
    query="""
        query starred{
            viewer{
                starredRepositories(first:100){
                    nodes{
                    owner{
                    login
                    }
                    name
                    primaryLanguage{
                    name
                    }
                    stargazers{
                    totalCount
                    }
                    forks{
                    totalCount
                    }
                    updatedAt
                    url
                    nameWithOwner
                    description
                }
                }
            }
        }
        """

    json = {
        "query": query, "variables":{
        }    
    }

    return __run_query(self,json)


def __findSimpleUser(self, user_id):
    queryUser="""
        query findUser($user:String!){
        user(login:$user){
            avatarUrl
            login
            company
            location
            email
            followers{
            totalCount
            }
            following{
            totalCount
            }
            repositories(first:100){
            nodes{
                owner{
                login
                }
                name
                primaryLanguage{
                name
                }
                stargazers{
                totalCount
                }
                forks{
                totalCount
                }
                updatedAt
                url
                nameWithOwner
                description
            }
            }
            organizations(first:100){
            nodes{
                repositories(first:100){
                nodes{
                    owner{
                    login
                    }
                    name
                    primaryLanguage{
                    name
                    }
                    stargazers{
                    totalCount
                    }
                    forks{
                    totalCount
                    }
                    updatedAt
                    url
                    nameWithOwner
                    description
                }
                }
            }
            }
        }
        }
        """
    jsonUser={
        "query":queryUser,"variables":{
            "user": user_id
        } 
    }

    return __run_query(self,jsonUser)

def __findOrganization(self, user_id):
    queryOrgs="""
    query findOrganization($org:String!){
    organization(login:$org){
        avatarUrl
        login
        location
        email
        repositories(first:100){
        nodes{
            owner{
            login
            }
            name
            primaryLanguage{
            name
            }
            stargazers{
            totalCount
            }
            forks{
            totalCount
            }
            updatedAt
            url
            nameWithOwner
            description
        }
        }
    }
    }
    """

    jsonOrgs={
        "query":queryOrgs,"variables":{
            "org": user_id
        } 
    }

    return __run_query(self,jsonOrgs)


def userType(self, user_id):
    queryType="""
        query type($queryUser:String!){
            search(query:$queryUser, type:USER, first:100){
                nodes{
                    ... on Actor{
                    __typename
                }
            }
        }
        }
        """

    jsonType = {
        "query": queryType, "variables":{
        "queryUser": "user:" + user_id
        }
    }

    result =  __run_query(self, jsonType)
    return result["data"]["search"]["nodes"][0]["__typename"]

def findUser(self, user_id):
    
    result = userType(self, user_id)

    if result is None:
        return
    
    actor = {}
    if result == "User":
        resultUser = __findSimpleUser(self, user_id)
        actor = resultUser["data"]["user"]
    else:
        resultUser = __findOrganization(self, user_id)
        actor = resultUser["data"]["organization"]
    
    return actor


