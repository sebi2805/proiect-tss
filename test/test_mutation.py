import pytest
from src.UserManager import UserManager 


class TestMutationAdditonal:
        
    @pytest.fixture(autouse=True)
    def setup_manager(self):
        self.um = UserManager()

    @pytest.mark.parametrize(
        "email, username, birth_date_str, phone_number, country, expected_status, expected_msg_fragment",
        [
            ("john.doe@example.com", "john_doe", "1990-05-10", "+40 712345678", "Romania", 200, "User successfully created"),
            ("john.doe@example.com", "john_doe", "1990-05-10", "+1 712345678", "USA", 200, "User successfully created"),
            ("john.doe@example.com", "john_doe", "1990-05-10", "+44 712345678", "UK", 200, "User successfully created"),
            ("john.doe@example.com", "john_doe", "1990-05-10", "+33 712345678", "France", 200, "User successfully created"),
            ("john.doe@example.com", "john_doe", "1990-05-10", "+49 712345678", "Germany", 200, "User successfully created"),
            ("john.doe@example.com", "john_doe", "1990-05-10", "+39 712345678", "Italy", 200, "User successfully created"),
            ("john.doe@example.com", "john_doe", "1990-05-10", "+34 712345678", "Spain", 200, "User successfully created"),
            ("john.doe@example.com", "john_doe", "1990-05-10", "+5 712345678", "Canada", 200, "User successfully created"),
            ("john.doe@example.com", "john_doe", "1990-05-10", "+61 712345678", "Australia", 200, "User successfully created"),
            ("john.doe@example.com", "john_doe", "1990-05-10", "+91 712345678", "India", 200, "User successfully created"),
        ]
    )
    def test_countries(self, email, username, birth_date_str, phone_number, country, expected_status, expected_msg_fragment):
        status, msg = self.um.create_user(
            email=email,
            username=username,
            birth_date_str=birth_date_str,
            phone_number=phone_number,
            country=country
        )
        assert status == expected_status
        assert expected_msg_fragment in msg

    def test_phone_prefix(self):
        status, msg = self.um.create_user(
                email="country.doe@example.com", username="country_user", 
                birth_date_str="1990-05-10", phone_number="+40 712345678", country="Mars"
        )
        assert status == 400
        assert "Phone number prefix does not match the country" == msg

    def test_email_already_exists(self):
        status, msg = self.um.create_user(
            email="existing.user@example.com",
            username="existinguser",
            birth_date_str="1990-05-10",
            phone_number="+40 712345678",
            country="Romania"
        )
        assert status == 200

        status, msg = self.um.create_user(
            email="existing.user@example.com",
            username="newuser",
            birth_date_str="1992-08-20",
            phone_number="+40 712345679",
            country="Romania"
        )
        assert status == 400
        assert "Email already exists" == msg