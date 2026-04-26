def test_create_expense(client, auth_headers, test_category):
    # POST /expenses/ với amount, category_id từ test_category
    # Assert: status "success", data có id, amount, category_id
    response = client.post("/expenses/", json={
        "amount": 50000,
        "category_id": test_category["id"]
    }, headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "id" in data["data"]
    assert data["data"]["amount"] == 50000
    assert data["data"]["category_id"] == test_category["id"]

def test_get_expenses(client, auth_headers, test_category):
    # Tạo 2 expenses, GET /expenses/
    for i in range(2):
        client.post("/expenses/", json={
        "amount": 50000,
        "category_id": test_category["id"]
    }, headers=auth_headers)

    response = client.get("/expenses", headers=auth_headers)
    data = response.json()
    assert data["status"] == "success"
    assert data["data"]["total_count"] == 2
    # Assert: total_count == 2

def test_update_expense(client, auth_headers, test_category):
    # Tạo expense, PUT /expenses/{id} với amount mới
    response_create = client.post("/expenses/", json={
        "amount": 50000,
        "category_id": test_category["id"]
    }, headers=auth_headers)
    expense_id = response_create.json()["data"]["id"]

    response_update = client.put(f"/expenses/{expense_id}", json={
        "amount": 150000,
        "category_id": test_category["id"]
    }, headers=auth_headers)

    data = response_update.json()
    assert data["status"] == "success"
    assert data["data"]["amount"] == 150000
    # Assert: amount đã thay đổi

def test_delete_expense(client, auth_headers, test_category):
    # Tạo expense, DELETE /expenses/{id}
    response_create = client.post("/expenses/", json={
        "amount": 50000,
        "category_id": test_category["id"]
    }, headers=auth_headers)

    expense_id = response_create.json()["data"]["id"]

    response_delete = client.delete(f"/expenses/{expense_id}", headers=auth_headers)
    
    # Assert: message "Expense deleted"
    data = response_delete.json()
    assert data["status"] == "success"
    assert data["message"] == "Expense deleted successfully"

def test_user_isolation(client, auth_headers, test_category):
    # User A tạo expense
    response_A = client.post("/expenses/", json={
        "amount": 50000,
        "category_id": test_category["id"]
    }, headers=auth_headers)
    # Register user B, login, GET /expenses/
    client.post("/auth/register", json={
        "email": "testB@test.com",
        "password": "testpassword123"
    })
    response_auth_B = client.post("/auth/login", json={
        "email": "testB@test.com",
        "password": "testpassword123"
    })
    token = response_auth_B.json()["data"]["tokens"]["access_token"]
    headers_B = {"Authorization": f"Bearer {token}"}

    # Assert: user B thấy total_count == 0
    response_B = client.get("/expenses", headers=headers_B)
    data_B = response_B.json()
    assert data_B["status"] == "success"
    assert data_B["data"]["total_count"] == 0