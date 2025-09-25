from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import requests

app = FastAPI()

ELASTIC_SEARCH_URL = 'http://localhost:9200'

class Alert(BaseModel):
    id: str
    severity: str
    message: str
    timestamp: str

@app.get("/api/alerts", response_model=List[Alert])
def get_critical_alerts():
    query = {
        "query": {"range": {"rule.level": {"gte": 10}}},
        "sort": [{"@timestamp": "desc"}],
        "size": 20
    }
    resp = requests.post(f"{ELASTIC_SEARCH_URL}/wazuh-alerts-4.x-*/_search", json=query)
    hits = resp.json().get('hits', {}).get('hits', [])
    alerts = []
    for h in hits:
        source = h["_source"]
        alerts.append(Alert(
            id=h["_id"],
            severity=source.get("rule", {}).get("level", "unknown"),
            message=source.get("rule", {}).get("description", ""),
            timestamp=source.get("@timestamp", "")
        ))
    return alerts
