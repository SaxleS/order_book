def test_create_order(client):
    response = client.post("/api/v1/users", json={"name": "Adam"})
    assert response.status_code == 200
    user_id = response.json()["id"]
    
    order_data = {
        "user_id": user_id,
        "stock_name": "Tesla",
        "order_type": "SELL",
        "shares": 150,
        "price_per_share": 176
    }
    response = client.post("/api/v1/orders", json=order_data)
    assert response.status_code == 200
    order_id = response.json()["id"]
    

    response = client.get(f"/api/v1/orders/{order_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["user_id"] == user_id
    assert data["stock_name"] == "Tesla"
    assert data["order_type"] == "SELL"

def test_cancel_order(client):

    response = client.post("/api/v1/users", json={"name": "Alice"})
    assert response.status_code == 200
    user_id = response.json()["id"]

    order_data = {
        "user_id": user_id,
        "stock_name": "Tesla",
        "order_type": "SELL",
        "shares": 50,
        "price_per_share": 175
    }
    response = client.post("/api/v1/orders", json=order_data)
    assert response.status_code == 200
    order_id = response.json()["id"]
    

    response = client.delete(f"/api/v1/orders/{order_id}")
    assert response.status_code == 200


    response = client.get(f"/api/v1/orders/{order_id}")
    assert response.status_code == 404