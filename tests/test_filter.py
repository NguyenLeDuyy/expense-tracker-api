from datetime import date, timedelta
def test_filter_by_date_range(client, auth_headers, test_category):
    # Tạo 3 expenses với dates khác nhau
    for i in range(3):
        client.post("/expenses/", json={
        "amount": 50000 - i * 5000,
        "category_id": test_category["id"],
        "date": str(date.today() - timedelta(days=i))
    }, headers=auth_headers)
    # GET /expenses/?start_date=. ..&end_date=...
    response = client.get("/expenses", params={
        "start_date": date.today(),
        "end_date": date.today()
    }, headers=auth_headers)
    # Assert: chỉ trả expenses trong range
    data = response.json()
    assert data["status"] == "success"
    assert data["data"]["total_count"] == 1


def test_sort_by_amount(client, auth_headers, test_category):
    # Tạo expenses với amounts khác nhau
    for i in range(3):
        client.post("/expenses/", json={
        "amount": 50000 - i * 5000,
        "category_id": test_category["id"],
    }, headers=auth_headers)
    # GET /expenses/?sort_by=amount_desc
    response = client.get("/expenses", params={
        "sort_by": "amount_desc"
    }, headers=auth_headers)
    # Assert: item đầu tiên có amount lớn nhất
    data = response.json()
    items = data["data"]["items"]
    max_amount = max(item["amount"] for item in items)
    assert max_amount == items[0]["amount"]

def test_pagination(client, auth_headers, test_category):
    # Tạo 15 expenses
    for i in range(15):
        client.post("/expenses/", json={
        "amount": 50000,
        "category_id": test_category["id"]
    }, headers=auth_headers)
    # GET /expenses/?page=1&page_size=5
    response = client.get("/expenses", params={
        "page": 1,
        "page_size": 5,
    }, headers=auth_headers)
    # Assert: items có 5 phần tử, total_count == 15
    data = response.json()
    assert data["status"] == "success"
    assert len(data["data"]["items"]) == 5
    assert data["data"]["total_count"] == 15