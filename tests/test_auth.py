from fastapi.testclient import TestClient
from app.main import app
from app.database.database import get_db
from .test_database import get_test_db
from app.models.user import User
from app.services.users_service import password_hash


client = TestClient(app)

# When a test endpoint asks for get_db, use get_test_db instead
app.dependency_overrides[get_db] = get_test_db

# Normal users can register
def test_user_registration(db):
    response = client.post("/api/v1/users/",
                           json={
                               "username": "Rahim",
                               "password": "testPassword123"
                           })

    assert response.status_code == 200
    data = response.json()

    assert data["username"] == "Rahim"
    assert data["role"] == "user"
    assert "id" in data
    assert "password" not in data


"""
Client sends:
role = "admin"
       ↓
UserCreate doesn't allow role to control privileges
       ↓
create_user()
       ↓
server sets:
role = "user"
       ↓
Response:
role = "user"
"""

# Users cannot make themselves admin
def test_user_cannot_choose_admin_role(db):
    response = client.post("/api/v1/users/",
                           json={
                               "username": "Rahim",
                               "password": "TestPassword123",
                               "role": "admin"
                           })

    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "Rahim"
    assert data["role"] == "user"
    assert "id" in data


"""
Registered user
      ↓
POST /api/v1/auth/login
      ↓
username + password
      ↓
authenticate_user()
      ↓
JWT generated
      ↓
access_token returned
"""

# Correct credentials produce a JWT
def test_user_login(db):
    # Creating a user first
    response = client.post("/api/v1/users/",
                           json={
                               "username": "Rahim",
                               "password": "testpassword123"
                           })
    # login with the user credentials that we have just created
    response = client.post("/api/v1/auth/login/",
                           data={       # our login uses OAuth2PasswordRequestForm so it expects data, not json
                               "username": "Rahim",
                               "password": "testpassword123"
                           })

    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


"""
POST /api/v1/sales/
        ↓
Does request contain JWT?
        ↓
       NO
        ↓
OAuth2PasswordBearer
        ↓
401 Unauthorized
"""

# Incorrect credentials are rejected with 401
def test_login_with_wrong_password(db):
    response = client.post("/api/v1/users/",
                           json={
                               "username": "Rahim",
                               "password": "testpass123"
                           })

    response = client.post("/api/v1/auth/login/",
                           data={ "username": "Rahim",
                                  "password": "sddsdcevdsdca"
                                  })

    assert response.status_code == 401
    data = response.json()
    assert data["detail"] == "Incorrect username or password"


# test whether the JWT actually protect your API!
# It should successfully block protected endpoints without a JWT
def test_create_sale_without_token(db):
    response = client.post("/api/v1/sales/",
                           json={
                               "product_name": "Laptop",
                               "category": "Electronics",
                               "quantity": 2,
                               "unit_price": 800.0,
                               "sale_date": "2026-09-21"
                           })

    assert response.status_code == 401


"""
Register user
    ↓
Login
    ↓
Receive JWT
    ↓
Send JWT to /sales/
    ↓
Sale created successfully
"""
# test create a sale with valid Jwt token
def test_create_sale_with_token(db):
    response = client.post("/api/v1/users/",
                           json={
                               "username": "Rahim",
                               "password": "mypassword123"
                           })

    response = client.post("/api/v1/auth/login/",
                           data={
                               "username": "Rahim",
                               "password": "mypassword123"
                           })

    login_data = response.json()
    token = login_data["access_token"]

    response = client.post("/api/v1/sales/",
                           headers={  # HTTP authentication uses an Authorization header
                               "Authorization": f"Bearer {token}"
                           },
                           json={
                               "product_name": "Laptop",
                               "category": "Electronics",
                               "quantity": 2,
                               "unit_price": 800.0,
                               "sale_date": "2026-09-21"
                           })

    assert response.status_code == 200
    data = response.json()
    assert data["product_name"] == "Laptop"
    assert data["category"] == "Electronics"
    assert data["quantity"] == 2
    assert data["unit_price"] == 800.0
    assert data["sale_date"] == "2026-09-21"


"""
USER A
  ↓
Register
  ↓
Login → token_a
  ↓
Create sale → sale_id


USER B
  ↓
Register
  ↓
Login → token_b
  ↓
GET /sales/{sale_id}
using token_b
  ↓
404
"""

# tester isolation
def test_user_cannot_access_other_users_sale(db):
    # User A
    response = client.post("/api/v1/users/",
                           json={
                               "username": "Rahim",
                                "password": "mypass123"
                           })
    response = client.post("/api/v1/auth/login/",
                           data={
                               "username": "Rahim",
                               "password": "mypass123"
                           })

    login_data_a = response.json()
    token_a = login_data_a["access_token"]

    response = client.post("/api/v1/sales/",
                           headers={  # HTTP authentication uses an Authorization header
                               "Authorization": f"Bearer {token_a}"
                           },
                           json={
                               "product_name": "Laptop",
                               "category": "Electronics",
                               "quantity": 2,
                               "unit_price": 800.0,
                               "sale_date": "2026-09-21"
                           })

    sale_data = response.json()
    sale_id = sale_data["id"]

    # user B
    response = client.post("/api/v1/users/",
                           json={
                               "username": "Karim",
                               "password": "123"
                           })
    response = client.post("/api/v1/auth/login/",
                           data={
                               "username": "Karim",
                               "password": "123"
                           })

    login_data_2 = response.json()
    token_b = login_data_2["access_token"]

    response = client.get(f"/api/v1/sales/{sale_id}",
                             headers={
                                 "Authorization": f"Bearer {token_b}"
                             })

    assert response.status_code == 404


"""
Register User
     ↓
Login
     ↓
Get JWT
     ↓
Create a sale
     ↓
GET /api/v1/sales/
     ↓
Use same JWT
     ↓
200 OK
     ↓
Sale appears in response
"""

# testing that an authenticated user can actually retrieve their own data.
def test_user_can_get_own_sales(db):
    response = client.post("/api/v1/users/",
                           json={
                               "username": "Rahim",
                               "password": "123"
                           })
    response = client.post("/api/v1/auth/login/",
                           data={
                               "username": "Rahim",
                               "password": "123"
                           })
    login_data = response.json()
    token = login_data["access_token"]

    response = client.post("/api/v1/sales/",
                           headers={ "Authorization": f"Bearer {token}"},
                           json={
                               "product_name": "Laptop",
                                "category": "Electronics",
                               "quantity": 2,
                                "unit_price": 800.0,
                               "sale_date": "2026-09-21"
                           })


    response = client.get("/api/v1/sales/",
                          headers={ "Authorization": f"Bearer {token}"})

    assert response.status_code == 200
    data = response.json()
    assert "id" in data[0]
    assert data[0]["product_name"] == "Laptop"
    assert data[0]["category"] == "Electronics"
    assert data[0]["quantity"] == 2
    assert data[0]["unit_price"] == 800.0
    assert data[0]["sale_date"] == "2026-09-21"

"""
Register
   ↓
Login → JWT
   ↓
Create sale
   ↓
Capture sale_id
   ↓
PUT /api/v1/sales/{sale_id}
   ↓
Send JWT
   ↓
Change something
   ↓
200 OK
   ↓
Verify updated data
"""

# update a sale
def test_user_can_update_own_sales(db):
    response = client.post("/api/v1/users/",
                           json={
                               "username": "Rahim",
                               "password": "123"
                           })
    response = client.post("/api/v1/auth/login/",
                           data={
                               "username": "Rahim",
                               "password": "123"
                           })
    login_data = response.json()
    token = login_data["access_token"]

    response = client.post("/api/v1/sales/",
                           headers={ "Authorization": f"Bearer {token}"},
                           json={
                               "product_name": "Laptop",
                               "category": "Electronics",
                               "quantity": 2,
                               "unit_price": 800.0,
                               "sale_date": "2026-09-21"
                           })

    sale_data = response.json()
    sale_id = sale_data["id"]

    response = client.put(f"/api/v1/sales/{sale_id}",
                          headers={ "Authorization": f"Bearer {token}"},
                          json={
                              "product_name": "Laptop",
                              "category": "Electronics",
                              "quantity": 5,
                              "unit_price": 599.99,
                              "sale_date": "2026-09-21"
                          })

    assert response.status_code == 200
    data = response.json()
    assert data["quantity"] == 5
    assert data["unit_price"] == 599.99

"""
Register
   ↓
Login → JWT
   ↓
Create sale
   ↓
Get sale_id
   ↓
DELETE /sales/{sale_id}
   ↓
JWT
   ↓
Successful deletion
   ↓
Try to GET the same sale
   ↓
404 Not Found
"""
# Delete a sale
def test_user_can_delete_own_sale(db):
    response = client.post("/api/v1/users/",
                           json={
                               "username": "Rahim",
                               "password": "123"
                           })
    response = client.post("/api/v1/auth/login/",
                           data={
                               "username": "Rahim",
                               "password": "123"
                           })

    login_data = response.json()
    token = login_data["access_token"]

    response = client.post("/api/v1/sales/",
                           headers={ "Authorization": f"Bearer {token}"},
                           json={
                               "product_name": "Laptop",
                                "category": "Electronics",
                               "quantity": 2,
                               "unit_price": 800.0,
                               "sale_date": "2026-09-21"
                           })

    sale_data = response.json()
    sale_id = sale_data["id"]

    response = client.delete(f"/api/v1/sales/{sale_id}",
                             headers={ "Authorization": f"Bearer {token}"})


    assert response.status_code == 200

    response = client.get(f"/api/v1/sales/{sale_id}",
                          headers={ "Authorization": f"Bearer {token}"})

    assert response.status_code == 404


"""
Register
   ↓
Login → token
   ↓
Create sale (2 × 800)
   ↓
GET /api/v1/analytics/revenue
   ↓
Authorization header
   ↓
200
   ↓
total_revenue == 1600.0
"""

# test revenue
def test_user_can_get_revenue(db):
    response = client.post("/api/v1/users/",
                           json={
                               "username": "Rahim",
                               "password": "123"
                           })
    response = client.post("/api/v1/auth/login/",
                           data={
                               "username": "Rahim",
                               "password": "123"
                           })
    login_data = response.json()
    token = login_data["access_token"]

    response = client.post("/api/v1/sales/",
                           headers={ "Authorization": f"Bearer {token}"},
                           json={
                               "product_name": "Laptop",
                               "category": "Electronics",
                               "quantity": 2,
                               "unit_price": 800.0,
                               "sale_date": "2026-09-21"
                           })

    assert response.status_code == 200

    response = client.get("/api/v1/analytics/revenue/",
                          headers={ "Authorization": f"Bearer {token}"})


    data = response.json()
    assert data["total_revenue"] == 1600.0


"""
Register
 ↓
Login → token
 ↓
Create Laptop sale #1
 ↓
Create Laptop sale #2
 ↓
GET /api/v1/analytics/products
 ↓
JWT
 ↓
Find Laptop in the returned list
 ↓
Verify quantity = 5
 ↓
Verify revenue = 3700
"""
#test product analytics
def test_user_can_get_product_analytics(db):
    response = client.post("/api/v1/users/",
                           json={
                               "username": "Rahim",
                               "password": "123"
                           })
    response = client.post("/api/v1/auth/login/",
                           data={
                               "username": "Rahim",
                               "password": "123"
                           })
    login_data = response.json()
    token = login_data["access_token"]

    response = client.post("/api/v1/sales/",
                           headers={ "Authorization": f"Bearer {token}"},
                           json={
                               "product_name": "Laptop",
                               "category": "Electronics",
                               "quantity": 2,
                               "unit_price": 800.0,
                               "sale_date": "2026-09-21"
                           })
    response = client.post("/api/v1/sales/",
                           headers={ "Authorization": f"Bearer {token}"},
                           json={
                               "product_name": "Laptop",
                               "category": "Electronics",
                               "quantity": 5,
                               "unit_price": 599.99,
                               "sale_date": "2026-09-21"
                           })

    response = client.get("/api/v1/analytics/products/",
                          headers={ "Authorization": f"Bearer {token}"})

    data = response.json()
    assert data[0]["product_name"] == "Laptop"
    assert data[0]["quantity_sold"] == 7
    assert data[0]["revenue"] == 4599.95


"""
Register
   ↓
Login → token
   ↓
Create Laptop sale
   ↓
Create Chair sale
   ↓
GET /api/v1/analytics/categories
   ↓
JWT
   ↓
Find Electronics in returned list
   ↓
Verify quantity = 2
   ↓
Verify revenue = 1600
   ↓
Find Furniture in returned list
   ↓
Verify quantity = 3
   ↓
Verify revenue = 600
"""

# test category analytics
def test_user_can_get_category_analytics(db):
    response = client.post("/api/v1/users/",
                           json={
                               "username": "Rahim",
                               "password": "123"
                           })
    response = client.post("/api/v1/auth/login/",
                           data={
                               "username": "Rahim",
                               "password": "123"
                           })
    login_data = response.json()
    token = login_data["access_token"]

    response = client.post("/api/v1/sales/",
                           headers={ "Authorization": f"Bearer {token}"},
                           json={
                               "product_name": "Laptop",
                               "category": "Electronics",
                               "quantity": 2,
                               "unit_price": 800.0,
                               "sale_date": "2026-09-21"
                           })
    response = client.post("/api/v1/sales/",
                           headers={ "Authorization": f"Bearer {token}"},
                           json={
                               "product_name": "Chair",
                               "category": "Furniture",
                               "quantity": 6,
                               "unit_price": 35.0,
                               "sale_date": "2026-09-21"
                           })

    response = client.get("/api/v1/analytics/categories/",
                          headers={ "Authorization": f"Bearer {token}"})

    assert response.status_code == 200
    data = response.json()

    assert data[0]["category"] == "Electronics"
    assert data[0]["quantity_sold"] == 2
    assert data[0]["revenue"] == 1600

    assert data[1]["category"] == "Furniture"
    assert data[1]["quantity_sold"] == 6
    assert data[1]["revenue"] == 210


"""
Register
   ↓
Login → token
   ↓
Create Sale #1
   ↓
Create Sale #2
   ↓
GET /api/v1/analytics/summary
   ↓
JWT
   ↓
Verify total revenue
   ↓
Verify total orders
   ↓
Verify average order value
"""
# test analytics summary
def test_user_can_get_summary_analytics(db):
    response = client.post("/api/v1/users/",
                           json={
                               "username": "Rahim",
                               "password": "123"
                           })
    response  = client.post("/api/v1/auth/login/",
                            data={
                                "username": "Rahim",
                                "password": "123"
                            })

    login_data = response.json()
    token = login_data["access_token"]

    response = client.post("/api/v1/sales/",
                           headers={ "Authorization": f"Bearer {token}"},
                           json={
                               "product_name": "Laptop",
                               "category": "Electronics",
                               "quantity": 2,
                               "unit_price": 500.0,
                               "sale_date": "2026-09-21"
                           })
    response = client.post("/api/v1/sales/",
                           headers={ "Authorization": f"Bearer {token}"},
                           json={
                               "product_name": "Chair",
                               "category": "Furniture",
                               "quantity": 5,
                               "unit_price": 100.0,
                               "sale_date": "2026-09-21"
                           })

    response = client.get("/api/v1/analytics/summary/",
                          headers={ "Authorization": f"Bearer {token}"})

    assert response.status_code == 200
    data = response.json()
    assert data["total_revenue"] == 1500
    assert data["total_orders"] == 2
    assert data["average_order_value"] == 750


"""
Register normal user
        ↓
Login → token
        ↓
GET /api/v1/users/
        ↓
JWT
        ↓
Expect 403 Forbidden
"""
# test normal user cannot access user list
def test_normal_user_cannot_get_all_users(db):
    response = client.post("/api/v1/users/",
                           json={
                               "username": "Rahim",
                               "password": "123"
                           })
    response = client.post("/api/v1/auth/login/",
                           data={
                               "username": "Rahim",
                               "password": "123"
                           })
    login_data = response.json()
    token = login_data["access_token"]

    response = client.get("/api/v1/users/",
                          headers={ "Authorization": f"Bearer {token}"})

    assert response.status_code == 403


"""
Create admin user directly in test DB
        ↓
Login as admin → token
        ↓
Create normal user
        ↓
GET /api/v1/users/
        ↓
JWT
        ↓
Expect 200
        ↓
Verify users are returned
"""
# test admin can get all users
def test_admin_can_get_all_users(db):
    # it creates admin directly in test DB
    admin = User(
        username="Rahim",
        password_hash=password_hash.hash("123"),
        role="admin"
    )

    db.add(admin)
    db.commit()

    response = client.post("/api/v1/auth/login/",
                           data={
                               "username": "Rahim",
                               "password": "123"
                           })
    login_data = response.json()
    token = login_data["access_token"]

    response = client.get("/api/v1/users/",
                          headers={ "Authorization": f"Bearer {token}"})

    assert response.status_code == 200












