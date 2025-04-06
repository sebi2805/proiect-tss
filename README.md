[WIP SEBI]
For class equivalence, we have 4 parameters and these 4 parameters can be classified in the following categories

| Parameter        | Valid Class                                     | Invalid Classes                                                                                         |
| ---------------- | ----------------------------------------------- | ------------------------------------------------------------------------------------------------------- |
| **Email**        | Correct format (`john.doe@example.com`), unique | Incorrect format (`johndoeexample.com`, `john.doe@com`), already registered                             |
| **Username**     | 3-20 characters (`john123`, `user_name`)        | Too short (< 3 characters, e.g., `ab`), too long (> 20 characters, e.g., `thisusernameiswaytoolong123`) |
| **Birth Date**   | Format `YYYY-MM-DD`, past date (`1990-05-10`)   | Incorrect format (`1990/05/10`), future date (`2090-05-10`)                                             |
| **Phone Number** | Valid prefix (`+40 712345678` for Romania)      | Invalid prefix (`+99 712345678`), mismatched country (`country="Romania"` but number starts with `+33`) |

---

## Boundary Value Analysis

In our case, we applied Boundary Value Analysis to the `UserManager` class to ensure that edge cases related to user creation were properly handled. The key boundary conditions we tested include:

1. **Username Length**

   - Minimum invalid: `aaa` (3 characters) → Expected failure
   - Minimum valid: `aaaa` (4 characters) → Expected success
   - Maximum valid: `a` \* 19 (19 characters) → Expected success
   - Maximum invalid: `a` \* 20 (20 characters) → Expected failure

2. **Birth Date**

   - Future date (today’s date) → Expected failure
   - Oldest valid date (`1900-01-01`) → Expected success

3. **Email Format**

   - Minimal valid email format (`a@b.c`) → Expected success

4. **Phone Number Prefix Matching**
   - Valid country prefix (`+1` for USA when the country is "USA") → Expected success
   - Invalid prefix (`+1` for Romania when the expected prefix is `+40`) → Expected failure

These tests ensure that `UserManager` correctly validates user inputs at the boundaries of acceptable values.

### Running the Tests and Coverage Analysis

We executed the boundary tests using the following command:

```sh
pytest --cov=src --cov-report=term-missing test/test_boundary.py
```

The results were as follows:

```plaintext
Name                 Stmts   Miss  Cover   Missing
--------------------------------------------------
src\User.py              7      0   100%
src\UserManager.py      40      7    82%   12-13, 38, 43-44, 50, 53
src\__init__.py          0      0   100%
--------------------------------------------------
TOTAL                   47      7    85%
```

### Why 100% Coverage Isn't Necessary

The reported 82% coverage for UserManager.py indicates that some lines are not executed by our boundary tests. However, this does not mean that our boundary testing is incomplete. The missing lines are not related to boundary conditions.

Since our goal was to validate boundary conditions, achieving 100% coverage is not strictly necessary. Instead, our focus is on ensuring that key input constraints are thoroughly tested, which our boundary tests accomplish effectively.

We validated that extreme and edge-case inputs are properly handled. Although we achieved 82% coverage, our tests sufficiently address critical boundary conditions, ensuring robust user validation.

---

## Statement Analysis

We applied Statement analisys on the `UserManager` class with a 98% statement coverage. The following Control Flow Graph has been created:
[Lucid Chart](<https://lucid.app/lucidchart/52e5e0a2-3c17-4dda-8930-4ef34498d4b7/edit?invitationId=inv_e62830fb-62b8-4810-9e4c-0ee0b0dc8ec7>)

![Control Flow Graph Code](images/statement_analysis_code.png)

![Control Flow Graph](images/statement_analysis_graph.png)
