from neo4j import GraphDatabase
import pandas as pd
import numpy as np
from scipy.spatial.distance import euclidean

# Neo4j configuration
NEO4J_URI = "bolt://localhost:7687"  # Ensure Neo4j is running
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "test12345"

# connect to Neo4j
class KnowledgeGraph:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def run_query(self, query, parameters=None):
        with self.driver.session() as session:
            return session.run(query, parameters)
           
    def collect_query_results(self, query, parameters=None):
        results = []
        with self.driver.session() as session:
            result = session.run(query, parameters)
            # Properly collect all records
            results = [record.data() for record in result]
        return results

# Load input
def load_input_data(csv_file):
    try:
        input_data = pd.read_csv(csv_file)
        print("Loaded CSV Data Successfully!")

        # Ensure correct column names
        expected_columns = ["NetName", "ComponentName", "Width", "Height", "PinCount"]
        missing_cols = [col for col in expected_columns if col not in input_data.columns]

        if missing_cols:
            raise ValueError(f"Missing columns in CSV: {missing_cols}")

        net_dict = {}
        for _, row in input_data.iterrows():
            net_name = row["NetName"]
            component_data = [row["Width"], row["Height"], row["PinCount"]]

            if net_name not in net_dict:
                net_dict[net_name] = []
            net_dict[net_name].append(component_data)

        return net_dict

    except Exception as e:
        print(f"Error loading input CSV: {e}")
        return {}

# Peform similarity search
def find_similar_nets(graph, input_data):
    results = []

    # Fetch all stored components once (Optimized Query)
    query = """
    MATCH (n:Net)-[:HAS_COMPONENT]->(c:Component)
    RETURN n.name AS Net, n.design AS Design,
           c.width AS Width, c.height AS Height, c.pin_count AS PinCount
    """
    stored_components = []
    with graph.driver.session() as session:
        result = session.run(query)
        # Collect all records
        stored_components = [record.data() for record in result]
   
    print(f"Fetched {len(stored_components)} components from Neo4j!")

    for net_name, components in input_data.items():
        print(f"Processing input net: {net_name}")

        for width, height, pin_count in components:
            net_scores = []

            for stored in stored_components:
                stored_vector = np.array([stored["Width"], stored["Height"], stored["PinCount"]])
                input_vector = np.array([width, height, pin_count])
                distance = euclidean(stored_vector, input_vector)
                similarity = 1 / (1 + distance)  # Convert to similarity score

                net_scores.append({
                    "InputNet": net_name,
                    "MatchedNet": stored["Net"],
                    "Design": stored["Design"],
                    "SimilarityScore": round(similarity, 4),
                    "Width": stored["Width"],
                    "Height": stored["Height"],
                    "PinCount": stored["PinCount"]
                })

            # Sort by similarity score in descending order
            net_scores.sort(key=lambda x: x["SimilarityScore"], reverse=True)
            results.extend(net_scores)

    print("Similarity search completed!")
    return results

# Save outputs in CSV
def save_results_to_csv(results, output_file="Similar_Nets_Neo4j.csv"):
    df = pd.DataFrame(results)
    df.to_csv(output_file, index=False)
    print(f"\n Results saved to {output_file}")

if __name__ == "__main__":
    input_csv = "Input_Nets.csv"

    # Initialize Neo4j Knowledge Graph
    graph = KnowledgeGraph(NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD)

    # Step 1: Load input CSV
    input_data = load_input_data(input_csv)

    # Step 2: Perform similarity search
    similar_nets = find_similar_nets(graph, input_data)

    # Step 3: Save results
    save_results_to_csv(similar_nets)

    # Close Neo4j connection
    graph.close()