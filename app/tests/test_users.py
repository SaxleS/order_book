def test_create_user(client):
    response = client.post("/api/v1/users", json={"name": "Adam"})
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert data["name"] == "Adam"



def test_get_user(client): 
    response = client.post("/api/v1/users", json={"name": "Alice"})
    assert response.status_code == 200
    user_id = response.json()["id"]
    
    response = client.get(f"/api/v1/users/{user_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == user_id
    assert data["name"] == "Alice"