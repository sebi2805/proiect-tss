# Demo

[![Demo Preview](https://img.youtube.com/vi/4h-NoWC28mM/0.jpg)](https://youtu.be/4h-NoWC28mM)

## Project structure and purpose

Our approach would be to have a package 'src', what does contain our bussnies logic in 2 modules User and UserManager. Here we will have an functionality that will create users if certain information are validated, also in order to cover more tests we would like to implement a functionality for searching the user, this way we can adapt better tests to showcase

The purpose of this project is to create tests using some the current tehcnologies and where certain requirements don't fit with the project, we would adapt it with some other packages or functionalities integrated in pycharm (because last year pychamr also integrated some code-coverage functionalities).

Regarding the setup, we have a page dedicated to it, we try to make this code work in a similar way on multiple machine, that's why we created an venv, We could also consider using <https://github.com/pyenv/pyenv>, so we manage our python versions.

This being said these are some projects that have a similar approach like us:

- <https://github.com/MartinThoma/mpu> - a python library where tests are mandatory so you can have backwards compability
- <https://github.com/ryankanno/cookiecutter-py> - a standard python project template

on the other hand we also have some research papers that are studying the pytest inline and how small is the overload <https://arxiv.org/abs/2305.13486#:~:text=program%20statements,provides%2C%20and%20the%20intended%20use>, maybe we can also implement some of this

## PyTest vs Unittest

| Feature                | **Pytest (3rd party)**                                                                  | **unittest (standard library)**                                                 |
| ---------------------- | --------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------- |
| **Initial Setup**      | External installation required, but auto-discovers tests effortlessly                   | Built-in (no install), but requires strict naming conventions (`test*` methods) |
| **Test Syntax**        | Uses plain functions with `assert` (concise, detailed failure messages)                 | Requires `TestCase` classes and `assert*` methods (more boilerplate)            |
| **Fixtures & Setup**   | Powerful fixtures (function, module, session scope); mocking plugins available          | `setUp`/`tearDown` methods; limited native fixture support                      |
| **Extensibility**      | Rich plugin ecosystem (coverage, Django, benchmarks); active community                  | Basic built-in features; few extensions beyond third-party tools like `nose`    |
| **Parallel Execution** | Yes – via plugins (e.g., `xdist`)                                                       | Not by default – only possible using external tools                             |
| **IDE/CI Integration** | Well-supported in most IDEs (e.g., PyCharm) and CI tools; coverage needs config/plugins | Natively supported in IDEs/CI; coverage via `coverage.py` or IDE integration    |
| **Current Popularity** | Widely adopted, de facto standard for new projects                                      |

<https://blog.jetbrains.com/pycharm/2024/03/pytest-vs-unittest/#:~:text=That%20said%2C%20for%20new%20projects,has%20become%20the%20default%20choice>
<https://dev.to/vbuxbaum/testing-tests-in-python-part-1-reasons-and-alternatives-42bn#:~:text=,assert>

---

## Pytest-cov vs. PyCharm Code Coverage

Both use `coverage.py` under the hood. Key differences lie in usage and output:

### ✅ Pytest-cov

- Pytest plugin for CLI-based coverage.
- Add `--cov` to pytest to collect coverage data (incl. parallel runs via `pytest-xdist`).
- Outputs a text summary in the terminal.
- Easily exportable (HTML/XML) with `coverage.py`.
- Ideal for CI/CD (e.g. GitHub Actions, Jenkins).
- Works in any dev environment (not tied to an IDE).

### 🖥️ PyCharm Coverage

- Built into the PyCharm IDE.
- GUI summary per file/package.
- Useful for fast feedback during development or teaching.
- Can merge multiple coverage runs.

---

## Mutation

To improve the quality of our tests and not just focus on code coverage, we’ll integrate **mutatin testing** using [Mutmut](https://github.com/boxed/mutmut). The idea is simple: we intentionally inject small bugs into the code (called **mutants**) and see if our tests catch them. If a mutant survives, it’s a sign that the test might not be verifying the behavior properly.

We’re interested in testing not just that "code is run", but that it’s actually **validated**. For example, a test might give you 100% coverage but still miss a logic error if there’s no assertion and that's is what we are trying to combine also with the 2 tools dor code coverage.

Mutmut works well with `pytest`, so the integration into our current stack will be smooth. Once installed (`pip install mutmut`), we can run `mutmut run` to generate mutants and get a report showing:

- **Killed mutants** = tests failed → good.
- **Survived mutants** = tests passed → weak spot in test logic.

Mutmut applies mutations like:

- Changing operators (`>` → `>=`, `+` → `-`)
- Flipping booleans (`True` → `False`)
- Removing return statements
- Altering constant values or string literals

---

## Boundary Value Analysis

Boundary Value Analysis (BVA) focuses on testing the boundaries of input domains rather than selecting arbitrary values. The rationale behind BVA is that errors are more likely to occur at the edges of valid input ranges rather than within the normal operating range. This technique is particularly effective for numeric values, string lengths, date ranges, and other inputs with clear minimum and maximum constraints.

#### Why Use Boundary Value Analysis?

- Catches edge case errors that might not appear in normal input values.
- Reduces the number of test cases while still providing strong test coverage.
- Ensures robustness of the system by testing both valid and invalid boundary inputs.

---

## Decision-Based Coverage

Decision-Based Coverage (also known as branch coverage) is a white-box testing technique that ensures every decision point in the code is tested for all possible outcomes—true and false. Unlike line coverage, which only verifies if a line is executed, branch coverage verifies that each condition has been fully exercised.

#### Key Concepts:

- Decisions: Statements like if, for, while, and try/except blocks.
- Branches: The two possible outcomes of each decision (e.g., True and False).
- To achieve 100% decision coverage, each of the following must be tested:
- Every if condition evaluated to both true and false
- Every loop entered and skipped
- Every exception raised and not raised

---

## Statement Analysis

Statement Analysis is a technique used to evaluate whether each line of code in a program has been executed at least once during testing. This method ensures that no part of the code remains untested, reducing the risk of hidden bugs.

#### Why Use Statement Analysis?

- Identifies Dead Code – Helps detect unused or redundant code.
- Improves Test Coverage – Ensures that every statement has been executed at least once.
- Complements Code Coverage – While coverage tools show percentage metrics, statement analysis provides deeper insights into untested logic.

---

## Independent Circuit Testing

Independent Circuit Testing (ICT) focuses on testing the individual decision circuits in a program to ensure all possible decision paths are verified. It is particularly useful for validating complex decision structures and ensuring that all logic paths are properly exercised in isolation.

This method is based on McCabe's Cyclomatic Complexity formula, which helps determine the number of independent paths in a program. The formula is as follows:

- **V(G) = e - n + 2** for a single program or subroutine, where:
  - `e` is the number of edges (arcs),
  - `n` is the number of nodes,
  - `p` is the number of connected components (typically 1 for a single program).

By calculating the number of independent circuits, ICT ensures that each unique logical decision path is tested without interference from other paths in the program.

#### Why Use Independent Circuit Testing?

- **Validates Decision Paths**: Ensures that all possible decision outcomes (true/false) are tested, providing comprehensive coverage.
- **Reduces Complexity**: Focuses on testing small, independent sections of code, making it easier to identify errors in logic.
- **Improves Test Accuracy**: By isolating logic tests, it reduces the chance of missing edge cases or subtle bugs.

---

## Class Equivalence Analysis

The `create_user` method accepts the following parameters:

1. e - a string with an email template
2. u - a string that represents the username
3. b - a date that represents the birth date
4. p - a string with phone number template
5. r - a string that represents a country

### Individual Parameter Equivalence Classes

### Input domain

#### Email

- **E1** = { e | e has a valid format and is unique (e.g., "john.doe@example.com") }
<!-- TODO  or is already registered -->
- **E2** = { e | e has an invalid format (e.g., "johndoeexample.com", "john.doe@com") }

#### Username

- **U1** = { u | u has a valid length (3 ≤ length ≤ 20) (e.g., "john_doe", "user123") }
- **U2** = { u | u is too short (< 3 characters, e.g., "ab") }
- **U3** = { u | u is too long (> 20 characters, e.g., "thisusernameiswaytoolong123") }

#### Birth Date

- **B1** = { b | b is in the format "YYYY-MM-DD" and is a past date (e.g., "1990-05-10") }
- **B2** = { b | b is in an incorrect format (e.g., "1990/05/10") }
- **B3** = { b | b is in the format "YYYY-MM-DD" but is a future date (e.g., "2090-05-10") }

#### Phone Number

- **P1** = { p | p has a valid format and prefix for the specified country (e.g., "+40 712345678" for Romania) }
- **P2** = { p | p has an invalid format or an incorrect prefix (e.g., "+33 712345678" when country is "Romania") }

#### Country

Let the valid set of countries be:  
{ "Romania", "USA", "UK", "France", "Germany", "Italy", "Spain", "Canada", "Australia", "India" }

- **R1** = { r | c ∈ { "Romania", "USA", "UK", "France", "Germany", "Italy", "Spain", "Canada", "Australia", "India" } }
- **R2** = { r | c ∉ { "Romania", "USA", "UK", "France", "Germany", "Italy", "Spain", "Canada", "Australia", "India" } }

---

### Output Domain

Consists of the following two attributes:

- `status` – the HTTP response code (200 = success, 400 = error)
- `msg` – a descriptive message indicating whether the operation succeeded or why it failed

These map to the following output equivalence classes:

- **O1** = { status = 200; msg contains `"User successfully created"` }
- **O2** = { status = 400; msg contains `"Invalid email"` }
- **O3** = { status = 400; msg contains `"Email already registered"` }
- **O4** = { status = 400; msg contains `"Username too short"` }
- **O5** = { status = 400; msg contains `"Username too long"` }
- **O6** = { status = 400; msg contains `"Invalid birth date format"` }
- **O7** = { status = 400; msg contains `"Birth date is in the future"` }
- **O8** = { status = 400; msg contains `"Invalid phone number"` }
- **O9** = { status = 400; msg contains `"Unsupported country"` }

---

### Global Equivalence Classes

We combine the individual classes to form global test cases. Denote a global class as **C\_{abcde}**, where:

- **a**: Email class (1 for E1, 2 for E2)
- **b**: Username class (1 for U1, 2 for U2, 3 for U3)
- **c**: Birth Date class (1 for B1, 2 for B2, 3 for B3)
- **d**: Phone Number class (1 for P1, 2 for P2)
- **e**: Country class (1 for R1, 2 for R2)

Key examples include:

1. **C_11111** = { (e, u, b, p, r) | e ∈ E1, u ∈ U1, b ∈ B1, p ∈ P1, r ∈ R1 }  
   _All parameters valid (happy path)._

2. **C_12111** = { (e, u, b, p, r) | e ∈ E1, u ∈ U2, b ∈ B1, p ∈ P1, r ∈ R1 }  
   _Invalid: Username is too short._

3. **C_13111** = { (e, u, b, p, r) | e ∈ E1, u ∈ U3, b ∈ B1, p ∈ P1, r ∈ R1 }  
   _Invalid: Username is too long._

4. **C_11211** = { (e, u, b, p, r) | e ∈ E1, u ∈ U1, b ∈ B2, p ∈ P1, r ∈ R1 }  
   _Invalid: Birth Date format is incorrect._

5. **C_11311** = { (e, u, b, p, r) | e ∈ E1, u ∈ U1, b ∈ B3, p ∈ P1, r ∈ R1 }  
   _Invalid: Birth Date is in the future._

6. **C_11121** = { (e, u, b, p, r) | e ∈ E1, u ∈ U1, b ∈ B1, p ∈ P2, r ∈ R1 }  
   _Invalid: Phone Number is invalid._

7. **C_11112** = { (e, u, b, p, r) | e ∈ E1, u ∈ U1, b ∈ B1, p ∈ P1, r ∈ R2 }  
   _Invalid: Country is not in the valid list._

8. **C_21111** = { (e, u, b, p, r) | e ∈ E2, u ∈ U1, b ∈ B1, p ∈ P1, r ∈ R1 }  
   _Invalid: Email is invalid or duplicated._

---

- **c_11111** ∈ C_11111:  
  ("john.doe@example.com", "john_doe", "1990-05-10", "+40 712345678", "Romania")

- **c_12111** ∈ C_12111:  
  ("john.doe@example.com", "ab", "1990-05-10", "+40 712345678", "Romania")

- **c_13111** ∈ C_13111:  
  ("john.doe@example.com", "thisusernameiswaytoolong123", "1990-05-10", "+40 712345678", "Romania")

- **c_11211** ∈ C_11211:  
  ("john.doe@example.com", "john_doe", "1990/05/10", "+40 712345678", "Romania")

- **c_11311** ∈ C_11311:  
  ("john.doe@example.com", "john_doe", "2090-05-10", "+40 712345678", "Romania")

- **c_11121** ∈ C_11121:  
  ("john.doe@example.com", "john_doe", "1990-05-10", "+33 712345678", "Romania")

- **c_11112** ∈ C*11112:  
  ("john.doe@example.com", "john_doe", "1990-05-10", "+40 712345678", "Mars")  
  *(Invalid country example)\_

- **c_21111** ∈ C_21111:  
  ("johndoeexample.com", "john_doe", "1990-05-10", "+40 712345678", "Romania")

| Test    | Email                | Username                    | Birthdate  | Phone         | Country | Expected Output                    |
| ------- | -------------------- | --------------------------- | ---------- | ------------- | ------- | ---------------------------------- |
| C_11111 | john.doe@example.com | john_doe                    | 1990-05-10 | +40 712345678 | Romania | 200, “User successfully created”   |
| C_12111 | john.doe@example.com | ab                          | 1990-05-10 | +40 712345678 | Romania | 400, “Username too short”          |
| C_13111 | john.doe@example.com | thisusernameiswaytoolong123 | 1990-05-10 | +40 712345678 | Romania | 400, “Username too long”           |
| C_11211 | john.doe@example.com | john_doe                    | 1990/05/10 | +40 712345678 | Romania | 400, “Invalid birth date format”   |
| C_11311 | john.doe@example.com | john_doe                    | 2090-05-10 | +40 712345678 | Romania | 400, “Birth date is in the future” |
| C_11121 | john.doe@example.com | john_doe                    | 1990-05-10 | +33 712345678 | Romania | 400, “Invalid phone number”        |
| C_11112 | john.doe@example.com | john_doe                    | 1990-05-10 | +40 712345678 | Mars    | 400, “Unsupported country”         |
| C_21111 | johndoeexample.com   | john_doe                    | 1990-05-10 | +40 712345678 | Romania | 400, “Invalid email”               |

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

### Running the Tests and Coverage Analysis

We executed the class equivalence tests using the following command:

```sh
pytest --cov=src --cov-report=term-missing test/test_equivalence_partitioning.py
```

The results were as follows:

```plaintext
Name                 Stmts   Miss  Cover   Missing
--------------------------------------------------
src/User.py              7      0   100%
src/UserManager.py      40      4    90%   12-13, 38, 53
src/__init__.py          0      0   100%
--------------------------------------------------
TOTAL                   47      4    91%
```

[![Video Preview](https://img.youtube.com/vi/jrMZes8y4pg/0.jpg)](https://youtu.be/jrMZes8y4pg)

## Boundary Value Analysis

### What is Boundary Value Analysis?

Boundary Value Analysis (BVA) is a black-box test design technique that complements equivalence partitioning. It focuses on testing input values at their boundaries, where errors are statistically more likely to occur. Instead of randomly selecting values from valid partitions, BVA suggests choosing:

- The minimum and maximum valid values
- Values just below and above these limits

This method is particularly useful for identifying off-by-one errors and validating input restrictions.

---

### Identifying Boundary Classes for UserManager

In our case, we applied BVA to the `create_user` method from the `UserManager` class. The input fields we considered for boundary testing are:

1. **Username length**:

   - Valid range: 4 to 19 characters
   - Classes:
     - U_1: valid username length (4, 19)
     - U_2: under min length (3)
     - U_3: over max length (20)

2. **Birth date**:

   - Valid range: between 1900-01-01 and yesterday
   - Classes:
     - B_1: valid old date (e.g., `1900-01-01`)
     - B_2: boundary invalid (today’s date or future)

3. **Email format**:
   - Basic syntactic check (e.g., must contain `@` and `.`)
   - Classes:
     - E_1: minimal valid email (`a@b.c`)
     - E_2: invalid formats – not explicitly tested here as this falls more under format validation

---

### Test Cases from Boundary Classes

The following table shows test data derived from our boundary classes:

| Username Length  | Birth Date   | Email            | Expected Result             | Class |
| ---------------- | ------------ | ---------------- | --------------------------- | ----- |
| `aaa` (3 chars)  | 2003-02-26   | test@example.com | Username too short          | U_2   |
| `aaaa` (4 chars) | 2003-02-26   | test@example.com | User successfully created   | U_1   |
| `a` \* 19        | 2003-02-26   | test@example.com | User successfully created   | U_1   |
| `a` \* 20        | 2003-02-26   | test@example.com | Username too long           | U_3   |
| `validname`      | `1900-01-01` | test@example.com | User successfully created   | B_1   |
| `validname`      | Today’s date | test@example.com | Birth date is in the future | B_2   |
| `minimal`        | 2003-02-26   | `a@b.c`          | User successfully created   | E_1   |

> Note: All tests assume that `country="Romania"` and `phone_number="+40 712345678"` are valid and constant, to isolate boundary analysis to the fields above.

---

### Running the Tests and Coverage Analysis on Boundary Classes

We executed the boundary tests using the following command:

```sh
pytest --cov=src --cov-report=term-missing test/test_boundary.py
```

The results were as follows:

```plaintext
Name                 Stmts   Miss  Cover   Missing
--------------------------------------------------
src\User.py              7      0   100%
src\UserManager.py      40      8    80%   12-13, 38, 43-44, 50, 53, 62
src\__init__.py          0      0   100%
--------------------------------------------------
TOTAL                   47      8    83%
```

[![Video Preview](https://img.youtube.com/vi/Ai9dJchoAgs/0.jpg)](https://youtu.be/Ai9dJchoAgs)

---

### Coverage analysis

The reported 80% coverage for UserManager.py indicates that some lines are not executed by our boundary tests. However, this does not mean that our boundary testing is incomplete. The missing lines are not related to boundary conditions.

Since our goal was to validate boundary conditions, achieving 100% coverage is not strictly necessary. Instead, our focus is on ensuring that key input constraints are thoroughly tested, which our boundary tests accomplish effectively.

We validated that extreme and edge-case inputs are properly handled. Although we achieved 80% coverage, our tests sufficiently address critical boundary conditions, ensuring robust user validation.

---

## Decision Coverage

**Purpose:** To verify the application’s behavior at critical decision points (if statements, loops, logical expressions), ensuring that all possible branches (true / false) are tested at least once.

---

### Analyzed Code: `create_user` from `UserManager.py`

This function includes several decisions that must be covered to guarantee robust behavior:

| #   | Decision Statement                                   | Type            | Description                               |
| --- | ---------------------------------------------------- | --------------- | ----------------------------------------- |
| 1   | `if birth_date >= datetime.today()`                  | simple if       | Checks if the birth date is in the future |
| 2   | `if not self.validate_email(email)`                  | simple if       | Validates email format                    |
| 3   | `if self.email_exists(email)`                        | if without else | Checks if the email is already used       |
| 4   | `if len(username) <= 3` / `elif len(username) >= 20` | if with else    | Checks username length                    |
| 5   | `if not self.validate_phone_prefix(...)`             | simple if       | Checks phone prefix-country match         |

Helper functions tested separately:

- `email_exists()` – contains a `for` + `if`
- `validate_phone_prefix()` – contains a `for` + `if` + `return`

---

### Loops and Decisions Covered

| Location                                  | Loop Type                               | Behavior Tested                                                 |
| ----------------------------------------- | --------------------------------------- | --------------------------------------------------------------- |
| `for user in self.users:`                 | `for` loop in `email_exists()`          | Tests case where email does not match any existing user         |
| `for c, prefix in country_codes.items():` | `for` loop in `validate_phone_prefix()` | Tests case where prefix doesn't match (triggers fallback logic) |

---

### Implemented Tests: `test_decision_coverage.py`

| Test                                          | Branch Tested        | Target Decision                    |
| --------------------------------------------- | -------------------- | ---------------------------------- |
| `test_email_exists_with_non_matching_email()` | False                | `email_exists()`                   |
| `test_validate_phone_prefix_no_match()`       | False                | `validate_phone_prefix()`          |
| `test_username_exactly_3_characters()`        | True → error         | `if len(username) <= 3`            |
| `test_birth_date_exact_today()`               | True → error         | `if birth_date >= today()`         |
| `test_success_path_user_creation()`           | All conditions False | Positive path through all branches |

---

### Conclusion

- Every decision in `create_user()` is evaluated for both **true** and **false** results.
- All relevant decision branches are covered: simple and compound conditions, including `if` statements without `else`, and chained expressions (`if` + `elif`).
- Inactive branches of loops are also tested (`for` + `return False`).

---

### Advantages

- Complete logical coverage of critical decisions.
- Combined with the tests from `test_user_manager.py` and `test_boundary.py`, this test suite provides a strong foundation for structural testing.

---

[![Video Preview](https://img.youtube.com/vi/qhdAivN3ZgI/0.jpg)](https://youtu.be/qhdAivN3ZgI)

---

## Statement Analysis

We applied Statement analisys on the `UserManager` class with a 98% statement coverage. The following Control Flow Graph has been created:
[Lucid Chart](https://lucid.app/lucidchart/52e5e0a2-3c17-4dda-8930-4ef34498d4b7/edit?invitationId=inv_e62830fb-62b8-4810-9e4c-0ee0b0dc8ec7)

To achieve statement coverage, we need to focus on the instructions controlled by conditions (corresponding to branches in the graph).

For statement coverage testing, each instruction in the source code must be executed at least once during testing. This is considered the minimum coverage level that a structural test can achieve.

The following table shows test inputs and the instructions they cover:

| Test ID | Email                | Username                 | Birth Date   | Phone Number  | Country | Expected Output                         | Lines Covered                                          |
| ------- | -------------------- | ------------------------ | ------------ | ------------- | ------- | --------------------------------------- | ------------------------------------------------------ |
| 1       | valid@example.com    | validuser                | 1990-01-01   | +40 712345678 | Romania | 200, User successfully created          | 36-37, 40-41, 43-44, 46-47, 49-50, 52-53, 55-56, 58-61 |
| 2       | invalid-email        | validuser                | 1990-01-01   | +40 712345678 | Romania | 400, Invalid email                      | 36-37, 40-41, 43-45                                    |
| 3       | existing@example.com | validuser                | 1990-01-01   | +40 712345678 | Romania | 400, Email already exists               | 36-37, 40-41, 43-44, 46-48                             |
| 4       | valid@example.com    | ab                       | 1990-01-01   | +40 712345678 | Romania | 400, Username too short                 | 36-37, 40-41, 43-44, 46-47, 49-51                      |
| 5       | valid@example.com    | thisusernameiswaytoolong | 1990-01-01   | +40 712345678 | Romania | 400, Username too long                  | 36-37, 40-41, 43-44, 46-47, 49-50, 52-54               |
| 6       | valid@example.com    | validuser                | invalid-date | +40 712345678 | Romania | 400, Invalid birth date                 | 36, 38-39                                              |
| 7       | valid@example.com    | validuser                | 2099-01-01   | +40 712345678 | Romania | 400, Birth date is in the future        | 36-37, 40-42                                           |
| 8       | valid@example.com    | validuser                | 1990-01-01   | +33 712345678 | Romania | 400, Phone number prefix does not match | 36-37, 40-41, 43-44, 46-47, 49-50, 52-53, 55-57        |

![Control Flow Graph Code](images/statement_analysis_code.png)

![Control Flow Graph](images/statement_analysis_graph.png)

---

## Independent Circuit Testing

This form of analysis identifies the **upper bound on the number of paths** required to achieve complete **branch coverage**.

It is based on **McCabe's Cyclomatic Complexity**, which estimates the number of **linearly independent circuits** in a control flow graph (CFG).

---

### McCabe's Cyclomatic Complexity

To compute the number of independent circuits, we use the formula:

\[
V(G) = e - n + 2p
\]

Where:

- `e` = number of edges
- `n` = number of nodes
- `p` = number of connected components (for a single method, `p = 1`)

---

### Estimation for `create_user`

#### Node and Edge Analysis

| Node ID | Description                              | Type     |
| ------- | ---------------------------------------- | -------- |
| N1      | Start node                               | Entry    |
| N2      | Try to parse birth date                  | Decision |
| N3      | Exception handling (invalid date format) | Terminal |
| N4      | Check if birth date is in the future     | Decision |
| N5      | Return future date error                 | Terminal |
| N6      | Check email format                       | Decision |
| N7      | Return invalid email                     | Terminal |
| N8      | Check if email exists                    | Decision |
| N9      | Return duplicate email                   | Terminal |
| N10     | Check if username is too short           | Decision |
| N11     | Return username too short                | Terminal |
| N12     | Check if username is too long            | Decision |
| N13     | Return username too long                 | Terminal |
| N14     | Validate phone prefix                    | Decision |
| N15     | Return phone prefix mismatch             | Terminal |
| N16     | Create user and return success           | Terminal |

**Total Nodes (`n`) = 16**

---

| Edge # | From → To | Reason                        |
| ------ | --------- | ----------------------------- |
| E1     | N1 → N2   | Begin method                  |
| E2     | N2 → N3   | Exception raised              |
| E3     | N2 → N4   | Valid birth date              |
| E4     | N4 → N5   | Future date                   |
| E5     | N4 → N6   | Past date                     |
| E6     | N6 → N7   | Invalid email                 |
| E7     | N6 → N8   | Valid email                   |
| E8     | N8 → N9   | Email exists                  |
| E9     | N8 → N10  | Email unique                  |
| E10    | N10 → N11 | Username too short            |
| E11    | N10 → N12 | Username long enough          |
| E12    | N12 → N13 | Username too long             |
| E13    | N12 → N14 | Username length valid         |
| E14    | N14 → N15 | Invalid phone prefix          |
| E15    | N14 → N16 | Valid phone and country match |

**Total Edges (`e`) = 15**

---

### Final Calculation

Using the formula:

\[
V(G) = e - n + 2 = 15 - 16 + 2 = \boxed{1}
\]

This is too low because **each decision point counts toward complexity**, and this formula assumes a simplified structure.

**Better formula for structured programs**:

\[
V(G) = \text{Number of predicate nodes (decisions)} + 1
\]

We have:

- `try/except` = 1
- `if birth_date >= today` = 1
- `validate_email` = 1
- `email_exists` = 1
- `username too short` = 1
- `username too long` = 1
- `validate_phone_prefix` = 1

So:

\[
V(G) = 7 + 1 = \boxed{8}
\]

And we also add the **final return (success)** as another control branch → \[
V(G) = \boxed{9}
\]

---

### Independent Paths (Base Path Set)

The following 9 paths test each control decision independently:

| Path | Description                                  | Result Code | Message Fragment                     |
| ---- | -------------------------------------------- | ----------- | ------------------------------------ |
| A    | All inputs valid                             | 200         | "User successfully created"          |
| B    | Invalid birth date format                    | 400         | "Invalid birth date"                 |
| C    | Future birth date                            | 400         | "Birth date is in the future"        |
| D    | Invalid email format                         | 400         | "Invalid email"                      |
| E    | Duplicate email                              | 400         | "Email already exists"               |
| F    | Username too short                           | 400         | "Username too short"                 |
| G    | Username too long                            | 400         | "Username too long"                  |
| H    | Valid prefix, wrong country (mismatch)       | 400         | "Phone number prefix does not match" |
| I    | Phone number does not match any known prefix | 400         | "Phone number prefix does not match" |

---

### Python Test Example

```python
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

### Running the Tests and Coverage Analysis on Independent Circuits

We executed the boundary tests using the following command:

```sh
pytest --cov=src --cov-report=term-missing .\test\test_independent_circuits.py
```

The results were as follows:

```plaintext

Name                 Stmts   Miss  Cover   Missing
--------------------------------------------------
src\User.py              7      0   100%
src\UserManager.py      40      0   100%
src\__init__.py          0      0   100%
--------------------------------------------------
TOTAL                   47      0   100%
```

[![Video Preview](https://img.youtube.com/vi/vAOG3gtxtfs/0.jpg)](https://youtu.be/vAOG3gtxtfs)

## Condition Coverage Analysis

### Why Condition Coverage?

Condition coverage forces **every atomic Boolean operand** inside every decision to evaluate
to both `True` and `False` at least once.  
This satisfies the _condition coverage._ criterions.

### Decision points in `UserManager`

| #   | Location / predicate                                        | Atomic conditions flipped                      |
| --- | ----------------------------------------------------------- | ---------------------------------------------- |
| 1   | `try/except` around `datetime.strptime`                     | _raises_ / _does-not-raise_                    |
| 2   | `if birth_date >= today:`                                   | `birth_date >= today`                          |
| 3   | `if not self.validate_email(email):`                        | `validate_email(email)`                        |
| 4   | `if self.email_exists(email):`                              | `email_exists(email)`                          |
| 5   | `if len(username) < 4:`                                     | `len(username) < 4`                            |
| 6   | `elif len(username) > 20:`                                  | `len(username) > 20`                           |
| 7   | `if not self.validate_phone_prefix(phone_number, country):` | `validate_phone_prefix(phone_number, country)` |

### Mapping tests → atomic conditions

| Predicate ID | **True** exercised by                  | **False** exercised by      |
| ------------ | -------------------------------------- | --------------------------- |
| 1            | CU2 (invalid date format)              | all other CU\* cases        |
| 2            | CU3 (future date)                      | CU1, CU4-CU9                |
| 3            | CU1 (invalid email)                    | CU2-CU9, VE1 helper test    |
| 4            | CU8 (duplicate email) & E1 helper test | all non-duplicate scenarios |
| 5            | CU4 (username too short)               | everything else             |
| 6            | CU5 (username too long)                | everything else             |
| 7            | CU6 & CU7, VP2/VP3 helper tests        | CU1-CU5, CU8-CU9, VP1       |

### Achieved coverage

Run the suite with branch tracking enabled:

```bash
pytest --cov=src --cov-branch --cov-report=term-missing


Name                 Stmts   Miss Branch BrPart  Cover
------------------------------------------------------
src/UserManager.py      40      0     14      0   100%
src/User.py              7      0      0      0   100%
------------------------------------------------------
TOTAL                   47      0     14      0   100%
```

[![Watch the video](https://img.youtube.com/vi/Y59qTBrWnFo/hqdefault.jpg)](https://www.youtube.com/watch?v=Y59qTBrWnFo)
