import pytest

from app.users.dao import UsersDAO


@pytest.mark.parametrize("user_id,email,exist", [
    (1, "test@test.com", True), 
    (2, "artem@example.com", True),
    (3, "nonexistent@example.com", False)
    ])
async def test_find_user_by_id(user_id, email, exist):
    user = await UsersDAO.find_by_id(user_id)

    if exist:
        assert user
        assert user.id == user_id
        assert user.email == email
    else:
        assert not user


