import pytest
from your_app import register_user


@pytest.fixture
def valid_user_data():
    return {
        "username": "johndoe",
        "password": "password123",
        "email": "johndoe@example.com",
        "subscribe_newsletter": True
    }


def test_successful_registration(valid_user_data):
    """
       Objective: Tests a successful registration with valid input values.
    """
    result = register_user(**valid_user_data)
    assert result == "Registration successful"


@pytest.mark.parametrize("field_to_remove", ["username", "password", "email"])
def test_missing_required_field(valid_user_data, field_to_remove):
    """
       Objective: Tests the case when the required field is missing.
    """
    valid_user_data.pop(field_to_remove)
    with pytest.raises(ValueError) as exc_info:
        register_user(**valid_user_data)
    assert str(exc_info.value) == f"{field_to_remove.capitalize()} is required"


def test_invalid_email_format(valid_user_data):
    """
       Objective: Tests the case when the email format is invalid.
    """

    valid_user_data["email"] = "johndoe@example"
    with pytest.raises(ValueError) as exc_info:
        register_user(**valid_user_data)
    assert str(exc_info.value) == "Invalid email format"


def test_username_already_exists(valid_user_data):
    """
       Objective: Tests the case when the username already exists.
    """

    valid_user_data["username"] = "existinguser"
    with pytest.raises(ValueError) as exc_info:
        register_user(**valid_user_data)
    assert str(exc_info.value) == "Username already exists"


def test_password_too_short(valid_user_data):
    """
       Objective: Tests the case when the password is too short.
    """

    valid_user_data["password"] = "pass"
    with pytest.raises(ValueError) as exc_info:
        register_user(**valid_user_data)
    assert str(exc_info.value) == "Password must be at least 8 characters long"


def test_long_username(valid_user_data):
    """
       Objective: Tests the case when the username exceeds the maximum allowed length.
    """

    valid_user_data["username"] = "a" * 51
    with pytest.raises(ValueError) as exc_info:
        register_user(**valid_user_data)
    assert str(exc_info.value) == "Username cannot exceed 50 characters"


def test_subscribe_newsletter_false(valid_user_data):
    """
       Objective: Tests the case when the user opts out of subscribing to the newsletter.
    """

    valid_user_data["subscribe_newsletter"] = False
    result = register_user(**valid_user_data)
    assert result == "Registration successful"
