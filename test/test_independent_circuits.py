import pytest
from src.UserManager import UserManager


class TestUserManagerCircuits:

    def setup_method(self):
        self.um = UserManager()
        # Preload with an existing user to test duplication
        self.um.create_user(
            email="existing@example.com",
            username="existinguser",
            country="Romania",
            phone_number="+40 712345678",
            birth_date_str="1990-01-01"
        )

    @pytest.mark.parametrize(
        "email, username, birth_date_str, phone_number, country, expected_status, expected_msg",
        [
            # Path A: All valid
            ("john@example.com", "validUser", "1990-01-01",
             "+40 712345678", "Romania", 200, "User successfully created"),

            # Path B: Invalid birth date format
            ("badformat@example.com", "validUser", "1990/01/01",
             "+40 712345678", "Romania", 400, "Invalid birth date"),

            # Path C: Future birth date
            ("future@example.com", "validUser", "2099-01-01",
             "+40 712345678", "Romania", 400, "Birth date is in the future"),

            # Path D: Invalid email format
            ("invalidemail", "validUser", "1990-01-01",
             "+40 712345678", "Romania", 400, "Invalid email"),

            # Path E: Duplicate email
            ("existing@example.com", "newuser", "1990-01-01",
             "+40 712345678", "Romania", 400, "Email already exists"),

            # Path F: Username too short
            ("short@example.com", "ab", "1990-01-01",
             "+40 712345678", "Romania", 400, "Username too short"),

            # Path G: Username too long
            ("long@example.com", "a" * 25, "1990-01-01",
             "+40 712345678", "Romania", 400, "Username too long"),

            # Path H: Invalid phone prefix
            ("wrongprefix@example.com", "validUser", "1990-01-01", "+33 712345678",
             "Romania", 400, "Phone number prefix does not match"),

            # Path I: Phone number doesn't match any known prefix
            ("unknownprefix@example.com", "validUser", "1990-01-01",
             "1234567890", "Romania", 400, "Phone number prefix does not match"),
        ]
    )
    def test_independent_circuits(self, email, username, birth_date_str, phone_number, country, expected_status, expected_msg):
        status, msg = self.um.create_user(
            email=email,
            username=username,
            birth_date_str=birth_date_str,
            phone_number=phone_number,
            country=country
        )
        assert status == expected_status
        assert expected_msg in msg
