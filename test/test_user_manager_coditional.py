import pytest
from datetime import datetime, timedelta
from src.UserManager import UserManager
from src.User import User

@pytest.fixture
def user_manager():
    return UserManager()

def test_email_exists_true(user_manager):
    user_manager.users.append(User("existing@example.com", "u1", "Romania", "+40123456789", datetime(2000, 1, 1).date()))
    assert user_manager.email_exists("existing@example.com") is True

def test_email_exists_false(user_manager):
    assert user_manager.email_exists("nonexisting@example.com") is False

def test_validate_email_valid(user_manager):
    assert user_manager.validate_email("valid@email.com") is True

def test_validate_email_invalid(user_manager):
    assert user_manager.validate_email("invalidemail") is False

def test_phone_prefix_match_true(user_manager):
    assert user_manager.validate_phone_prefix("+40123456789", "Romania") is True

def test_phone_prefix_match_false_prefix_true_country_false(user_manager):
    assert user_manager.validate_phone_prefix("+40123456789", "Germany") is False

def test_phone_prefix_match_false_prefix_false(user_manager):
    assert user_manager.validate_phone_prefix("123456", "Romania") is False


def test_create_user_invalid_date_format(user_manager):
    status, msg = user_manager.create_user("a@a.com", "validuser", "Romania", "+40123456789", "not-a-date")
    assert status == 400 and msg == "Invalid birth date"

def test_create_user_future_birth_date(user_manager):
    future_date = (datetime.today() + timedelta(days=1)).strftime("%Y-%m-%d")
    status, msg = user_manager.create_user("a@a.com", "validuser", "Romania", "+40123456789", future_date)
    assert status == 400 and msg == "Birth date is in the future"

def test_create_user_invalid_email(user_manager):
    status, msg = user_manager.create_user("invalidemail", "validuser", "Romania", "+40123456789", "2000-01-01")
    assert status == 400 and msg == "Invalid email"

def test_create_user_existing_email(user_manager):
    user_manager.users.append(User("existing@example.com", "u1", "Romania", "+40123456789", datetime(2000, 1, 1).date()))
    status, msg = user_manager.create_user("existing@example.com", "validuser", "Romania", "+40123456789", "2000-01-01")
    assert status == 400 and msg == "Email already exists"

def test_create_user_username_too_short(user_manager):
    status, msg = user_manager.create_user("a@a.com", "usr", "Romania", "+40123456789", "2000-01-01")
    assert status == 400 and msg == "Username too short"

def test_create_user_username_too_long(user_manager):
    long_username = "u" * 21
    status, msg = user_manager.create_user("a@a.com", long_username, "Romania", "+40123456789", "2000-01-01")
    assert status == 400 and msg == "Username too long"

def test_create_user_invalid_phone_prefix(user_manager):
    status, msg = user_manager.create_user("a@a.com", "validuser", "Germany", "+40123456789", "2000-01-01")
    assert status == 400 and msg == "Phone number prefix does not match the country"

def test_create_user_prefix_not_in_list(user_manager):
    status, msg = user_manager.create_user("a@a.com", "validuser", "Romania", "12345678", "2000-01-01")
    assert status == 400 and msg == "Phone number prefix does not match the country"

def test_create_user_success(user_manager):
    status, msg = user_manager.create_user("new@user.com", "validuser", "Romania", "+40123456789", "2000-01-01")
    assert status == 200 and msg == "User successfully created"
    assert len(user_manager.users) == 1
    assert user_manager.users[0].email == "new@user.com"
