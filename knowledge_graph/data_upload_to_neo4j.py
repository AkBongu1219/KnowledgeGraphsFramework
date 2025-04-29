from neo4j import GraphDatabase
import json

# Neo4j configuration
NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "test12345"

# Path to your dummy JSON file
DUMMY_JSON_FILE = "dummy_component_data.json"  # <-- CHANGE THIS to your file path!

# Connect to Neo4j
class KnowledgeGraphUploader:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def insert_data(self, data):
        with self.driver.session() as session:
            for design_name, nets in data.items():
                for net_name, net_details in nets.items():
                    size_string = net_details['TrainingStrings']['Size'].strip()
                    sizes = size_string.split(' ')
                    for size in sizes:
                        if not size.strip():
                            continue  # Skip empty strings

                        try:
                            width, height, pin_count = map(float, size.strip('!').split('!'))
                        except ValueError:
                            print(f"Skipping malformed size: {size}")
                            continue

                        session.run(
                            """
                            MERGE (n:Net {name: $net_name, design: $design_name})
                            CREATE (c:Component {width: $width, height: $height, pin_count: $pin_count})
                            CREATE (n)-[:HAS_COMPONENT]->(c)
                            """,
                            {
                                "net_name": net_name,
                                "design_name": design_name,
                                "width": width,
                                "height": height,
                                "pin_count": pin_count
                            }
                        )
        print("Data upload completed successfully!")

if __name__ == "__main__":
    # Load your dummy JSON data
    try:
        with open(DUMMY_JSON_FILE, 'r') as file:
            dummy_data = json.load(file)
    except Exception as e:
        print(f"Error reading JSON file: {e}")
        exit(1)

    # Upload to Neo4j
    uploader = KnowledgeGraphUploader(NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD)
    uploader.insert_data(dummy_data)
    uploader.close()