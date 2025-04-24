Our approach would be to have a package 'src', what does contain our bussnies logic in 2 modules User and UserManager. Here we will have an functionality that will create users if certain information are validated, also in order to cover more tests we would like to implement a functionality for searching the user, this way we can adapt better tests to showcase

The purpose of this project is to create tests using some the current tehcnologies and where certain requirements don't fit with the project, we would adapt it with some other packages or functionalities integrated in pycharm (because last year pychamr also integrated some code-coverage functionalities).

Regarding the setup, we have a page dedicated to it, we try to make this code work in a similar way on multiple machine, that's why we created an venv, We could also consider using <https://github.com/pyenv/pyenv>, so we manage our python versions.

This being said these are some projects that have a similar approach like us:

- <https://github.com/MartinThoma/mpu> - a python library where tests are mandatory so you can have backwards compability
- <https://github.com/ryankanno/cookiecutter-py> - a standard python project template

on the other hand we also have some research papers that are studying the pytest inline and how small is the overload <https://arxiv.org/abs/2305.13486#:~:text=program%20statements,provides%2C%20and%20the%20intended%20use>, maybe we can also implement some of this

## PyTest vs Unittest

| Feature | **Pytest (3rd party)** | **unittest (standard library)** |
|----------------------------|-----------------------------------------------------------------------------------------|----------------------------------------------------------------------------------|
| **Initial Setup** | External installation required, but auto-discovers tests effortlessly | Built-in (no install), but requires strict naming conventions (`test*` methods) |
| **Test Syntax** | Uses plain functions with `assert` (concise, detailed failure messages) | Requires `TestCase` classes and `assert*` methods (more boilerplate) |
| **Fixtures & Setup** | Powerful fixtures (function, module, session scope); mocking plugins available | `setUp`/`tearDown` methods; limited native fixture support | |
| **Extensibility** | Rich plugin ecosystem (coverage, Django, benchmarks); active community | Basic built-in features; few extensions beyond third-party tools like `nose` |
| **Parallel Execution** | Yes – via plugins (e.g., `xdist`) | Not by default – only possible using external tools |
| **IDE/CI Integration** | Well-supported in most IDEs (e.g., PyCharm) and CI tools; coverage needs config/plugins| Natively supported in IDEs/CI; coverage via `coverage.py` or IDE integration |
| **Current Popularity** | Widely adopted, de facto standard for new projects | Mostly used in legacy code or by those preferring stdlib; declining in new code |

<https://blog.jetbrains.com/pycharm/2024/03/pytest-vs-unittest/#:~:text=That%20said%2C%20for%20new%20projects,has%20become%20the%20default%20choice>
<https://dev.to/vbuxbaum/testing-tests-in-python-part-1-reasons-and-alternatives-42bn#:~:text=,assert>

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

## Mutation

To improv the quality of our tests and not just focus on code coverage, we’ll integrate **mutatin testing** using [Mutmut](https://github.com/boxed/mutmut). The idea is simple: we intentionally inject small bugs into the code (called **mutants**) and see if our tests catch them. If a mutant survives, it’s a sign that the test might not be verifying the behavior properly.

We’re interested in testing not just that "code is run", but that it’s actually **validated**. For example, a test might give you 100% coverage but still miss a logic error if there’s no assertion and that's is what we are trying to combine also with the 2 tools dor code coverage.

Mutmut works well with `pytest`, so the integration into our current stack will be smooth. Once installed (`pip install mutmut`), we can run `mutmut run` to generate mutants and get a report showing:

- **Killed mutants** = tests failed → good.
- **Survived mutants** = tests passed → weak spot in test logic.

Mutmut applies mutations like:

- Changing operators (`>` → `>=`, `+` → `-`)
- Flipping booleans (`True` → `False`)
- Removing return statements
- Altering constant values or string literals

## Boundary Value Analysis

Boundary Value Analysis (BVA) focuses on testing the boundaries of input domains rather than selecting arbitrary values. The rationale behind BVA is that errors are more likely to occur at the edges of valid input ranges rather than within the normal operating range. This technique is particularly effective for numeric values, string lengths, date ranges, and other inputs with clear minimum and maximum constraints.

Why Use Boundary Value Analysis?

- Catches edge case errors that might not appear in normal input values.
- Reduces the number of test cases while still providing strong test coverage.
- Ensures robustness of the system by testing both valid and invalid boundary inputs.

## Decision-Based Coverage

Decision-Based Coverage (also known as branch coverage) is a white-box testing technique that ensures every decision point in the code is tested for all possible outcomes—true and false. Unlike line coverage, which only verifies if a line is executed, branch coverage verifies that each condition has been fully exercised.

Key Concepts:

- Decisions: Statements like if, for, while, and try/except blocks.
- Branches: The two possible outcomes of each decision (e.g., True and False).
- To achieve 100% decision coverage, each of the following must be tested:
- Every if condition evaluated to both true and false
- Every loop entered and skipped
- Every exception raised and not raised

## Statement Analysis

Statement Analysis is a technique used to evaluate whether each line of code in a program has been executed at least once during testing. This method ensures that no part of the code remains untested, reducing the risk of hidden bugs.

Why Use Statement Analysis?

- Identifies Dead Code – Helps detect unused or redundant code.
- Improves Test Coverage – Ensures that every statement has been executed at least once.
- Complements Code Coverage – While coverage tools show percentage metrics, statement analysis provides deeper insights into untested logic.
