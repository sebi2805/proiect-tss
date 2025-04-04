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

Using GithubCopilor, the prompt used for generating the test case was:

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





## Boundary Value Analysis

### Our code

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
    assert not um.validate_phone_prefix("+999999", "Neverland")

```


