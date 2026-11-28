NEW = {"passenger_name": "Amine", "origin": "Central", "destination": "Airport"}


def test_create_and_get(client):
    r = client.post("/tickets", json=NEW)
    assert r.status_code == 201
    code = r.json()["code"]
    assert client.get(f"/tickets/{code}").json()["status"] == "ISSUED"


def test_unknown_ticket_is_404(client):
    assert client.get("/tickets/nope").status_code == 404


def test_qr_is_png(client):
    code = client.post("/tickets", json=NEW).json()["code"]
    r = client.get(f"/tickets/{code}/qr")
    assert r.status_code == 200
    assert r.headers["content-type"] == "image/png"


def test_ticket_can_be_used_only_once(client):
    code = client.post("/tickets", json=NEW).json()["code"]
    assert client.post(f"/tickets/{code}/use").status_code == 200
    assert client.post(f"/tickets/{code}/use").status_code == 409


def test_empty_name_is_rejected(client):
    assert client.post("/tickets", json={**NEW, "passenger_name": ""}).status_code == 422
