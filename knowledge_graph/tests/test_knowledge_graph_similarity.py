# knowledge_graph/tests/test_knowledge_graph_similarity.py
import pytest
import pandas as pd
import numpy as np
from knowledge_graph.knowledge_graph_similarity import load_input_data, find_similar_nets, KnowledgeGraph

class FakeRecord:
    def __init__(self, data):
        self._data = data
    def data(self):
        return self._data

class DummySession:
    def __init__(self, records):
        self._records = records

    def run(self, query):
        return [FakeRecord(r) for r in self._records]

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        pass

class DummyDriver:
    def __init__(self, session):
        self._session = session

    def session(self):
        return self._session

    def close(self):
        pass

def test_load_input_data(tmp_path):
    df = pd.DataFrame({
        "NetName": ["NET1", "NET1", "NET2"],
        "ComponentName": ["C1", "C2", "C3"],
        "Width": [100, 150, 200],
        "Height": [200, 250, 300],
        "PinCount": [5, 10, 15]
    })
    csv_file = tmp_path / "input.csv"
    df.to_csv(csv_file, index=False)

    result = load_input_data(str(csv_file))
    assert result == {
        "NET1": [[100, 200, 5], [150, 250, 10]],
        "NET2": [[200, 300, 15]]
    }

def test_find_similar_nets_identical_and_different():
    input_data = {"NET1": [[100, 200, 5]]}
    stored = [
        {"Net": "NET1", "Design": "D1", "Width": 100.0, "Height": 200.0, "PinCount": 5.0},
        {"Net": "NET2", "Design": "D2", "Width": 0.0,   "Height": 0.0,   "PinCount": 0.0}
    ]

    session = DummySession(stored)
    driver = DummyDriver(session)

    graph = KnowledgeGraph("bolt://x", "u", "p")
    graph.driver = driver  # inject our dummy driver

    results = find_similar_nets(graph, input_data)

    # First result should be the identical match with similarity 1.0
    assert results[0]["MatchedNet"] == "NET1"
    assert pytest.approx(results[0]["SimilarityScore"], rel=1e-4) == 1.0

    # Second result should be the different one with lower similarity
    assert results[1]["MatchedNet"] == "NET2"
    assert results[1]["SimilarityScore"] < 1.0
