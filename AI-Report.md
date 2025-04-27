# AI-Report

We are having the context of the project and the tests that are implemented in the test folder.

We will compare our tests with AI-generated tests to see if they are better or worse. We will use tools like Github Copilot and ChatGPT to generate the tests.

## Class Equivalence Analysis

### Our code

```python
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

```

### AI Generated-code

Using GithubCopilot, the prompt used for generating the test case was:

`Generate a class equivalence‑analysis test suite for the UserManager class. Write a concise set of tests that together cover the entire input domain.`

```python
import pytest
from datetime import datetime, timedelta

from src.UserManager import UserManager

@pytest.fixture
def um():
    return UserManager()

# ==== 1. Equivalence classes for email ====
@pytest.mark.parametrize(
    "email, expected",
    [
        ("user@example.com", True),      # valid
        ("user.name+tag@domain.co", True), # valid complex
        ("no-at-sign.com", False),       # invalid: missing '@'
        ("@no-local-part.com", False),   # invalid: missing local
        ("user@.com", False),            # invalid: domain starts with dot
    ],
)
def test_validate_email(um, email, expected):
    assert um.validate_email(email) is expected

# ==== 2. Equivalence classes for phone prefix ====
@pytest.mark.parametrize(
    "phone, country, expected",
    [
        ("+40 712345678", "Romania", True),   # valid RO
        ("+49 1234567", "Germany", True),     # valid DE
        ("+40 712345678", "USA", False),      # valid USA
        ("0712345678", "Romania", False),     # missing '+'
        ("+999123", "Unknown", False),        # unsupported code
    ],
)
def test_validate_phone_prefix(um, phone, country, expected):
    assert um.validate_phone_prefix(phone, country) is expected

# ==== 3. Equivalence classes for birth_date_str ====
@pytest.mark.parametrize(
    "bd_str, expected_code, expected_msg",
    [
        # valid past date
        ("2000-01-01", 200, "User successfully created"),
        # invalid format
        ("01-01-2000", 400, "Invalid birth date"),
        # future date
        ((datetime.today() + timedelta(days=1)).strftime("%Y-%m-%d"), 400, "Birth date is in the future"),
    ],
)
def test_birth_date_classes(um, bd_str, expected_code, expected_msg):
    code, msg = um.create_user(
        email="e@t.co",
        username="validuser",
        country="Romania",
        phone_number="+40 712345678",
        birth_date_str=bd_str,
    )
    assert code == expected_code
    assert expected_msg in msg

# ==== 4. Equivalence classes for username length ====
@pytest.mark.parametrize(
    "username, expected_code, expected_msg",
    [
        ("usr",        400, "Username too short"),  # <= 3
        ("user4",      200, "User successfully created"),  # between 4–19
        ("a" * 19,     200, "User successfully created"),  # upper valid
        ("a" * 20,     400, "Username too long"),   # >= 20
    ],
)
def test_username_length(um, username, expected_code, expected_msg):
    code, msg = um.create_user(
        email="u@e.com",
        username=username,
        country="Romania",
        phone_number="+40 712345678",
        birth_date_str="1995-05-05",
    )
    assert code == expected_code
    assert expected_msg in msg

# ==== 5. Equivalence classes for duplicate email ====
def test_email_exists(um):
    # creare inițială
    um.create_user("dup@e.com", "dupuser", "Romania", "+40 712345678", "1990-01-01")
    # încercare duplicat
    code, msg = um.create_user("dup@e.com", "other", "Romania", "+40 712345678", "1990-01-01")
    assert code == 400
    assert "Email already exists" in msg

# ==== 6. Happy path end‑to‑end ====
def test_full_valid_user(um):
    code, msg = um.create_user(
        email="good@e.com",
        username="gooduser",
        country="Germany",
        phone_number="+49 123456789",
        birth_date_str="1985-12-12",
    )
    assert code == 200
    assert msg == "User successfully created"

```

As you can observe, the generated code isn't really tight to class equivalence testing, it is more related to general testing. Moreover, when it is testing the phone number format for USA, the test is wrong because the test should fail.

---

## Boundary Value Analysis

### Our code

We'll look at an upper boundary value analysis test case for the `username` field in the `UserManager` class. The username is expected to be between 1 and 20 characters long.

```python

def test_boundary_username_max_valid(self):
    status, msg = self.um.create_user(
        email="test_valid_max@example.com",
        username="a" * 19,  # Just valid max
        country="Romania",
        phone_number="+40 712345678",
        birth_date_str="2003-02-26"
    )
    assert status == 200
    assert "User successfully created" in msg

def test_boundary_username_max(self):
    status, msg = self.um.create_user(
        email="test_max@example.com",
        username="a" * 20,  # Upper boundary (too long)
        country="Romania",
        phone_number="+40 712345678",
        birth_date_str="2003-02-26"
    )
    assert status == 400
    assert "Username too long" in msg
```

This test case checks the upper boundary of the username length. The expected behavior is that the system should return a status code of 400 and an appropriate error message indicating that the username is too long.

### AI-generated code

Using GithubCopilot, the prompt used for generating the test case was:

`Generate a boundary value analysis test only for the upper boundary of the username, having the context of UserManager class.`

The result was the following:

```python

def test_username_upper_boundary_valid(user_manager):
    # Test with a username of exactly 19 characters (valid case)
    status, message = user_manager.create_user(
        email="test@example.com",
        username="a" * 19,  # 19 characters
        country="USA",
        phone_number="+11234567890",
        birth_date_str="2000-01-01"
    )
    assert status == 200
    assert message == "User successfully created"

def test_username_upper_boundary_invalid(user_manager):
    # Test with a username of exactly 20 characters (invalid case)
    status, message = user_manager.create_user(
        email="test2@example.com",
        username="a" * 20,  # 20 characters
        country="USA",
        phone_number="+11234567890",
        birth_date_str="2000-01-01"
    )
    assert status == 400
    assert message == "Username too long"

```

An interesting observation is that the AI-generated test case includes both a valid and an invalid case for the upper boundary of the username length without specifying that in the prompt.

The generated code looks quite similar to the one we wrote, it only has a few more comments and data specific to another region (USA).

---

## Boundary Value Analysis

### Our code

We will create two different tests: the first will check whether a given email is already present in the user list, and the second will verify the validity of a given phone prefix.

```python
def test_email_exists_with_non_matching_email():
    um = UserManager()
    um.create_user(
        email="existing@example.com",
        username="user1",
        country="Romania",
        phone_number="+40 712345678",
        birth_date_str="2000-01-01"
    )
    # This email does not match existing user
    assert not um.email_exists("nonexistent@example.com")


def test_validate_phone_prefix_no_match():
    um = UserManager()
    # Country prefix that isn't mapped
    assert not um.validate_phone_prefix("+999999", "TestTest")

```

### AI-generated code

The following prompt was given to ChatGPT's GPT-4o model:

`For the provided UserManager.py file, can you generate test cases to ensure decision-based coverage?`

This was the result:

```python
def test_email_exists_with_non_matching_email():
    """
    This test checks that the email_exists method correctly identifies that
    a given email is not already present in the user list.
    """
    # Create an instance of UserManager
    user_manager = UserManager()

    # First, add a user with a known email to simulate existing data
    user_manager.create_user(
        email="existing.user@example.com",
        username="existing_user",
        country="USA",
        phone_number="+1 5551234567",
        birth_date_str="1990-01-01"
    )

    # Now, check for a different email that should not be found in the system
    email_check = user_manager.email_exists("not.found@example.com")

    # Assert that the non-existent email returns False
    assert email_check is False


def test_validate_phone_prefix_no_match():
    """
    This test ensures that validate_phone_prefix returns False when the
    phone number prefix does not correspond to any known country.
    """
    # Instantiate a new UserManager object
    user_manager = UserManager()

    # Define a phone number with a prefix not included in the mapping
    invalid_phone_number = "+999 5551234567"
    unknown_country = "Atlantis"

    # Call the validation method with the unknown prefix and country
    is_valid = user_manager.validate_phone_prefix(invalid_phone_number, unknown_country)

    # Assert that the validation fails, as expected
    assert is_valid is False

```

The AI-provided code contains more comments, offering both a summary of each method and line-by-line explanations where necessary. Additionally, it includes more generic examples than our own.

---

## Statement Analisys

### Our code

We'll look at birth date test that checks if the value entered by the user is in the future. This checks the `birth_date` field in the `User` class.
The birth date is expected to be in the past.

```python

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

```

These test cases check if the birth date entered by the user is valid (not in the future). For birth dates in the future we expect a status code 400
and an appropiate error message.

### AI-generated code

Using GithubCopilot, the prompt used for generating the test case was:

`Generate statement analisys tests for the validation of the birth date. Use the UserManager class as context.`

The result was the following:

```python

def test_valid_birth_date(user_manager):
    """Test that a valid birth date is accepted."""
    valid_date = "2000-12-31"
    status, message = user_manager.create_user(
        email="test@example.com",
        username="testuser",
        country="USA",
        phone_number="+1234567890",
        birth_date_str=valid_date
    )
    assert status == 200
    assert message == "User successfully created"

def test_birth_date_in_future(self):
    """Test that a birth date in the future is rejected."""
    future_date = (datetime.today() + timedelta(days=1)).strftime("%Y-%m-%d")
    status, message = self.user_manager.create_user(
        email="test@example.com",
        username="testuser",
        country="USA",
        phone_number="+1234567890",
        birth_date_str=future_date
    )
    self.assertEqual(status, 400)
    self.assertEqual(message, "Birth date is in the future")

```

We observed that the code generated by GitHub Copilot correctly generates the tests for the birth_date field, but it failed to also check the other fields. For example, the phone number that is generated doesn't have a valid prefix, so the test for a valid birth date will fail because that field validation. We also saw some regional differences, Copilot assumed that our user is located in USA and used the testuser username.

---

## Independent Circuit Testing

The test suite regarding independent circuits checks various input scenarios for creating a user using McCabe's complexity, ensuring different paths are validated for correctness. It includes tests for valid and invalid email formats, birth dates, usernames, and phone numbers, as well as duplicate entries.

Each test corresponds to an independent circuit in the system, verifying different conditions and their expected results. The test uses pytest.mark.parametrize to run these scenarios with different inputs, ensuring 100% coverage of the decision points in the code.

### Our code

```python
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
```

## AI-generated code

Using GithubCopilot, the prompt used for generating the test case was:

`Generate Independent Circuit Tests based on McCabe's Cyclomatic Complexity formula for this UserManager class.`

The result was the following:

At first it started explaining the McCabe's Cyclomatic Complexity formula:

```
To generate independent circuit tests based on McCabe's Cyclomatic Complexity formula, we first calculate the cyclomatic complexity of the UserManager class. Cyclomatic complexity is calculated as:

Where:

E = Number of edges in the control flow graph.
N = Number of nodes in the control flow graph.
P = Number of connected components (usually 1 for a single function).
Step 1: Analyze the create_user method
The create_user method is the most complex method in the UserManager class. Let's count the decision points:

try-except block (1 decision point).
if birth_date >= datetime.today().date() (1 decision point).
if not self.validate_email(email) (1 decision point).
if self.email_exists(email) (1 decision point).
if len(username) <= 3 (1 decision point).
if len(username) >= 20 (1 decision point).
if not self.validate_phone_prefix(phone_number, country) (1 decision point).
Total decision points = 7.

Cyclomatic complexity = 7 + 1 (entry point) = 8.

This means we need 8 independent test cases to cover all paths.
```

We see a difference in our calculus, since we have 9 independent tests to cover all paths.

Then it generated the following code:

```python
import pytest
from datetime import datetime, timedelta
from src.UserManager import UserManager

@pytest.fixture
def user_manager():
    return UserManager()

def test_valid_user_creation(user_manager):
    # Valid user creation
    status, message = user_manager.create_user(
        email="test@example.com",
        username="validuser",
        country="USA",
        phone_number="+11234567890",
        birth_date_str="2000-01-01"
    )
    assert status == 200
    assert message == "User successfully created"

def test_invalid_birth_date_format(user_manager):
    # Invalid birth date format
    status, message = user_manager.create_user(
        email="test@example.com",
        username="validuser",
        country="USA",
        phone_number="+11234567890",
        birth_date_str="01-01-2000"  # Invalid format
    )
    assert status == 400
    assert message == "Invalid birth date"

def test_birth_date_in_future(user_manager):
    # Birth date in the future
    future_date = (datetime.today() + timedelta(days=1)).strftime("%Y-%m-%d")
    status, message = user_manager.create_user(
        email="test@example.com",
        username="validuser",
        country="USA",
        phone_number="+11234567890",
        birth_date_str=future_date
    )
    assert status == 400
    assert message == "Birth date is in the future"

def test_invalid_email_format(user_manager):
    # Invalid email format
    status, message = user_manager.create_user(
        email="invalid-email",
        username="validuser",
        country="USA",
        phone_number="+11234567890",
        birth_date_str="2000-01-01"
    )
    assert status == 400
    assert message == "Invalid email"

def test_duplicate_email(user_manager):
    # Duplicate email
    user_manager.create_user(
        email="test@example.com",
        username="validuser",
        country="USA",
        phone_number="+11234567890",
        birth_date_str="2000-01-01"
    )
    status, message = user_manager.create_user(
        email="test@example.com",  # Duplicate email
        username="anotheruser",
        country="USA",
        phone_number="+11234567890",
        birth_date_str="2000-01-01"
    )
    assert status == 400
    assert message == "Email already exists"

def test_username_too_short(user_manager):
    # Username too short
    status, message = user_manager.create_user(
        email="test@example.com",
        username="abc",  # Too short
        country="USA",
        phone_number="+11234567890",
        birth_date_str="2000-01-01"
    )
    assert status == 400
    assert message == "Username too short"

def test_username_too_long(user_manager):
    # Username too long
    status, message = user_manager.create_user(
        email="test@example.com",
        username="a" * 20,  # Too long
        country="USA",
        phone_number="+11234567890",
        birth_date_str="2000-01-01"
    )
    assert status == 400
    assert message == "Username too long"

def test_invalid_phone_prefix(user_manager):
    # Phone number prefix does not match the country
    status, message = user_manager.create_user(
        email="test@example.com",
        username="validuser",
        country="USA",
        phone_number="+441234567890",  # UK prefix, but country is USA
        birth_date_str="2000-01-01"
    )
    assert status == 400
    assert message == "Phone number prefix does not match the country"
```

We actually ran the code and we got a 98% coverage, which is not bad, but it is not 100% as we expected.

This is the result of the code coverage:

```
Name                 Stmts   Miss  Cover   Missing
--------------------------------------------------
src\User.py              7      0   100%
src\UserManager.py      40      1    98%   38
src\__init__.py          0      0   100%
--------------------------------------------------
TOTAL                   47      1    98%
```

The AI-generated code is missing the test for the phone number that doesn't match any known prefix which is defined in line 38 of the UserManager class.

We can conclude that, in this case, the AI-generated code didn't compute correctly the cyclomatic complexity of the code and it didn't cover all the paths, but it was close to it.

---
