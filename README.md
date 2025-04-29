# KnowledgeGraphsFramework(test)

## similarity_search.py
This Python function, find_similar_nets, compares input net components to stored components in a Neo4j graph database to find similar nets based on physical attributes (width, height, pin count). It works as follows:

Queries Neo4j to fetch all components linked to nets (Net) and stores their attributes.

For each component in the input data, it:

Computes Euclidean distance between the input and stored components' attributes.

Converts the distance into a similarity score.

Ranks stored components by similarity for each input net.

Returns a list of results containing the similarity score and matching component details.

## running_knowledge_graph.py
This code defines a Neo4j database interface in Python using the neo4j driver. It creates a class called KnowledgeGraph that handles connecting to and interacting with a Neo4j graph database.

Uses the bolt:// protocol to connect to a local Neo4j instance.

Credentials (neo4j / test12345) are used for authentication.

Class: KnowledgeGraph:

__init__: Initializes the database connection.

close(): Closes the connection to the database.

run_query(): Runs a Cypher query with optional parameters and returns a result cursor.

collect_query_results(): Executes a query and returns all results as a list of dictionaries (record.data()), making it easier to work with the data.
