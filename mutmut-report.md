# Mutation Testing

We’re using **mutmut v2.5.2** to generate and test mutants because in the 3.x series the HTML output was removed in favor of an unfinished UI, and there are outstanding issues around module imports.

---

## Requirements

- A Linux or macOS environment
- Dependencies installed from `requirements.txt`

---

## Usage

1. Ensure your virtual environment is active.
2. Run:
   ```bash
   bash mutmut.sh
   ```

This will create all mutants, run your tests against them, and produce both the console report and an HTML report.

## First Run Results

- Generated mutants: 56
- Killed before tests: 6
- Killed after tests: 31

I identified some of the surviving mutants. For example:

```bash
(.venv) sebi@DESKTOP-G5GBQBL:/mnt/c/Users/User/Desktop/university/proiect-tss$ mutmut show 10
```

```python
--- src/UserManager.py
+++ src/UserManager.py
@@ -20,7 +20,7 @@
     def validate_phone_prefix(self, phone_number, country):
         country_codes = {
             "Romania": "+40",
-            "USA": "+1",
+            "XXUSAXX": "+1",
             "UK": "+44",
             "France": "+33",
             "Germany": "+49",
         }
```

Then I added a parametrized test covering every country code to catch this in `test_mutation`:

```python
@pytest.mark.parametrize(
    "email, username, birth_date_str, phone_number, country, expected_status, expected_msg_fragment",
    [
        ("john.doe@example.com", "john_doe", "1990-05-10", "+40 712345678", "Romania", 200, "User successfully created"),
        ("john.doe@example.com", "john_doe", "1990-05-10", "+1 712345678", "USA",     200, "User successfully created"),
        ("john.doe@example.com", "john_doe", "1990-05-10", "+44 712345678", "UK",     200, "User successfully created"),
        ("john.doe@example.com", "john_doe", "1990-05-10", "+33 712345678", "France", 200, "User successfully created"),
        ("john.doe@example.com", "john_doe", "1990-05-10", "+49 712345678", "Germany",200, "User successfully created"),
        ("john.doe@example.com", "john_doe", "1990-05-10", "+39 712345678", "Italy",  200, "User successfully created"),
        ("john.doe@example.com", "john_doe", "1990-05-10", "+34 712345678", "Spain",  200, "User successfully created"),
        ("john.doe@example.com", "john_doe", "1990-05-10", "+5 712345678",  "Canada", 200, "User successfully created"),
        ("john.doe@example.com", "john_doe", "1990-05-10", "+61 712345678", "Australia",200, "User successfully created"),
        ("john.doe@example.com", "john_doe", "1990-05-10", "+91 712345678", "India",   200, "User successfully created"),
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

```

## Second Run Results

The next surviving mutant was:

```bash
(.venv) sebi@DESKTOP-G5GBQBL:/mnt/c/Users/User/Desktop/university/proiect-tss$ mutmut show 53
```

```python
--- src/UserManager.py
+++ src/UserManager.py
@@ -53,7 +53,7 @@
         if len(username) <= 3:
-            return 400, "Username too short"
+            return 400, "XXUsername too shortXX"
```

To cover that case I added:

```
def test_phone_prefix(self):
    status, msg = self.um.create_user(
        email="country.doe@example.com",
        username="country_user",
        birth_date_str="1990-05-10",
        phone_number="+40 712345678",
        country="Mars"
    )
    assert status == 400
    assert msg == "Phone number prefix does not match the country"
```

After adjusting the code (removing the in operator and fixing prefix logic), we reached 53/56 mutants killed, with only 3 still surviving and the status being suspicious.
