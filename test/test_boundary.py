import pytest
from datetime import datetime
from src.UserManager import UserManager


class TestUserManagerBoundary:
    @pytest.fixture(autouse=True)
    def setup_manager(self):
        self.um = UserManager()

    def test_boundary_username_min(self):
        status, msg = self.um.create_user(
            email="test_min@example.com",
            username="aaa",  # Lower boundary (too short)
            country="Romania",
            phone_number="+40 712345678",
            birth_date_str="2003-02-26"
        )
        assert status == 400
        assert "Username too short" == msg

    def test_boundary_username_min_valid(self):
        status, msg = self.um.create_user(
            email="test_valid_min@example.com",
            username="aaaa",  # Just valid
            country="Romania",
            phone_number="+40 712345678",
            birth_date_str="2003-02-26"
        )
        assert status == 200
        assert "User successfully created" == msg

    def test_boundary_username_max_valid(self):
        status, msg = self.um.create_user(
            email="test_valid_max@example.com",
            username="a" * 19,  # Just valid max
            country="Romania",
            phone_number="+40 712345678",
            birth_date_str="2003-02-26"
        )
        assert status == 200
        assert "User successfully created" == msg

    def test_boundary_username_max(self):
        status, msg = self.um.create_user(
            email="test_max@example.com",
            username="a" * 20,  # Upper boundary (too long)
            country="Romania",
            phone_number="+40 712345678",
            birth_date_str="2003-02-26"
        )
        assert status == 400
        assert "Username too long" == msg

    def test_boundary_birth_date_min(self):
        today = datetime.today().strftime("%Y-%m-%d")
        status, msg = self.um.create_user(
            email="future@example.com",
            username="future_user",
            country="Romania",
            phone_number="+40 712345678",
            birth_date_str=today  # Minimum invalid (today)
        )
        assert status == 400
        assert "Birth date is in the future" == msg

    def test_boundary_birth_date_max(self):
        old_date = "1900-01-01"
        status, msg = self.um.create_user(
            email="old@example.com",
            username="old_user",
            country="Romania",
            phone_number="+40 712345678",
            birth_date_str=old_date  # Extreme valid old date
        )
        assert status == 200
        assert "User successfully created" == msg

    def test_boundary_email_format(self):
        status, msg = self.um.create_user(
            email="a@b.c",  # Minimal valid email
            username="minimal_email",
            country="Romania",
            phone_number="+40 712345678",
            birth_date_str="2003-02-26"
        )
        assert status == 200
        assert "User successfully created" == msg
