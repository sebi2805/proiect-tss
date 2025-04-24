
import pytest
from src.UserManager import UserManager

class TestUserManagerDecisionCoverage:
    @pytest.fixture(autouse=True)
    def setup_manager(self):
        self.um = UserManager()

    def test_email_exists_with_non_matching_email(self):
        self.um.create_user(
            email="existing@example.com",
            username="user1",
            country="Romania",
            phone_number="+40 712345678",
            birth_date_str="2000-01-01"
        )
        # This email does not match existing user
        assert not self.um.email_exists("nonexistent@example.com")

    def test_validate_phone_prefix_no_match(self):
        # Using a prefix not in the mapping
        assert not self.um.validate_phone_prefix("+999 123456789", "NowhereLand")

    def test_username_exactly_3_characters(self):
        status, msg = self.um.create_user(
            email="test3char@example.com",
            username="abc",  # exactly 3 characters
            country="Germany",
            phone_number="+49 1234567890",
            birth_date_str="1990-01-01"
        )
        assert status == 400
        assert "Username too short" in msg

    def test_birth_date_exact_today(self):
        from datetime import datetime
        today_str = datetime.today().strftime("%Y-%m-%d")
        status, msg = self.um.create_user(
            email="today@example.com",
            username="todayuser",
            country="India",
            phone_number="+91 9876543210",
            birth_date_str=today_str
        )
        assert status == 400
        assert "Birth date is in the future" in msg

    def test_success_path_user_creation(self):
        status, msg = self.um.create_user(
            email="success@example.com",
            username="happy_user",
            country="Canada",
            phone_number="+1 2345678901",
            birth_date_str="1980-01-01"
        )
        assert status == 200
        assert msg == "User successfully created"
