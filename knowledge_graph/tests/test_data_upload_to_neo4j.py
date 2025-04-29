# knowledge_graph/tests/test_data_upload_to_neo4j.py
import pytest
from neo4j import GraphDatabase
from knowledge_graph.data_upload_to_neo4j import KnowledgeGraphUploader

class DummySession:
    def __init__(self):
        self.runs = []

    def run(self, query, parameters=None):
        self.runs.append((query, parameters))

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

def test_insert_data(monkeypatch):
    dummy_data = {
        "DesignA": {
            "NET1": {"TrainingStrings": {"Size": "100!200!5 malformed 150!250!10!"}}
        }
    }
    session = DummySession()
    driver = DummyDriver(session)

    # Patch GraphDatabase.driver to return our dummy driver
    import knowledge_graph.data_upload_to_neo4j as module
    monkeypatch.setattr(module.GraphDatabase, "driver", lambda uri, auth: driver)

    uploader = KnowledgeGraphUploader("bolt://x", "u", "p")
    uploader.insert_data(dummy_data)

    # Expect two valid inserts (100!200!5 and 150!250!10)
    assert len(session.runs) == 2

    # First call parameters
    _, params1 = session.runs[0]
    assert params1["net_name"] == "NET1"
    assert params1["design_name"] == "DesignA"
    assert params1["width"] == 100.0
    assert params1["height"] == 200.0
    assert params1["pin_count"] == 5.0

    # Second call parameters
    _, params2 = session.runs[1]
    assert params2["width"] == 150.0
    assert params2["height"] == 250.0
    assert params2["pin_count"] == 10.0
