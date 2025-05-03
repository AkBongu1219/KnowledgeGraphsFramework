# KnowledgeGraphsFramework(test)

## Project Overview
This project implements a knowledge graph-based system for storing and querying electronic component data, with a focus on finding similar nets across different designs. The application uses Neo4j as the graph database backend and provides tools for:

 - Loading component data into the knowledge graph
 - Performing similarity searches based on component dimensions and pin counts
 - Exporting similarity results for further analysis

## Purpose
The end goal of this system is to help engineers and designers identify similar electronic components or nets across different designs, which can be useful for:

 - Component reuse opportunities
 - Identifying design patterns
 - Knowledge sharing across design teams
 - Standardization of component selections

## Project Structure

```bash
KnowledgeGraphsFramework/
├── knowledge_graph/
│   ├── __pycache__/                         # Python cache files
│   ├── tests/                               # Contains unit or integration tests
         ├── test_data_upload_to_neo4j.py        # Tests data_upload_to_neo4j.py
         ├── test_knowledge_graph_similarity.py  # Tests knowledge_graph_similarity.py                                                     
│   ├── Input_Nets.csv                       # Input data for knowledge graph generation
│   ├── Similar_Nets_Neo4j.csv               # CSV with similarity results or edges for Neo4j
│   ├── data_upload_to_neo4j.py              # Script to upload data into Neo4j
│   ├── dummy_component_data.json            # Dummy component metadata
│   └── knowledge_graph_similarity.py        # Code for calculating graph-based similarities
```
## Method

