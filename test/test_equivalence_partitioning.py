import pytest
from src.UserManager import UserManager

class TestUserManagerEquivalencePartitioning:
    @pytest.fixture(autouse=True)
    def setup_manager(self):
        self.um = UserManager()

    @pytest.mark.parametrize(
        "email, username, birth_date_str, phone_number, country, expected_status, expected_msg_fragment",
        [
            # C_11111: All parameters valid (E1, U1, B1, P1, R1)
            ("john.doe@example.com", "john_doe", "1990-05-10", "+40 712345678", "Romania", 200, "User successfully created"),
            # C_21111: Invalid email (E2)
            ("johndoeexample.com", "john_doe", "1990-05-10", "+40 712345678", "Romania", 400, "Invalid email"),
            # C_12111: Username too short (U2)
            ("jane.doe@example.com", "ab", "1990-05-10", "+40 712345678", "Romania", 400, "Username too short"),
            # C_13111: Username too long (U3)
            ("jane.doe2@example.com", "a" * 21, "1990-05-10", "+40 712345678", "Romania", 400, "Username too long"),
            # C_11211: Birth date in incorrect format (B2)
            ("jack.doe@example.com", "jack_doe", "1990/05/10", "+40 712345678", "Romania", 400, "Invalid birth date"),
            # C_11311: Birth date in future (B3)
            ("future.doe@example.com", "future_user", "2090-05-10", "+40 712345678", "Romania", 400, "Birth date is in the future"),
            # C_11121: Invalid phone number (P2)
            ("phone.doe@example.com", "phone_user", "1990-05-10", "+33 712345678", "Romania", 400, "Phone number prefix does not match the country"),
            # C_11112: Invalid country (R2)
            # as it will not have a prefix
            ("country.doe@example.com", "country_user", "1990-05-10", "+40 712345678", "Mars", 400, "Phone number prefix does not match the country"),
        ]
    )
    def test_equivalence_classes(self, email, username, birth_date_str, phone_number, country, expected_status, expected_msg_fragment):
        status, msg = self.um.create_user(
            email=email,
            username=username,
            birth_date_str=birth_date_str,
            phone_number=phone_number,
            country=country
        )
        assert status == expected_status
        assert expected_msg_fragment in msg