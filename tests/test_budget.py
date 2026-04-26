def test_create_category(client, auth_headers):
    # POST /categories/ với name + monthly_budget
    response = client.post("/categories/", json={
        "name": "Food",
        "monthly_budget": 1000000
    }, headers=auth_headers)
    # Assert: status "success"
    data = response.json()
    assert data["status"] == "success"

def test_budget_exceeded_warning(client, auth_headers, test_category):
    # test_category có monthly_budget = 1,000,000
    # Tạo expense amount = 1,200,000
    response = client.post("/expenses/", json={
        "amount": 1200000,
        "category_id": test_category["id"]
    }, headers=auth_headers)
    # Assert: response có warning chứa "Budget exceeded"
    data = response.json()
    assert data["data"]["warning"] is not None

def test_within_budget_no_warning(client, auth_headers, test_category):
    # Tạo expense amount = 500,000
    response = client.post("/expenses/", json={
        "amount": 50000,
        "category_id": test_category["id"]
    }, headers=auth_headers)
    # Assert: warning is None
    assert response.json()["data"]["warning"] is None
    