import requests

def run_query(query):
  request = requests.post('http://localhost:5000/graphql?', json=query)
  if request.status_code == 200:
    return request.json()
  else:
    raise Exception("Query failed to run by returning code of {}. {}".format(request.status_code, query))

def find_papers(search_query, start, maxResults):
    query = """
            query findPapers($query: String!, $start: Int!, $maxResults: Int!) {
            entries(searchQuery: $query, start: $start, maxResults: $maxResults, sortBy: "lastUpdatedDate", sortOrder: "descending") {
              id
              title
              updated
              pdfUrl
              arxivPrimaryCategory {
                term
              }
              authors
              arxivUrl
              summary
              tags{
                term
              }
              published
            }
          }
        """

    json = {
        "query": query, "variables":{
            "query": search_query,
            "start": start,
            "maxResults": maxResults
        }
    }


    return run_query(json)["data"]["entries"]
