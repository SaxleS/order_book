# Тест частичного исполнения ордера
def test_partial_order_execution(client):
    response = client.post("/api/v1/users", json={"name": "Adam"})
    assert response.status_code == 200
    adam_id = response.json()["id"]

    sell_order = {
        "user_id": adam_id,
        "stock_name": "Tesla",
        "order_type": "SELL",
        "shares": 150,
        "price_per_share": 176
    }
    client.post("/api/v1/orders", json=sell_order)


    response = client.post("/api/v1/users", json={"name": "Alice"})
    assert response.status_code == 200
    alice_id = response.json()["id"]

    buy_order = {
        "user_id": alice_id,
        "stock_name": "Tesla",
        "order_type": "BUY",
        "shares": 100,
        "price_per_share": 176
    }
    client.post("/api/v1/orders", json=buy_order)


    response = client.get("/api/v1/transactions")
    transactions = response.json()
    assert len(transactions) == 1
    assert transactions[0]["shares"] == 100


    response = client.get("/api/v1/orders")
    orders = response.json()
    print("ORDERS AFTER TRANSACTION:", orders)

    remaining_order = next(order for order in orders if order["user_id"] == adam_id)
    assert remaining_order["shares"] == 50

# Тест приоритета исполнения ордеров по времени создания
def test_order_priority_by_timestamp(client):

    response = client.post("/api/v1/users", json={"name": "Bob"})
    assert response.status_code == 200
    bob_id = response.json()["id"]

    sell_order_bob = {
        "user_id": bob_id,
        "stock_name": "Tesla",
        "order_type": "SELL",
        "shares": 50,
        "price_per_share": 175
    }
    client.post("/api/v1/orders", json=sell_order_bob)

    response = client.post("/api/v1/users", json={"name": "Charlie"})
    assert response.status_code == 200
    charlie_id = response.json()["id"]

    sell_order_charlie = {
        "user_id": charlie_id,
        "stock_name": "Tesla",
        "order_type": "SELL",
        "shares": 50,
        "price_per_share": 175
    }
    client.post("/api/v1/orders", json=sell_order_charlie)


    response = client.post("/api/v1/users", json={"name": "Julia"})
    assert response.status_code == 200
    julia_id = response.json()["id"]

    buy_order = {
        "user_id": julia_id,
        "stock_name": "Tesla",
        "order_type": "BUY",
        "shares": 70,
        "price_per_share": 175
    }
    client.post("/api/v1/orders", json=buy_order)


    response = client.get("/api/v1/transactions")
    transactions = response.json()
    
    assert len(transactions) == 2  # Ожидаем две транзакции
    assert transactions[0]["seller_id"] == bob_id
    assert transactions[0]["shares"] == 50  # Полностью выполнен первый ордер
    assert transactions[1]["seller_id"] == charlie_id
    assert transactions[1]["shares"] == 20  # Частично выполнен второй ордер

# Тест сортировки списка ордеров по цене и времени создания
def test_order_sorting(client):

    response = client.post("/api/v1/users", json={"name": "Eve"})
    eve_id = response.json()["id"]

    order1 = {
        "user_id": eve_id,
        "stock_name": "Tesla",
        "order_type": "SELL",
        "shares": 30,
        "price_per_share": 180
    }
    client.post("/api/v1/orders", json=order1)

    order2 = {
        "user_id": eve_id,
        "stock_name": "Tesla",
        "order_type": "SELL",
        "shares": 50,
        "price_per_share": 175
    }
    client.post("/api/v1/orders", json=order2)

    order3 = {
        "user_id": eve_id,
        "stock_name": "Tesla",
        "order_type": "SELL",
        "shares": 20,
        "price_per_share": 178
    }
    client.post("/api/v1/orders", json=order3)


    response = client.get("/api/v1/orders")
    orders = response.json()

    assert orders[0]["price_per_share"] == 175
    assert orders[1]["price_per_share"] == 178
    assert orders[2]["price_per_share"] == 180

# Тест обработки некорректного ордера
def test_invalid_order_creation(client):
    response = client.post("/api/v1/orders", json={
        "user_id": 1,
        "stock_name": "Tesla",
        "order_type": "BUY",
        "shares": -10,
        "price_per_share": 170
    })
    assert response.status_code == 422

# Тест отмены ордера после частичного исполнения
def test_cancel_order_after_partial_execution(client):
    # Создаем продавца
    response = client.post("/api/v1/users", json={"name": "Adam"})
    adam_id = response.json()["id"]

    sell_order = {
        "user_id": adam_id,
        "stock_name": "Tesla",
        "order_type": "SELL",
        "shares": 150,
        "price_per_share": 176
    }
    client.post("/api/v1/orders", json=sell_order)


    response = client.post("/api/v1/users", json={"name": "Alice"})
    alice_id = response.json()["id"]

    buy_order = {
        "user_id": alice_id,
        "stock_name": "Tesla",
        "order_type": "BUY",
        "shares": 100,
        "price_per_share": 176
    }
    client.post("/api/v1/orders", json=buy_order)

    response = client.get("/api/v1/transactions")
    transactions = response.json()
    assert len(transactions) == 1
    assert transactions[0]["shares"] == 100

    response = client.get("/api/v1/orders")
    remaining_order = next(order for order in response.json() if order["user_id"] == adam_id)
    response = client.delete(f"/api/v1/orders/{remaining_order['id']}")
    assert response.status_code == 200


    response = client.get(f"/api/v1/orders/{remaining_order['id']}")
    assert response.status_code == 404

