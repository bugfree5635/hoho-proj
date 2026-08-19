# GitHub Actions Coverage Failure

## Problem

GitHub Actions runs the tests successfully, but the CI job still fails because the project's test coverage is below the configured minimum.

For example:

```text
============================= test session starts ==============================
collected 2 items

tests/test_api.py ..

ERROR: Coverage failure: total of 78 is less than fail-under=80

============================== 2 passed in 0.51s ===============================
Error: Process completed with exit code 1
```

The important detail is:

```text
2 passed
```

but:

```text
Coverage: 77.78%
Required: 80%
```

Therefore, the tests themselves passed, but the **coverage requirement failed**.

## Cause

The GitHub Actions workflow contains something similar to:

```yaml
- name: Run tests
  run: |
    pytest --cov=app --cov-report=term-missing --cov-fail-under=80
```

This means:

```text
pytest
  ↓
run tests
  ↓
measure coverage of app/
  ↓
require at least 80%
  ↓
below 80%?
  ↓
CI fails
```

For example:

```text
Total statements: 126
Missing:           28
Coverage:          77.78%
Required:          80%
```

Even though every existing test passes, the project does not have enough tests covering the application code.

## Debug

Run the same command locally:

```bash
pytest --cov=app --cov-report=term-missing --cov-fail-under=80
```

The most useful part is:

```text
Name                         Stmts   Miss  Cover   Missing
----------------------------------------------------------
app/api/auth.py                 22     11    50%   15-22, 28-38
app/security/auth.py            18      9    50%   14-16, 20-23, 27-29
app/database/connection.py      12      4    67%   27-35
```

The `Missing` column tells you which lines are not executed by your tests.

For example:

```text
app/api/auth.py
50% coverage
Missing: 15-22, 28-38
```

means your authentication tests are not exercising those branches.

## Understand the Difference

There are two separate questions:

### Are the tests passing?

```text
tests/test_api.py ..
```

Yes.

### Is enough code being tested?

```text
Coverage: 77.78%
Required: 80%
```

No.

Therefore:

```text
Tests pass
    +
Coverage too low
    =
CI failure
```

This is expected behavior from `--cov-fail-under=80`.

## Solution

The best solution is usually to **add meaningful tests** for the uncovered behavior.

For an authentication API, you might already have:

```python
def test_login_success(client):
    ...
```

but still need tests for:

```text
wrong password
unknown user
successful registration
duplicate username
token creation
invalid credentials
```

For example:

```python
def test_login_wrong_password(client):
    client.post(
        "/auth/register",
        json={
            "username": "henry",
            "password": "123456",
        },
    )

    response = client.post(
        "/auth/login",
        json={
            "username": "henry",
            "password": "wrong",
        },
    )

    assert response.status_code == 401
```

This test executes the error branch in the authentication endpoint.

## Test Authentication Branches

For an authentication API, a useful minimum test set could be:

```text
Registration
├── successful registration
└── duplicate username

Login
├── successful login
├── wrong password
└── unknown username

Authentication
├── valid token
└── invalid/missing token
```

The exact tests depend on your implementation.

The goal is not to write tests simply to increase the percentage.

The goal is to test the important behavior of the application.

## Check Coverage Again

After adding tests:

```bash
pytest --cov=app --cov-report=term-missing
```

For example:

```text
Name                         Stmts   Miss  Cover
------------------------------------------------
app/api/auth.py                 22      3    86%
app/security/auth.py            18      2    89%
...
------------------------------------------------
TOTAL                          126     18    86%
```

Now:

```text
86% > 80%
```

so:

```bash
pytest --cov=app --cov-fail-under=80
```

will pass.

## Do Not Just Lower the Requirement

You could change:

```yaml
--cov-fail-under=80
```

to:

```yaml
--cov-fail-under=70
```

but this usually isn't the best first solution.

If CI tells you:

```text
77.78%
```

and your requirement is:

```text
80%
```

the useful question is:

> "Which important application behavior haven't I tested?"

rather than:

> "How can I make CI accept 77.78%?"

Lowering the threshold may be reasonable for an early prototype, but it should be an intentional project decision.

## `term-missing` Is Useful

This option:

```bash
--cov-report=term-missing
```

is especially useful because it shows the exact uncovered lines:

```text
Missing
-------
15-22
28-38
```

You can then inspect the code:

```bash
nl -ba app/api/auth.py
```

or:

```bash
sed -n '1,120p' app/api/auth.py
```

and determine which behavior those lines represent.

## Generate an HTML Report

For larger projects, generate an HTML coverage report:

```bash
pytest --cov=app --cov-report=html
```

This creates:

```text
htmlcov/
```

Open:

```text
htmlcov/index.html
```

The report lets you see which lines and branches are covered.

You can also combine reports:

```bash
pytest \
  --cov=app \
  --cov-report=term-missing \
  --cov-report=html
```

## GitHub Actions

Your CI might contain:

```yaml
- name: Run tests
  run: |
    pytest --cov=app \
           --cov-report=term-missing \
           --cov-fail-under=80
```

You don't need to change this if `80%` is your intended project standard.

The CI pipeline then becomes:

```text
Install dependencies
        ↓
Run migrations
        ↓
Lint
        ↓
Format check
        ↓
Run tests
        ↓
Measure coverage
        ↓
Coverage >= 80%?
       / \
     yes  no
      ↓    ↓
    pass  fail
```

## Common Mistake

Do not assume:

```text
100% tests passed
```

means:

```text
100% code covered
```

They measure different things.

For example:

```text
5 tests
5 passed
```

could still produce:

```text
Coverage: 60%
```

because the tests may only exercise the successful path.

## Lesson

Code coverage measures **how much of your code is executed by your tests**.

It does not measure whether your code is good, secure, or correct.

For example:

```text
100% coverage
```

does not guarantee:

```text
100% correctness
```

But a coverage threshold can prevent important parts of the application from having no tests at all.

For your project, a useful workflow is:

```text
Implement feature
      ↓
Write tests
      ↓
Run pytest
      ↓
Check uncovered lines
      ↓
Add meaningful tests
      ↓
Coverage >= 80%
      ↓
Push to GitHub
      ↓
GitHub Actions passes
```

The key lesson is:

> **A coverage failure means your tests passed, but your test suite does not exercise enough of the application code to meet the configured coverage threshold.**
