def test_root_endpoint(client):
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_user_registration(client):
    response = client.post(
        "/auth/register",
        json={
            "email": "pytest@example.com",
            "password": "TestPassword123!"
        }
    )

    assert response.status_code == 200
    assert response.json()["email"] == "pytest@example.com"
    assert "id" in response.json()


def test_duplicate_email_registration(client):
    user_data = {
        "email": "duplicate@example.com",
        "password": "TestPassword123!"
    }

    first_response = client.post(
        "/auth/register",
        json=user_data
    )

    second_response = client.post(
        "/auth/register",
        json=user_data
    )

    assert first_response.status_code == 200
    assert second_response.status_code == 400


def test_user_login(client):
    user_data = {
        "email": "login@example.com",
        "password": "TestPassword123!"
    }

    # Register the user first
    register_response = client.post(
        "/auth/register",
        json=user_data
    )

    assert register_response.status_code == 200

    # Attempt to log in
    login_response = client.post(
        "/auth/login",
        data={
            "username": user_data["email"],
            "password": user_data["password"]
        }
    )

    assert login_response.status_code == 200
    assert "access_token" in login_response.json()
    assert login_response.json()["token_type"] == "bearer"


def test_authenticated_user_can_access_me(client):
    user_data = {
        "email": "authenticated@example.com",
        "password": "TestPassword123!"
    }

    # Register user
    client.post("/auth/register", json=user_data)

    # Log in
    login_response = client.post(
        "/auth/login",
        data={
            "username": user_data["email"],
            "password": user_data["password"]
        }
    )

    token = login_response.json()["access_token"]

    # Access protected endpoint
    response = client.get(
        "/auth/me",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200
    assert response.json()["email"] == user_data["email"]


def test_unauthenticated_user_cannot_access_me(client):
    response = client.get("/auth/me")

    assert response.status_code == 401


def test_unauthenticated_user_cannot_create_expense(client):
    response = client.post(
        "/expenses/",
        json={
            "description": "Groceries",
            "amount": 450.50,
            "date": "2026-11-12"
        }
    )

    assert response.status_code == 401


def test_login_with_wrong_password(client):
    user_data = {
        "email": "wrongpassword@example.com",
        "password": "CorrectPassword123!"
    }

    # Register user
    client.post("/auth/register", json=user_data)

    # Attempt login with incorrect password
    response = client.post(
        "/auth/login",
        data={
            "username": user_data["email"],
            "password": "WrongPassword123!"
        }
    )

    assert response.status_code == 401


def test_user_cannot_access_me_with_invalid_token(client):
    response = client.get(
        "/auth/me",
        headers={
            "Authorization": "Bearer invalid.token.here"
        }
    )

    assert response.status_code == 401


def test_authenticated_user_can_create_expense(client):
    user_data = {
        "email": "expenseuser@example.com",
        "password": "TestPassword123!"
    }

    # Register user
    client.post("/auth/register", json=user_data)

    # Log in
    login_response = client.post(
        "/auth/login",
        data={
            "username": user_data["email"],
            "password": user_data["password"]
        }
    )

    token = login_response.json()["access_token"]

    # Create an expense
    expense_data = {
        "description": "Groceries",
        "amount": 450.50,
        "date": "2026-11-12"
    }

    response = client.post(
        "/expenses/",
        json=expense_data,
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200
    assert response.json()["description"] == "Groceries"
    assert response.json()["amount"] == 450.50
    assert response.json()["date"] == "2026-11-12"
    assert "id" in response.json()


def test_user_can_list_their_expenses(client):
    user_data = {
        "email": "listuser@example.com",
        "password": "TestPassword123!"
    }

    # Register user
    client.post("/auth/register", json=user_data)

    # Log in
    login_response = client.post(
        "/auth/login",
        data={
            "username": user_data["email"],
            "password": user_data["password"]
        }
    )

    token = login_response.json()["access_token"]

    headers = {
        "Authorization": f"Bearer {token}"
    }

    # Create an expense
    client.post(
        "/expenses/",
        json={
            "description": "Transport",
            "amount": 100.00,
            "date": "2026-11-12"
        },
        headers=headers
    )

    # Retrieve expenses
    response = client.get("/expenses/", headers=headers)

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["description"] == "Transport"


def test_users_cannot_see_each_others_expenses(client):

    # Register and log in User 1
    user1 = {
        "email": "user1@example.com",
        "password": "TestPassword123!"
    }

    client.post("/auth/register", json=user1)

    login1 = client.post(
        "/auth/login",
        data={
            "username": user1["email"],
            "password": user1["password"]
        }
    )

    token1 = login1.json()["access_token"]

    headers1 = {
        "Authorization": f"Bearer {token1}"
    }

    # User 1 creates an expense
    client.post(
        "/expenses/",
        json={
            "description": "Private groceries",
            "amount": 500.00,
            "date": "2026-11-12"
        },
        headers=headers1
    )

    # Register and log in User 2
    user2 = {
        "email": "user2@example.com",
        "password": "TestPassword123!"
    }

    client.post("/auth/register", json=user2)

    login2 = client.post(
        "/auth/login",
        data={
            "username": user2["email"],
            "password": user2["password"]
        }
    )

    token2 = login2.json()["access_token"]

    headers2 = {
        "Authorization": f"Bearer {token2}"
    }

    # User 2 tries to retrieve expenses
    response = client.get("/expenses/", headers=headers2)

    assert response.status_code == 200
    assert len(response.json()) == 0


def test_user_can_delete_their_expense(client):
    user_data = {
        "email": "deleteuser@example.com",
        "password": "TestPassword123!"
    }

    # Register user
    client.post("/auth/register", json=user_data)

    # Log in
    login_response = client.post(
        "/auth/login",
        data={
            "username": user_data["email"],
            "password": user_data["password"]
        }
    )

    token = login_response.json()["access_token"]

    headers = {
        "Authorization": f"Bearer {token}"
    }

    # Create an expense
    create_response = client.post(
        "/expenses/",
        json={
            "description": "Dinner",
            "amount": 250.00,
            "date": "2026-11-12"
        },
        headers=headers
    )

    expense_id = create_response.json()["id"]

    # Delete the expense
    delete_response = client.delete(
        f"/expenses/{expense_id}",
        headers=headers
    )

    assert delete_response.status_code == 200
    assert delete_response.json() == {"status": "deleted"}

    # Confirm it no longer exists in the user's expense list
    list_response = client.get("/expenses/", headers=headers)

    assert list_response.status_code == 200
    assert len(list_response.json()) == 0


def test_user_cannot_delete_another_users_expense(client):

    # Register User 1
    user1 = {
        "email": "owner@example.com",
        "password": "TestPassword123!"
    }

    client.post("/auth/register", json=user1)

    login1 = client.post(
        "/auth/login",
        data={
            "username": user1["email"],
            "password": user1["password"]
        }
    )

    token1 = login1.json()["access_token"]

    headers1 = {
        "Authorization": f"Bearer {token1}"
    }

    # User 1 creates an expense
    create_response = client.post(
        "/expenses/",
        json={
            "description": "Private dinner",
            "amount": 300.00,
            "date": "2026-11-12"
        },
        headers=headers1
    )

    expense_id = create_response.json()["id"]

    # Register User 2
    user2 = {
        "email": "attacker@example.com",
        "password": "TestPassword123!"
    }

    client.post("/auth/register", json=user2)

    login2 = client.post(
        "/auth/login",
        data={
            "username": user2["email"],
            "password": user2["password"]
        }
    )

    token2 = login2.json()["access_token"]

    headers2 = {
        "Authorization": f"Bearer {token2}"
    }

    # User 2 attempts to delete User 1's expense
    response = client.delete(
        f"/expenses/{expense_id}",
        headers=headers2
    )

    assert response.status_code == 404

    # Verify User 1's expense still exists
    owner_response = client.get("/expenses/", headers=headers1)

    assert owner_response.status_code == 200
    assert len(owner_response.json()) == 1
    assert owner_response.json()[0]["description"] == "Private dinner"


def test_user_can_update_their_expense(client):
    user_data = {
        "email": "updateuser@example.com",
        "password": "TestPassword123!"
    }

    # Register user
    client.post("/auth/register", json=user_data)

    # Log in
    login_response = client.post(
        "/auth/login",
        data={
            "username": user_data["email"],
            "password": user_data["password"]
        }
    )

    token = login_response.json()["access_token"]

    headers = {
        "Authorization": f"Bearer {token}"
    }

    # Create an expense
    create_response = client.post(
        "/expenses/",
        json={
            "description": "Old description",
            "amount": 100.00,
            "date": "2026-11-12"
        },
        headers=headers
    )

    expense_id = create_response.json()["id"]

    # Update the expense
    update_response = client.put(
        f"/expenses/{expense_id}",
        json={
            "description": "Updated description",
            "amount": 200.00,
            "date": "2026-11-12"
        },
        headers=headers
    )

    assert update_response.status_code == 200
    assert update_response.json()["description"] == "Updated description"
    assert update_response.json()["amount"] == 200.00


def test_user_can_partially_update_expense(client):
    user_data = {
        "email": "patchuser@example.com",
        "password": "TestPassword123!"
    }

    # Register user
    client.post("/auth/register", json=user_data)

    # Log in
    login_response = client.post(
        "/auth/login",
        data={
            "username": user_data["email"],
            "password": user_data["password"]
        }
    )

    token = login_response.json()["access_token"]

    headers = {
        "Authorization": f"Bearer {token}"
    }

    # Create an expense
    create_response = client.post(
        "/expenses/",
        json={
            "description": "Original description",
            "amount": 150.00,
            "date": "2026-11-12"
        },
        headers=headers
    )

    expense_id = create_response.json()["id"]

    # Change only the description
    patch_response = client.patch(
        f"/expenses/{expense_id}",
        json={
            "description": "New description"
        },
        headers=headers
    )

    assert patch_response.status_code == 200
    assert patch_response.json()["description"] == "New description"
    assert patch_response.json()["amount"] == 150.00


def test_user_cannot_update_another_users_expense(client):

    # Register User 1
    user1 = {
        "email": "updateowner@example.com",
        "password": "TestPassword123!"
    }

    client.post("/auth/register", json=user1)

    login1 = client.post(
        "/auth/login",
        data={
            "username": user1["email"],
            "password": user1["password"]
        }
    )

    token1 = login1.json()["access_token"]

    headers1 = {
        "Authorization": f"Bearer {token1}"
    }

    # User 1 creates an expense
    create_response = client.post(
        "/expenses/",
        json={
            "description": "Original expense",
            "amount": 400.00,
            "date": "2026-11-12"
        },
        headers=headers1
    )

    expense_id = create_response.json()["id"]

    # Register User 2
    user2 = {
        "email": "updateattacker@example.com",
        "password": "TestPassword123!"
    }

    client.post("/auth/register", json=user2)

    login2 = client.post(
        "/auth/login",
        data={
            "username": user2["email"],
            "password": user2["password"]
        }
    )

    token2 = login2.json()["access_token"]

    headers2 = {
        "Authorization": f"Bearer {token2}"
    }

    # User 2 attempts to update User 1's expense
    response = client.put(
        f"/expenses/{expense_id}",
        json={
            "description": "Hacked expense",
            "amount": 1.00,
            "date": "2026-11-12"
        },
        headers=headers2
    )

    assert response.status_code == 404

    # Verify User 1's expense remains unchanged
    owner_response = client.get("/expenses/", headers=headers1)

    assert owner_response.status_code == 200
    assert owner_response.json()[0]["description"] == "Original expense"
    assert owner_response.json()[0]["amount"] == 400.00


def test_user_cannot_patch_another_users_expense(client):

    # Register User 1
    user1 = {
        "email": "patchowner@example.com",
        "password": "TestPassword123!"
    }

    client.post("/auth/register", json=user1)

    login1 = client.post(
        "/auth/login",
        data={
            "username": user1["email"],
            "password": user1["password"]
        }
    )

    token1 = login1.json()["access_token"]
    headers1 = {"Authorization": f"Bearer {token1}"}

    # User 1 creates an expense
    create_response = client.post(
        "/expenses/",
        json={
            "description": "Original groceries",
            "amount": 600.00,
            "date": "2026-11-12"
        },
        headers=headers1
    )

    expense_id = create_response.json()["id"]

    # Register User 2
    user2 = {
        "email": "patchattacker@example.com",
        "password": "TestPassword123!"
    }

    client.post("/auth/register", json=user2)

    login2 = client.post(
        "/auth/login",
        data={
            "username": user2["email"],
            "password": user2["password"]
        }
    )

    token2 = login2.json()["access_token"]
    headers2 = {"Authorization": f"Bearer {token2}"}

    # User 2 attempts to modify User 1's expense
    response = client.patch(
        f"/expenses/{expense_id}",
        json={"description": "Stolen expense"},
        headers=headers2
    )

    assert response.status_code == 404

    # Confirm User 1's expense remains unchanged
    owner_response = client.get("/expenses/", headers=headers1)

    assert owner_response.status_code == 200
    assert owner_response.json()[0]["description"] == "Original groceries"
    assert owner_response.json()[0]["amount"] == 600.00



def test_user_registration_with_invalid_email(client):
    response = client.post(
        "/auth/register",
        json={
            "email": "not-an-email",
            "password": "TestPassword123!"
        }
    )

    assert response.status_code == 422



def test_login_with_nonexistent_user(client):
    response = client.post(
        "/auth/login",
        data={
            "username": "nonexistent@example.com",
            "password": "TestPassword123!"
        }
    )

    assert response.status_code == 401



def test_login_without_password(client):
    response = client.post(
        "/auth/login",
        data={
            "username": "test@example.com"
        }
    )

    assert response.status_code == 422



def test_create_expense_with_negative_amount(client):
    user_data = {
        "email": "negativeamount@example.com",
        "password": "TestPassword123!"
    }

    client.post("/auth/register", json=user_data)

    login_response = client.post(
        "/auth/login",
        data={
            "username": user_data["email"],
            "password": user_data["password"]
        }
    )

    token = login_response.json()["access_token"]

    response = client.post(
        "/expenses/",
        json={
            "description": "Invalid expense",
            "amount": -100.00,
            "date": "2026-11-12"
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 422


def test_partially_update_expense_with_negative_amount(client):
    user_data = {
        "email": "negativeupdate@example.com",
        "password": "TestPassword123!"
    }

    client.post("/auth/register", json=user_data)

    login_response = client.post(
        "/auth/login",
        data={
            "username": user_data["email"],
            "password": user_data["password"]
        }
    )

    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    create_response = client.post(
        "/expenses/",
        json={
            "description": "Valid expense",
            "amount": 100.00,
            "date": "2026-11-12"
        },
        headers=headers
    )

    expense_id = create_response.json()["id"]

    response = client.patch(
        f"/expenses/{expense_id}",
        json={"amount": -50.00},
        headers=headers
    )

    assert response.status_code == 422