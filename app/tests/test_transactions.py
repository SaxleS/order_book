def test_transaction_creation(client):
    response = client.post("/api/v1/users", json={"name": "Adam"})
    assert response.status_code == 200
    adam_id = response.json()["id"]

    response = client.post("/api/v1/users", json={"name": "Alice"})
    assert response.status_code == 200
    alice_id = response.json()["id"]


    sell_order = {
        "user_id": adam_id,
        "stock_name": "Tesla",
        "order_type": "SELL",
        "shares": 100,
        "price_per_share": 170
    }
    response = client.post("/api/v1/orders", json=sell_order)
    assert response.status_code == 200
    sell_order_id = response.json()["id"]


    buy_order = {
        "user_id": alice_id,
        "stock_name": "Tesla",
        "order_type": "BUY",
        "shares": 100,
        "price_per_share": 170
    }
    response = client.post("/api/v1/orders", json=buy_order)
    assert response.status_code == 200
    buy_order_id = response.json()["id"]


    response = client.get("/api/v1/orders")
    assert response.status_code == 200
    orders = response.json()
    print("ORDERS:", orders) 

    response = client.get("/api/v1/transactions")
    assert response.status_code == 200
    transactions = response.json()
    print("TRANSACTIONS:", transactions) 
    assert len(transactions) == 1 



def test_get_transactions(client):
    response = client.get("/api/v1/transactions")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)