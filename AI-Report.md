# AI-Report

We are having the context of the project and the tests that are implemented in the test folder.

We will compare our tests with AI-generated tests to see if they are better or worse. We will use tools like Github Copilot and ChatGPT to generate the tests.

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
