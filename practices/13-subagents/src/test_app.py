from app import handle_request, reset_store, ApiRequest


class TestPostUsers:
    def setup_method(self):
        reset_store()

    def test_should_create_a_new_user(self):
        request = ApiRequest(
            method="POST",
            path="/users",
            body={"name": "Alice", "email": "alice@example.com"},
        )

        response = handle_request(request)
        assert response.status == 201
        assert response.body["name"] == "Alice"
        assert response.body["email"] == "alice@example.com"
        assert response.body["id"] is not None

    def test_should_return_400_for_missing_fields(self):
        request = ApiRequest(
            method="POST",
            path="/users",
            body={"name": "Alice"},
        )

        response = handle_request(request)
        assert response.status == 400


class TestGetUsers:
    def setup_method(self):
        reset_store()

    def test_should_return_all_users(self):
        handle_request(ApiRequest(
            method="POST",
            path="/users",
            body={"name": "Alice", "email": "alice@example.com"},
        ))
        handle_request(ApiRequest(
            method="POST",
            path="/users",
            body={"name": "Bob", "email": "bob@example.com"},
        ))

        response = handle_request(ApiRequest(method="GET", path="/users"))

        assert response.status == 200
        assert len(response.body) == 2

    def test_should_return_empty_list_when_no_users(self):
        response = handle_request(ApiRequest(method="GET", path="/users"))

        assert response.status == 200
        assert len(response.body) == 0


class TestGetUserById:
    def setup_method(self):
        reset_store()

    def test_should_return_a_specific_user(self):
        create_response = handle_request(ApiRequest(
            method="POST",
            path="/users",
            body={"name": "Alice", "email": "alice@example.com"},
        ))

        user_id = create_response.body["id"]
        response = handle_request(ApiRequest(
            method="GET",
            path=f"/users/{user_id}",
        ))

        assert response.status == 200
        assert response.body["name"] == "Alice"

    def test_should_return_404_for_non_existent_user(self):
        response = handle_request(ApiRequest(
            method="GET",
            path="/users/nonexistent",
        ))

        assert response.status == 404


class TestPutUser:
    def setup_method(self):
        reset_store()

    def test_should_update_a_user(self):
        create_response = handle_request(ApiRequest(
            method="POST",
            path="/users",
            body={"name": "Alice", "email": "alice@example.com"},
        ))

        user_id = create_response.body["id"]
        response = handle_request(ApiRequest(
            method="PUT",
            path=f"/users/{user_id}",
            body={"name": "Alice Updated"},
        ))

        assert response.status == 200
        assert response.body["name"] == "Alice Updated"
        assert response.body["email"] == "alice@example.com"


class TestDeleteUser:
    def setup_method(self):
        reset_store()

    def test_should_delete_a_user(self):
        create_response = handle_request(ApiRequest(
            method="POST",
            path="/users",
            body={"name": "Alice", "email": "alice@example.com"},
        ))

        user_id = create_response.body["id"]
        delete_response = handle_request(ApiRequest(
            method="DELETE",
            path=f"/users/{user_id}",
        ))

        assert delete_response.status == 204

        get_response = handle_request(ApiRequest(
            method="GET",
            path=f"/users/{user_id}",
        ))

        assert get_response.status == 404

    def test_should_return_404_for_non_existent_user(self):
        response = handle_request(ApiRequest(
            method="DELETE",
            path="/users/nonexistent",
        ))

        assert response.status == 404


class TestUnknownRoutes:
    def setup_method(self):
        reset_store()

    def test_should_return_404_for_unknown_routes(self):
        response = handle_request(ApiRequest(
            method="GET",
            path="/unknown",
        ))

        assert response.status == 404
