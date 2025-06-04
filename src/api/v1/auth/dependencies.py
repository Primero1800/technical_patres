from src.api.v1.auth.backend import fastapi_users


current_user = fastapi_users.current_user(
    active=True,
    verified=True,
)
