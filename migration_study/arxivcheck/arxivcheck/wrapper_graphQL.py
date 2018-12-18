import requests

def run_query(query):
    request = requests.post('http://localhost:5000/graphql?', json=query)
    if request.status_code == 200:
        return request.json()
    else:
        return None

def arxiv_info(value, field):
    if field == "id":
        prefix_query = """
            query arxiv($identifier:ID!){
            entry(id:$identifier){
        """
    else:
        prefix_query = """
            query arxiv($identifier:String!){
            entries(searchQuery:$identifier, start:0, maxResults:100, sortBy: "relevance", sortOrder: "descending"){
        """

    query = prefix_query + """
            doi
            pdfUrl
            title
            authors
            published
            id
        }
        }
    """

    json = {
        "query":query, "variables":{
            "identifier":value
        }
    }

    return run_query(json)
