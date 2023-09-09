from fastapi.testclient import TestClient
from app.config import settings
from app.main import app

client = TestClient(app)


def test_slack_event_challange():
    response = client.post(
        "/slack_events", json={
            "token": settings.slack_event_token,
            "challenge": "challangeString",
            "type": "url_verification"
        }
    )
    assert response.status_code == 200
    assert response.json() == {
        "challenge": "challangeString"
    }


def test_slack_event():
    response = client.post(
        "/slack_events",
        json={
            "token": settings.slack_event_token,
            "type": 'event_callback',
            "challenge": "challangeString",
            "event": {
                "type": 'test',
                'channel': 'channelName',
                'user': "userName",
                'text': 'Hello! How can I assist you today?',
                'event_ts': '1694257793.719319'
            }
        }
    )
    assert response.status_code == 200
    assert response.json() == {"message": "Event received"}
