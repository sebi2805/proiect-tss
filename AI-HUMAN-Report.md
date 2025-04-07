# AI Report – Human vs AI on Condition Coverage

## Project Context

The project tests the business logic behind the `UserManager` class, responsible for creating users by validating email, username, phone prefix, and birth date. Tests are implemented using `pytest`, focusing not only on **statement and decision coverage**, but also pushing towards **full condition coverage**.

In this section, we compare **manually written tests** (by us) with **AI-generated tests** (via GitHub Copilot and ChatGPT) to evaluate their **thoroughness**, especially in capturing **atomic conditions**.

---

##  Condition Coverage (Acoperire la nivel de condiție)

### Our Code

To ensure **every atomic condition** is tested both as `True` and `False`, we explicitly added edge cases that exercise:

| Atomic Condition | Covered? |
|------------------|----------|
| `email == user.email` |  True / False |
| `re.match(...)` in `validate_email` |  Match / No match |
| `phone_number.startswith(prefix)` |  True / False |
| `country == c` in prefix check |  True / False |
| `birth_date >= today` |  True / False |
| `len(username) <= 3` and `>= 20` |  Both hit |
| `self.email_exists(email)` |  Yes / No |
| `validate_phone_prefix(...)` |  Valid / Invalid |
| `try/except` birth date format |  With and without error |

###  Sample: Our Tests for Phone Prefix Match

```python
def test_phone_prefix_match_true(user_manager):
    assert user_manager.validate_phone_prefix("+40123456789", "Romania") is True

def test_phone_prefix_match_false_prefix_true_country_false(user_manager):
    assert user_manager.validate_phone_prefix("+40123456789", "Germany") is False

def test_phone_prefix_match_false_prefix_false(user_manager):
    assert user_manager.validate_phone_prefix("123456", "Romania") is False
```

 We explicitly test when:
- Prefix is matched & country is matched
- Prefix is matched & country mismatched
- Prefix is not matched at all

This guarantees full **truth table** traversal — AI tools rarely go this far.

---

##  AI-Generated Code (GitHub Copilot)

**Prompt used:**  
`Generate condition coverage tests for create_user in UserManager.`

###  Copilot Output

```python
def test_valid_email(user_manager):
    status, msg = user_manager.create_user(
        "test@example.com", "user123", "USA", "+11234567890", "1990-01-01")
    assert status == 200

def test_invalid_email(user_manager):
    status, msg = user_manager.create_user(
        "testexample.com", "user123", "USA", "+11234567890", "1990-01-01")
    assert status == 400
```

###  Issues with AI Output:
- Only tests 1–2 conditions per run
- Assumes `USA` for everything → breaks prefix validation
- Does **not** test boundary conditions like username length or date format
- Doesn't handle `prefix matches but country != c`
- Fails condition coverage

---

##  Boundary Value Analysis: Username Field

###  Our Code

```python
def test_boundary_username_max_valid(self):
    status, msg = self.um.create_user(
        email="test_valid_max@example.com",
        username="a" * 19,
        country="Romania",
        phone_number="+40 712345678",
        birth_date_str="2003-02-26"
    )
    assert status == 200

def test_boundary_username_max(self):
    status, msg = self.um.create_user(
        email="test_max@example.com",
        username="a" * 20,
        country="Romania",
        phone_number="+40 712345678",
        birth_date_str="2003-02-26"
    )
    assert status == 400
    assert "Username too long" in msg
```

### AI Code from Copilot

```python
def test_username_upper_boundary_valid(user_manager):
    status, message = user_manager.create_user(
        "test@example.com", "a" * 19, "USA", "+11234567890", "2000-01-01")
    assert status == 200

def test_username_upper_boundary_invalid(user_manager):
    status, message = user_manager.create_user(
        "test2@example.com", "a" * 20, "USA", "+11234567890", "2000-01-01")
    assert status == 400
```

###  Our Advantage:
- We pair valid `username` values with **valid country+prefix**
- AI generated test fails due to bad phone prefix → result is inconclusive

---

##  Statement Analysis: Birth Date Field

### Our Code

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
```

###  Copilot’s Output

```python
def test_valid_birth_date(user_manager):
    valid_date = "2000-12-31"
    status, message = user_manager.create_user(
        email="test@example.com", username="testuser",
        country="USA", phone_number="+1234567890",
        birth_date_str=valid_date)
    assert status == 200
```

###  Problem:
- Phone number prefix is invalid for `USA`
- So test result fails before reaching the statement being tested (`birth_date >= today`)

---

##  Final Comparison

| Area | Our Code | AI Output | Verdict |
|------|----------|-----------|---------|
|  Condition Coverage | Full atomic condition control | Misses branches & combinations |  Ours wins |
|  Boundary Analysis | Valid + invalid boundaries with valid inputs | Correct pattern, invalid data |  Ours wins |
|  Statement Coverage | Isolated valid and invalid input for logic lines | Mixes invalid dependencies |  Ours wins |

---

##  Conclusion

Human-crafted tests, though longer, are far more precise and **targeted for correctness and clarity**. AI tools are useful to scaffold, but must be audited to **avoid false positives or misleading failures**.
