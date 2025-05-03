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

## Project Structure
# KnowledgeGraphsFramework

A framework to work with and evaluate knowledge graphs, particularly using Neo4j.

## Repository Structure
```bash
KnowledgeGraphsFramework/
├── knowledge_graph/
│   ├── __pycache__/                         # Python cache files
│   ├── tests/                               # Contains unit or integration tests
│   ├── .DS_Store                            # macOS system file (should be gitignored)
│   ├── Input_Nets.csv                       # Input data for knowledge graph generation
│   ├── Similar_Nets_Neo4j.csv               # CSV with similarity results or edges for Neo4j
│   ├── data_upload_to_neo4j.py              # Script to upload data into Neo4j
│   ├── dummy_component_data.json            # Dummy component metadata
│   └── knowledge_graph_similarity.py        # Code for calculating graph-based similarities
```

