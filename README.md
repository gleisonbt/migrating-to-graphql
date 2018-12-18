# GraphQL: Grey Literature Review

## Selected Articles

#### [A1] GraphQL: A data query language
* Access date: September-2018
* URL: https://code.facebook.com/posts/1691455094417024
* Author: Lee Byron

> Defines a data shape: The first thing you’ll notice is that GraphQL queries mirror their response. This makes it easy to predict the shape of the data returned from a query, as well as to write a query if you know the data your app needs. More important, this makes GraphQL really easy to learn and use. GraphQL is unapologetically driven by the data requirements of products and of the designers and developers who build them.

> Hierarchical: Another important aspect of GraphQL is its hierarchical nature. GraphQL naturally follows relationships between objects, where a RESTful service may require multiple round-trips (resource-intensive on mobile networks) or a complex join statement in SQL. This data hierarchy pairs well with graph-structured data stores and ultimately with the hierarchical user interfaces it’s used within.

> Strongly typed: Each level of a GraphQL query corresponds to a particular type, and each type describes a set of available fields. Similar to SQL, this allows GraphQL to provide descriptive error messages before executing a query.

> Protocol, not storage: Each GraphQL field on the server is backed by any arbitrary function. While we were building GraphQL to support News Feed, we already had a sophisticated feed ranking and storage model, along with existing databases and business logic. GraphQL had to leverage all this existing work to be useful, and so does not dictate or provide any backing storage. Instead, GraphQL takes advantage of your existing code.

> Introspective: A GraphQL server can be queried for the types it supports. This creates a powerful platform for tools and client software to build atop this information like code generation in statically typed languages, our application framework, Relay, or IDEs like GraphiQL (pictured below). GraphiQL helps developers learn and explore an API quickly without grepping the codebase or wrangling with cURL.

> Version free: The shape of the returned data is determined entirely by the client’s query, so servers become simpler and easy to generalize. When you’re adding new product features, additional fields can be added to the server, leaving existing clients unaffected. When you’re sunsetting older features, the corresponding server fields can be deprecated but continue to function. This gradual, backward-compatible process removes the need for an incrementing version number. We still support three years of released Facebook applications on the same version of our GraphQL API.

#### [A2] Living APIs and the Case for GraphQL
* Access date: September-2018
* URL: https://brandur.org/graphql
* Author: Brandur

> The REST model of little insight tends to produce APIs with a strong tendency to ossify, with broad and abrupt changes made intermittently with new versions. GraphQL produces an environment that evolves much more gradually.

> Finally, GraphQL is typed. Types often come in the form of complex objects (e.g., User) or JSON scalars (e.g., int, string), but the type system also supports more sophisticated features like enumerations, interfaces, and union types.

> With GraphQL, fields and relationships must be requested explicitly.

> As its name would suggest, GraphQL models objects as a graph. Technically, the graph starts with a root node that branches into query and mutation nodes, which then descend into API-specific resources.


#### [A3] The GraphQL stack: How everything fits together
* Access date: September-2018
* URL: https://dev-blog.apollodata.com/the-graphql-stack-how-everything-fits-together-35f8bf34f841
* Author: Sashko Stubailo

> Since a GraphQL query is attached to the code that uses it, you can consider that query to be a unit of data fetching. GraphQL knows all of the data requirements for a UI component up front, enabling new types of server functionality.

> The server can provide information as part of the result, just like it provides cache hints, and the gateway can extract and aggregate that information. 

> GraphQL has a well-specified query language, which is a great way to describe data requirements, and a well-defined schema, which exposes API capabilities. 


#### [A4] Why use GraphQL, good and bad reasons
* Access date: September-2018
* URL: https://honest.engineering/posts/why-use-graphql-good-and-bad-reasons
* Authors:  Charly Poly, Bryan Frimim, David Ruyer, and Paul Bonaud

> This is pretty useful when considering mobile applications which have limited bandwidth and speed.

> This will allow you to have a better handling of versioning, maturity levels of your APIs through a decoupled architecture.

> Schema stitching is the process of creating a single GraphQL schema from multiple underlying GraphQL APIs.


#### [A5] GraphQL Introduction
* Access date: September-2028
* URL: https://facebook.github.io/react/blog/2015/05/01/graphql-introduction.html
* Author: Nick Schrock

> Hierarchical: Most product development today involves the creation and manipulation of view hierarchies. To achieve congruence with the structure of these applications, a GraphQL query itself is a hierarchical set of fields. The query is shaped just like the data it returns. It is a natural way for product engineers to describe data requirements.

> Product-centric: GraphQL is unapologetically driven by the requirements of views and the front-end engineers that write them. We start with their way of thinking and requirements and build the language and runtime necessary to enable that. 


> Client-specified queries: In GraphQL, the specification for queries are encoded in the client rather than the server. These queries are specified at field-level granularity. In the vast majority of applications written without GraphQL, the server determines the data returned in its various scripted endpoints. A GraphQL query, on the other hand, returns exactly what a client asks for and no more.

> Backwards Compatible: In a world of deployed native mobile applications with no forced upgrades, backwards compatibility is a challenge. Facebook, for example, releases apps on a two week fixed cycle and pledges to maintain those apps for at least two years. This means there are at a minimum 52 versions of our clients per platform querying our servers at any given time. Client-specified queries simplifies managing our backwards compatibility guarantees.

> Structured, Arbitrary Code: Query languages with field-level granularity have typically queried storage engines directly, such as SQL. GraphQL instead imposes a structure onto a server, and exposes fields that are backed by arbitrary code. This allows for both server-side flexibility and a uniform, powerful API across the entire surface area of an application.

> Application-Layer Protocol: GraphQL is an application-layer protocol and does not require a particular transport. It is a string that is parsed and interpreted by a server.

> Strongly-typed: GraphQL is strongly-typed. Given a query, tooling can ensure that the query is both syntactically correct and valid within the GraphQL type system before execution, i.e. at development time, and the server can make certain guarantees about the shape and nature of the response. This makes it easier to build high quality client tools.

> Introspective: GraphQL is introspective. Clients and tools can query the type system using the GraphQL syntax itself. This is a powerful platform for building tools and client software, such as automatic parsing of incoming data into strongly-typed interfaces. It is especially useful in statically typed languages such as Swift, Objective-C and Java, as it obviates the need for repetitive and error-prone code to shuffle raw, untyped JSON into strongly-typed business objects.

#### [A6] Introduction and Quick Guide to GraphQL for BackEnd and FrontEnd
* Access date: September-2018
* URL: https://time2hack.com/2018/02/introduction-quick-guide-to-graphql-for-backend-frontend/
* Author: Time to Hack

> GraphQL's benefits include
    Typed data
    Get what you asked for
    Multiple data requests in one call
    One endpoint, changes in API are now bit easier
 
#### [A7] You Might Not Need GraphQL
* Access date: September-2018
* URL: https://blog.runscope.com/posts/you-might-not-need-graphql#hn
* Author: Phil Sturgeon

> > That said, Facebook (and others like GitHub) switching from RESTish to GraphQL makes folks consider GraphQL as a replacement for REST. It is not. It is an alternative.   

#### [A8] REST in Peace. Long Live GraphQL
* Access date: September-2018
* URL: https://medium.freecodecamp.org/rest-apis-are-rest-in-peace-apis-long-live-graphql-d412e559d8e4
* Author: Samer Buna

> With GraphQL, you can always fetch all the initial data required by a view with a single round-trip to the server. To do the same with a REST API, we need to introduce unstructured parameters and conditions that are hard to manage and scale.

> With GraphQL, the client speaks a request language which: 1) eliminates the need for the server to hardcode the shape or size of the data, and 2) decouples clients from servers. This means we can maintain and improve clients separately from servers.

> The biggest problem with REST APIs is the nature of multiple endpoints. These require clients to do multiple round-trips to get their data.

> One important threat that GraphQL makes easier is resource exhaustion attacks (AKA Denial of Service attacks). A GraphQL server can be attacked with overly complex queries that will consume all the resources of the server. 

#### [A9] Is GraphQL the Next Frontier for Web APIs?
* Access date: September-2018
* URL: https://brandur.org/api-paradigms
* Author: Brandur

> With GraphQL, developers express the data requirements of their user interfaces using a declarative language. They express what they need, not how to make it available. There is a tight relationship between what data is needed by the UI and the way a developer can express a description of that data in GraphQL .

> It’s great for service operators too, because its explicitness allows them to get a better understanding of exactly what their users are trying to do.

#### [A10] An Introduction to GraphQL via the GitHub API
* Access date: September-2018
* URL: https://blog.codeship.com/an-introduction-to-graphql-via-the-github-api/
* Author: Derek Haynes

> Get exactly what you ask for: Your queries mirror the shape of data returned from a GraphQL API, so there’s no confusion over which fields an API call returns.

> Nesting: Graph queries can be nested, so you can fetch data across relationships. Without GraphQL, gathering data across relationships typically involves multiple, slower, HTTP calls.

> Strongly typed: It’s important to get the data format you expect when working with an external data source. GraphQL is strongly typed, so you get these guarantees.

> Introspective: Since a GraphQL server can be queried for the calls it supports, you can use tools like GraphiQL to organically explore versus hunting through API docs.

> No versioning: Since you get what ask for, fields won’t be added or removed out from under you. When fields are deprecated, they can be marked as such to provide advance warning.

#### [A11] GraphQL Deep Dive: The Cost of Flexibility
* Access date: September-2018
* URL: https://edgecoders.com/graphql-deep-dive-the-cost-of-flexibility-ee50f131a83d#.nr0kzgfk7
* Author: Samer Buna

> One important threat that GraphQL makes easier is resource exhaustion attacks (AKA Denial of Service attacks). A GraphQL server can be attacked with overly complex queries that will consume all the resources of the server. 

> One other task that GraphQL makes a bit more challenging is client data caching. 

#### [A12] GraphQL Didn't Kill REST
* Access date: September-2018
* URL: https://graphqlme.com/2018/04/01/graphql-didnt-kill-rest/
* Author: Matt Engledowl 

> Now don’t get me wrong, the `general` idea of what REST consists of is pretty straightforward, but again, most people are supposedly doing it wrong. In this way, REST is complicated, which means that it is actively killing itself. The reason that GraphQL is gaining such widespread adoption so quickly is because it solves many of the problems that people have experienced with REST, and regardless of whether or not you could “solve them on your own”, the fact is that GraphQL makes this much simpler.

#### [A13] We Need More Best Practices in GraphQL
* Access date: September-2018
* URL: http://graphqlme.com/2017/10/22/best-practices-graphql/
* Author: Matt Engledowl 

> I propose that we as a community start to outline some of these best practices and standards, and compile these somewhere so that they are easy to find. This will allow newcomers to get up to speed more quickly.

#### [A14] GraphQL is the King, R-I-P Rest
* Access date: September-2018
* URL: https://medium.com/@scbarrus/graphql-is-the-king-long-live-the-king-r-i-p-rest-cf04ce38f6c#.y977heueu
* Author: S.C. Barrus

> A query like this returns data in the same shape we requested it in. 

> With GraphQL you can structure your request however you need, including all the data points you require, send it all to a single endpoint (even if you’re calling a third party API) and the server will process all the necessary logic.

> Each field in your schema is enforced by a GraphQL type. This is nice for a number of reasons. My favorite: the IDE let’s you know what data is accepted, so any guesswork there might be is gone (...)

#### [A15] GraphQL in the age of REST APIs
* Access date: September-2018
* URL: https://medium.com/chute-engineering/graphql-in-the-age-of-rest-apis-b10f2bf09bba
* Author: Petr Bela

> Current REST APIs can be exposed to GraphQL clients by building a GraphQL server as a wrapper around the REST API. A client would talk to a GraphQL server which would translate the query to (multiple) REST APIs. Client only sends one request, and receives the smallest possible response it needs.

#### [A16] GraphQL is the new REST
* Access date: September-2018
* URL: https://medium.com/apollo-stack/why-graphql-is-the-future-3bec28193807#.u6spd52ox
* Author: Jonas Helfer

> GraphQL brings order to the chaos:
    Clean API between backends and frontends
    Less communication overhead and fewer meetings
    No more time spent writing API documentation
    No more time spent trying to figure out an API
    Great tooling for your API

#### [A17] Do We Need GraphQL?
* Access date: September-2018
* URL: http://kellysutton.com/2017/01/02/do-we-need-graphql.html
* Author: Kelly Sutton

> The biggest issue I see with GraphQL is that the default implementations disregard HTTP semantics by default.

>  GraphQL’s strength could also be its curse: If the data we request is too specific, it will never be cachable.

#### [A18] GraphQL: 3 reasons not to use it
* Access date: September-2018
* URL: https://blog.hitchhq.com/graphql-3-reasons-not-to-use-it-7715f60cb934
* Author: Bruno Pedro
* 
> Versioning helps deprecating APIs because it gives developers time to upgrade. (...)
By design, GraphQL does not offer versioning. Instead, it lets API providers define certain fields as deprecated. According to its specification, “fields and enum values can indicate whether or not they are deprecated and a description of why it is deprecated”. But how will developers know if their applications need to be rewritten to accommodate the changes?

#### [A19] Is GraphQL the Future?
* Access date: September-2018
* URL: http://artsy.github.io/blog/2018/05/08/is-graphql-the-future/
* Author:  Alan Johnson

>  It lets you model the resources and processes provided by a server as a domain-specific language (DSL). Clients can use it to send scripts written in your DSL to the server to process and respond to as a batch.

>  GraphQL models API operations as fields. How a field works in GraphQL depends on its type, which falls into one of two basic categories.

#### [A20] REST vs. GraphQL APIs, the Good, the Bad, the Ugly
* Access date: September-2018
* URL: https://dev.to/xngwng/rest-vs-graphql-apis-the-good-the-bad-the-ugly-34i8
* Author: Xing Wang

> GraphQL makes it easy to combine multiple APIs into one, so you can implement different parts of your schema as independent services.

> Many of us have seen an API where we first have to GET /user first and then fetch each friend individually viaGET /user/:id/friend/:id endpoint, this can result in N+1 queries and is a well known performance issue in API and database queries. In other words, RESTful API calls are chained on the client before the final representation can be formed for display. GraphQL can reduce this by enabling the server to aggregate the data for the client in a single query.

> GraphQL doesn’t follow the HTTP spec for caching and instead uses a single endpoint. Thus, it’s up to the developer to ensure caching is implemented correctly for non-mutable queries that can be cached. The correct key has to be used for the cache which may include inspecting the body contents.


#### [A21] Understanding RPC, REST and GraphQL
* Access date: September-2018
* URL: https://blog.apisyouwonthate.com/understanding-rpc-rest-and-graphql-2f959aadebe7
* Author: Phil Sturgeon

>  You ask for specific resources and specific fields, and it will return that data in the response.

> The main selling point of GraphQL is that it defaults to providing the very smallest response from an API, as you are requesting only the specific bits of data that you want, which minimizes the Content Download portion of the HTTP request.

#### [A22] The Fullstack Tutorial for GraphQL
* Access date: September-2018
* URL: https://www.howtographql.com/
* Author: Prisma

> GraphQL has its own type system that’s used to define the schema of an API. The syntax for writing schemas is called Schema Definition Language (SDL).

> Instead of having multiple endpoints that return fixed data structures, GraphQL APIs typically only expose a single endpoint. This works because the structure of the data that’s returned is not fixed. Instead, it’s completely flexible and lets the client decide what data is actually needed. 
#### [A23] Interview: GraphQL at Shopify with Evan Huus
* Access date: September-2018
* URL: https://graphqlme.com/2018/01/28/interview-graphql-at-shopify-with-evan-huus/
* Author: Matt Engledowl

>  I think it – there’ve definitely been benefits on the backend. I think it’s kind of a mirror of the benefits that you see on the front end in a lot of ways. The fact that it is strongly typed, that things like nullability are kind of enforced at the schema level has forced us to think about our data models on the server more. I

#### [A24] Beware of Complex Filtering in GraphQL
* Access date: September-2018
* URL: https://graphqlme.com/2018/05/05/beware-of-complex-filtering-in-graphql/
* Author: Matt Engledowl

> Even if you could somehow mitigate these concerns, there’s still the fact that this pushes the complexity and the responsibilities that should be on the server/API down to the client. The client is now responsible for creating these queries, which can quickly become verbose, and it’s no longer clear what the API can do. To me, this is almost as bad as using RESTful architecture to send a string to the server telling it what query to execute like “/posts?where=’user_id = 1 and comment_count > 10′” – maybe not as dangerous, but just as complex and useless for the client.

#### [A25] The GitHub GraphQL API
* Access date: September-2018
* URL: http://githubengineering.com/the-github-graphql-api/
* Authors: Garen Torikian, Brandon Black, Brooks Swinnerton, Charlie Somerville, David Celis, and Kyle Daigle

> You send this via a POST to a server, and the response matches the format of your request.

> You just made one request to fetch all the data you wanted.

> Since our application engineers are using the same GraphQL platform that we’re making available to our integrators, this provides us with the opportunity to ship UI features in conjunction with API access. 

#### [A26] React, Relay and GraphQL: Under the Hood of the Times Website Redesign
* Access date: September-2018
* URL: https://open.nytimes.com/react-relay-and-graphql-under-the-hood-of-the-times-website-redesign-22fb62ea9764
* Author: Scott Taylor

> Products are described in graphs and queries, instead of the REST notion of endpoints.

> A query might be resolved by multiple data sources: REST APIs, database, a flat JSON file. A product might begin by returning data from a simple CSV file, and later be grow to return data from a cluster of databases or remote storage like BigTable.


#### [A27] From REST to GraphQL
* Access date: September-2018
* URL: https://blog.jacobwgillespie.com/from-rest-to-graphql-b4e95e94c26b
* Author: Jacob Gillespie

> GraphQL is more or less a DSL on top of your own backend data fetching logic. It does not connect directly to a database. In fact, the schema you expose over GraphQL will likely not mirror your database exactly. It provides a way to describe a request for structured data, but it is then up to your backend to fulfill that request.

> With GraphQL, developers express the data requirements of their user interfaces using a declarative language. They express what they need, not how to make it available.

#### [A28] GraphQL: A query language for your API
* Access date: September-2018
* URL: http://graphql.github.io
* Author: Facebook Inc

> Strongly typed: Each level of a GraphQL query corresponds to a particular type, and each type describes a set of available fields. Similar to SQL, this allows GraphQL to provide descriptive error messages before executing a query. It also plays well with the strongly typed native environments of Obj-C and Java.

