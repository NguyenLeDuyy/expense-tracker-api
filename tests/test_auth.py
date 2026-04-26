def test_register_success(client):
    # POST /auth/register với email + password hợp lệ
    response = client.post("/auth/register", json={
        "email": "test@test.com",
        "password": "testpassword123"
    })
    # Assert: status 200, response có data.user.email và data.tokens
    data = response.json()
    assert data["status"] == "success"
    assert "email" in data["data"]["user"]
    assert "tokens" in data["data"]

def test_register_duplicate_email(client):
    # Register 2 lần cùng email
    client.post("/auth/register", json={
        "email": "test@test.com",
        "password": "testpassword123"
    })
    response = client.post("/auth/register", json={
        "email": "test@test.com",
        "password": "testpassword123"
    })

    # Assert: lần 2 trả status "error", message "Email already exists"
    data = response.json()
    assert response.status_code == 400   
    assert data["status"] == "error"
    assert data["message"] == "Email already exists"

def test_login_success(client):
    # Register rồi login
    client.post("/auth/register", json={
        "email": "test@test.com",
        "password": "testpassword123"
    })
    response = client.post("/auth/login", json={
        "email": "test@test.com",
        "password": "testpassword123"
    })
    # Assert: response có access_token và refresh_token
    tokens = response.json()["data"]["tokens"]
    assert "access_token" in tokens
    assert "refresh_token" in tokens



def test_login_wrong_password(client):
    # Register rồi login sai password
    client.post("/auth/register", json={
        "email": "test@test.com",
        "password": "testpassword123"
    })
    response = client.post("/auth/login", json={
        "email": "test@test.com",
        "password": "testpassword12"
    })
    # Assert: status "error", 401
    assert response.json()["status"] == "error"
    assert response.status_code == 401

def test_access_protected_route_without_token(client):
    # GET /auth/me không có header Authorization
    response = client.get("/auth/me")

    # Assert: 401 (FastAPI OAuth2 trả {"detail": "Not authenticated"}, không có "status")
    assert response.status_code == 401

def test_access_protected_route_with_token(client, auth_headers):
    # GET /auth/me với Bearer token
    response = client.get("/auth/me", headers=auth_headers)
    # Assert: trả email đúng
    assert "email" in response.json()["data"]