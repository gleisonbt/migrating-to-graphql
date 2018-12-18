require "graphql/client"
require "graphql/client/http"
require 'json'

module Github
    GITHUB_ACCESS_TOKEN = "bd85101a8de1cbd0088c1506b5a5c49b8eced3d7"
    URL = 'https://api.github.com/graphql'
  
    HttpAdapter = GraphQL::Client::HTTP.new(URL) do
      def headers(context)
        {
          "Authorization" => "Bearer #{GITHUB_ACCESS_TOKEN}",
          "User-Agent" => 'Ruby'
        }
      end
    end
  
    Schema = GraphQL::Client.load_schema(HttpAdapter)
    Client = GraphQL::Client.new(schema: Schema, execute: HttpAdapter)

    class Repository
      RepositoryQuery = Github::Client.parse <<-'GRAPHQL'
        query($owner: String!, $name:String! ){
          repository(owner:$owner, name:$name){
            name
            id
            isFork
            stargazers{
              totalCount
            }
            primaryLanguage{
              name
            }
          }
        }
        GRAPHQL
      
      def self.find(owner, name)
        response = Github::Client.query(RepositoryQuery, variables: { owner: owner, name: name })
            if response.errors.any?
              raise QueryExecutionError.new(response.errors[:data].join(", "))
            else
                response.data.repository
            end
      end
      
    end

    class User
       
      @@type = "User"
      def self.type
        @@type
      end

        TypeProfileQuery = Github::Client.parse <<-'GRAPHQL'
          query($username: String!){
            search(query:$username first:1 type:USER){
              nodes{
                __typename
              }
          }
        }
        GRAPHQL

        UserProfileQuery = Github::Client.parse <<-'GRAPHQL'
          query($username: String!) {
            user(login: $username) {
                id
                login
                websiteUrl
                company
                name
                email
                location
                avatarUrl
            }
          }
        GRAPHQL

        OrganizationProfileQuery = Github::Client.parse <<-'GRAPHQL'
          query($username: String!) {
            organization(login: $username) {
                id
                login
                websiteUrl
                name
                email
                location
                avatarUrl
            }
          }
        GRAPHQL

        ReposOfUserQuery = Github::Client.parse <<-'GRAPHQL'
          query($login:String!){
            user(login:$login){
              repositories(first:100){
                nodes{
                  name
                }
              }
            }
          }
        GRAPHQL

        def self.find_repos_user(login)
          response = Github::Client.query(ReposOfUserQuery, variables: { login: login })
          if response.errors.any?
              raise QueryExecutionError.new(response.errors[:data].join(", "))
          else
              response.data.user.repositories.nodes
          end
        end

        def self.find(username)
            type_response = Github::Client.query(TypeProfileQuery, variables: { username: username })
            if type_response.errors.any?
              raise QueryExecutionError.new(type_response.errors[:data].join(", "))
            else
                type_response.data.search.nodes
            end

            if type_response.data.search.nodes[0].__typename == "User"
                user_response = Github::Client.query(UserProfileQuery, variables: { username: username })
                if user_response.errors.any?
                    raise QueryExecutionError.new(user_response.errors[:data].join(", "))
                else
                    user_response.data.user
                end
            else
                organization_response = Github::Client.query(OrganizationProfileQuery, variables: { username: username })
                if organization_response.errors.any?
                    raise QueryExecutionError.new(organization_response.errors[:data].join(", "))
                else
                    @@type = "Organization"
                    organization_response.data.organization
                end
            end
        end
    end
end


# lol = Github::User.find("gleisonbt")
# puts lol.bio