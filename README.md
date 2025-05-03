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

### 1. Upload Data to Neo4j

Before performing any similarity operations, you must load the component data into a running Neo4j database.

```bash
python data_upload_to_neo4j.py
```

- This script parses `dummy_component_data.json`, extracts component sizes, and uploads each component to Neo4j.
- Ensure the Neo4j database is running at `bolt://localhost:7687` with the default credentials (`neo4j` / `test12345`), or modify them in the script.

### 2. Prepare Input CSV File

Ensure your input CSV file (e.g., `Input_Nets.csv`) is formatted with the following headers:

```
NetName,ComponentName,Width,Height,PinCount
```

Each row should define a component of a net.

### 3. Run Similarity Search

Once the database is populated, run the similarity search script:

```bash
python knowledge_graph_similarity.py
```

- The script reads the `Input_Nets.csv`, computes similarity scores based on Euclidean distance, and compares them with the data stored in Neo4j.
- Results are saved to `Similar_Nets_Neo4j.csv` automatically.

### 4. Output

After execution, check:

- `Similar_Nets_Neo4j.csv` — contains ranked matches of input nets to existing nets in the graph with similarity scores and component info.

### Notes

- Adjust the Neo4j credentials or file paths as needed in both scripts.
- Make sure your Neo4j server allows remote connections and is accessible if you're not running it locally.
```

