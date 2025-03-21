import pytest
from datetime import datetime, timedelta
from src.UserManager import UserManager

class TestUserManager:
    @pytest.fixture(autouse=True)
    def setup_manager(self):
        self.um = UserManager()

    def test_valid_user_creation(self):
        status, msg = self.um.create_user(
            email="john.doe@example.com",
            username="john_doe",
            country="Romania",
            phone_number="+40 712345678",
            birth_date_str="1990-05-10"
        )
        assert status == 200
        assert msg == "User successfully created"

    def test_invalid_email_format(self):
        status, msg = self.um.create_user(
            email="john.doeexample.com",
            username="john_doe",
            country="Romania",
            phone_number="+40 712345678",
            birth_date_str="1990-05-10"
        )
        assert status == 400
        assert "Invalid email" in msg

    def test_duplicate_email(self):
        # just make sure to create 2 users in sequence with the same email
        self.um.create_user(
            email="john.doe@example.com",
            username="john_doe",
            country="Romania",
            phone_number="+40 712345678",
            birth_date_str="1990-05-10"
        )
        status, msg = self.um.create_user(
            email="john.doe@example.com",
            username="johnny",
            country="Romania",
            phone_number="+40 712345679",
            birth_date_str="1991-06-15"
        )
        assert status == 400
        assert "Email already exists" in msg

    def test_username_too_short(self):

        status, msg = self.um.create_user(
            email="jane.doe@example.com",
            username="ab",
            country="Romania",
            phone_number="+40 712345678",
            birth_date_str="1985-08-20"
        )
        assert status == 400
        assert "Username too short" in msg

    def test_username_too_long(self):
        status, msg = self.um.create_user(
            email="jane.doe2@example.com",
            #  i think the easiest way is to do it like like, we can also use 
            # list comprehension I think with a range
            username="a" * 21,
            country="Romania",
            phone_number="+40 712345678",
            birth_date_str="1985-08-20"
        )
        assert status == 400
        assert "Username too long" in msg

    def test_invalid_birth_date_format(self):
        status, msg = self.um.create_user(
            email="jack.doe@example.com",
            username="jack_doe",
            country="Romania",
            phone_number="+40 712345678",
            birth_date_str="1990/05/10" 
        )
        assert status == 400
        assert "Invalid birth date" in msg

    def test_birth_date_in_future(self):
        future_date = (datetime.today() + timedelta(days=1)).strftime("%Y-%m-%d")
        status, msg = self.um.create_user(
            email="future.doe@example.com",
            username="future_user",
            country="Romania",
            phone_number="+40 712345678",
            birth_date_str=future_date
        )
        assert status == 400
        assert "Birth date is in the future" in msg

    def test_invalid_phone_prefix(self):
        status, msg = self.um.create_user(
            email="phone.doe@example.com",
            username="phone_user",
            country="Romania",
            phone_number="+33 712345678",
            birth_date_str="1990-05-10"
        )
        assert status == 400
        assert "Phone number prefix does not match the country" in msg
