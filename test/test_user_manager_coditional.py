import pytest
from datetime import datetime, timedelta

from src.UserManager import UserManager
from src.User import User


class TestUserManagerConditionCoverage:
    """Condition coverage - each predicate T / F."""

    @pytest.fixture(autouse=True)
    def _setup_manager(self):
        self.um = UserManager()


    @pytest.mark.parametrize(
        "preload, probe, expected",
        [
            # E1: already exists (condition True)
            (["exists@example.com"], "exists@example.com", True),
            # E2: does not exist (condition False)
            ([], "ghost@example.com", False),
        ],
    )
    def test_email_exists_condition(self, preload, probe, expected):
        for mail in preload:
            self.um.users.append(
                User(mail, "u", "Romania", "+40123456789", datetime(2000, 1, 1).date())
            )
        assert self.um.email_exists(probe) is expected


    @pytest.mark.parametrize(
        "email, expected",
        [
            # VE1: correct format
            ("good@mail.com", True),
            # VE2: incorrect format
            ("badmail", False),
        ],
    )
    def test_validate_email_condition(self, email, expected):
        assert self.um.validate_email(email) is expected


    @pytest.mark.parametrize(
        "phone, country, expected",
        [
            # VP1: prefix +40 & country RO  (True ∧ True)
            ("+40123456789", "Romania", True),
            # VP2: prefix +40 but country DE (True ∧ False)
            ("+40123456789", "Germany", False),
            # VP3: unknown prefix        (False ∧ _ )
            ("123456", "Romania", False),
        ],
    )
    def test_validate_phone_prefix_conditions(self, phone, country, expected):
        assert self.um.validate_phone_prefix(phone, country) is expected

    @pytest.mark.parametrize(
        "email, username, country, phone, bdate, exp_status, exp_msg",
        [
            # CU1 – invalid email (validate_email == False)
            ("badmail", "validuser", "Romania", "+40123456789", "2000-01-01",
             400, "Invalid email"),

            # CU2 – invalid date (format)
            ("ok@mail.com", "validuser", "Romania", "+40123456789", "not-a-date",
             400, "Invalid birth date"),

            # CU3 – date in the future
            ("ok@mail.com", "validuser", "Romania", "+40123456789",
             (datetime.today() + timedelta(days=1)).strftime("%Y-%m-%d"),
             400, "Birth date is in the future"),

            # CU4 – username too short
            ("u1@mail.com", "usr", "Romania", "+40123456789", "2000-01-01",
             400, "Username too short"),

            # CU5 – username too long
            ("u2@mail.com", "u" * 21, "Romania", "+40123456789", "2000-01-01",
             400, "Username too long"),

            # CU6 – prefix does not match the country
            ("u3@mail.com", "validuser", "Germany", "+40123456789", "2000-01-01",
             400, "Phone number prefix does not match the country"),

            # CU7 – completely unknown prefix
            ("u4@mail.com", "validuser", "Romania", "12345678", "2000-01-01",
             400, "Phone number prefix does not match the country"),

            # CU8 – email already exists
            ("dup@mail.com", "validuser", "Romania", "+40123456789", "2000-01-01",
             400, "Email already exists"),

            # CU9 – happy-path, everything valid
            ("new@mail.com", "validuser", "Romania", "+40123456789", "2000-01-01",
             200, "User successfully created"),
        ],
    )
    def test_create_user_conditions(self, email, username, country,
                                    phone, bdate, exp_status, exp_msg):
        # pre-populate for the duplicate-mail scenario
        if exp_msg == "Email already exists":
            self.um.users.append(
                User(email, "old", country, phone, datetime(1990, 1, 1).date())
            )

        status, msg = self.um.create_user(
            email=email,
            username=username,
            country=country,
            phone_number=phone,
            birth_date_str=bdate,
        )

        assert status == exp_status
        assert exp_msg in msg

        # check persisted effect in the CU9 scenario
        if exp_status == 200:
            assert any(u.email == email for u in self.um.users)