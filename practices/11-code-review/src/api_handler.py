# API Handler — intentionally contains multiple security and quality issues
# This code is for practice purposes. DO NOT use in production!

from typing import Any, Dict, List, Optional

# BUG: Hardcoded API key
API_KEY = "sk-secret-api-key-12345-do-not-share"
DB_PASSWORD = "admin123"


class User:
    def __init__(self, id: int, name: str, email: str, role: str) -> None:
        self.id = id
        self.name = name
        self.email = email
        self.role = role

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "role": self.role,
        }


class ApiResponse:
    def __init__(
        self,
        success: bool,
        data: Any = None,
        error: Optional[str] = None,
    ) -> None:
        self.success = success
        self.data = data
        self.error = error


# Simulated database
users: List[User] = [
    User(id=1, name="Alice", email="alice@example.com", role="admin"),
    User(id=2, name="Bob", email="bob@example.com", role="user"),
    User(id=3, name="Charlie", email="charlie@example.com", role="user"),
]


# BUG: No input validation, SQL-injection-like string interpolation
def search_users(query: str) -> ApiResponse:
    # Simulating SQL-injection-vulnerable query building
    sql_query = f"SELECT * FROM users WHERE name LIKE '%{query}%'"
    print(f"Executing query: {sql_query}")

    # Actually just filter in memory, but the SQL string is still dangerous if logged/sent
    results = [
        u.to_dict()
        for u in users
        if query.lower() in u.name.lower()
    ]

    return ApiResponse(success=True, data=results)


# BUG: No authentication check, returns sensitive data
def get_user_by_id(id: int) -> ApiResponse:
    user = next((u for u in users if u.id == id), None)

    if not user:
        # BUG: Leaking internal information in error message
        return ApiResponse(
            success=False,
            error=f"User not found in database table 'users' at index {id}. DB connection: {DB_PASSWORD}",
        )

    return ApiResponse(success=True, data=user.to_dict())


# BUG: No input validation, no error handling
def create_user(name: str, email: str) -> ApiResponse:
    # No validation of name or email
    # No check for duplicate emails
    # No sanitization

    new_user = User(
        id=len(users) + 1,  # BUG: ID collision if users are deleted
        name=name,
        email=email,
        role="user",
    )

    users.append(new_user)

    # BUG: Logging sensitive data
    print(f"Created user: {new_user.to_dict()}")

    return ApiResponse(success=True, data=new_user.to_dict())


# BUG: No authorization check — any user can delete any user
def delete_user(user_id: int) -> ApiResponse:
    index = next(
        (i for i, u in enumerate(users) if u.id == user_id), -1
    )

    if index == -1:
        return ApiResponse(success=False, error="User not found")

    # No check if the requester has permission to delete
    deleted = users.pop(index)

    return ApiResponse(success=True, data=deleted.to_dict())


# BUG: Hardcoded API key used directly, no rate limiting
def call_external_api(endpoint: str, data: Any) -> ApiResponse:
    # Using hardcoded API key
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }

    # No timeout setting
    # No retry logic
    # No rate limiting
    print(f"Calling {endpoint} with headers: {headers}")

    # Simulated response
    return ApiResponse(
        success=True,
        data={"message": "External API call simulated"},
    )


# BUG: Generic catch-all that swallows errors
def process_request(action: str, params: Dict[str, Any]) -> ApiResponse:
    try:
        if action == "search":
            return search_users(params["query"])
        elif action == "get":
            return get_user_by_id(params["id"])
        elif action == "create":
            return create_user(params["name"], params["email"])
        elif action == "delete":
            return delete_user(params["id"])
        elif action == "external":
            return call_external_api(params["endpoint"], params["data"])
        else:
            return ApiResponse(success=False, error="Unknown action")
    except Exception:
        # BUG: Swallowing error details, not logging properly
        return ApiResponse(success=False, error="Something went wrong")
