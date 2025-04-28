import re
from datetime import date, timedelta

import pytest
from freezegun import freeze_time

from src.UserManager import UserManager
from src.User import User

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

EMAIL_RE = re.compile(r"[^@]+@[^@]+\.[^@]+")


def make_user(email="u@mail.com",
              username="user",
              country="Romania",
              phone="+40123456789",
              born=date(2000, 1, 1)):
    """Factory for quickly creating User instances in tests."""
    return User(email, username, country, phone, born)


@pytest.fixture()
def um() -> UserManager:
    """Provide a *fresh* UserManager for every test."""
    return UserManager()


# ---------------------------------------------------------------------------
# Unit tests
# ---------------------------------------------------------------------------

@pytest.mark.parametrize(
    "preloaded, probe, expected",
    [
        pytest.param(["exists@mail.com"], "exists@mail.com", True,  id="email-exists"),
        pytest.param([],                  "ghost@mail.com",  False, id="email-missing"),
    ],
)
def test_email_exists(um, preloaded, probe, expected):
    um.users.extend(make_user(m) for m in preloaded)
    assert um.email_exists(probe) is expected


@pytest.mark.parametrize(
    "candidate, expected",
    [
        pytest.param("good@mail.com", True,  id="valid"),
        pytest.param("badmail",       False, id="no-at-sign"),
    ],
)
def test_validate_email(um, candidate, expected):
    assert um.validate_email(candidate) is expected
    # Quick sanity-check of the regex itself
    if expected:
        assert EMAIL_RE.fullmatch(candidate)


@pytest.mark.parametrize(
    "phone, country, ok",
    [
        pytest.param("+40123456789", "Romania",  True,  id="ro-matching-prefix"),
        pytest.param("+40123456789", "Germany",  False, id="prefix-country-mismatch"),
        pytest.param("123456",       "Romania",  False, id="unknown-prefix"),
    ],
)
def test_validate_phone_prefix(um, phone, country, ok):
    assert um.validate_phone_prefix(phone, country) is ok


# ---------------------------------------------------------------------------
# create_user high-level contract
# ---------------------------------------------------------------------------

# *Error* scenarios first ----------------------------------------------------

INVALID_CREATE_PARAMS = [
    pytest.param("badmail", "validuser", "Romania", "+40123456789", "2000-01-01",
                 400, "Invalid email",                           id="invalid-email"),

    pytest.param("ok@mail.com", "validuser", "Romania", "+40123456789", "not-a-date",
                 400, "Invalid birth date",                       id="invalid-date-format"),

    # Freeze clock so “future” is stable.
    pytest.param("ok@mail.com", "validuser", "Romania", "+40123456789",
                 (date(2025, 1, 1) + timedelta(days=1)).isoformat(),
                 400, "Birth date is in the future",              id="date-in-future"),

    pytest.param("u1@mail.com", "usr", "Romania", "+40123456789", "2000-01-01",
                 400, "Username too short",                       id="username-too-short"),

    pytest.param("u2@mail.com", "u" * 21, "Romania", "+40123456789", "2000-01-01",
                 400, "Username too long",                        id="username-too-long"),

    pytest.param("u3@mail.com", "validuser", "Germany", "+40123456789", "2000-01-01",
                 400, "Phone number prefix does not match the country",
                 id="prefix-country-mismatch"),

    pytest.param("u4@mail.com", "validuser", "Romania", "12345678", "2000-01-01",
                 400, "Phone number prefix does not match the country",
                 id="unknown-prefix"),
]


@freeze_time("2025-01-01")
@pytest.mark.parametrize(
    "email, username, country, phone, bdate, exp_status, exp_msg",
    INVALID_CREATE_PARAMS,
)
def test_create_user_validation_errors(
        um, email, username, country, phone, bdate, exp_status, exp_msg):
    """Every invalid-input variant should yield the documented (status, msg)."""
    if exp_msg == "Email already exists":
        um.users.append(make_user(email=email))

    status, msg = um.create_user(email, username, country, phone, bdate)
    assert (status, msg) == (exp_status, exp_msg)


# *Exception* branch ---------------------------------------------------------

def test_create_user_bubbles_up_exception(monkeypatch, um):
    """If the underlying save logic throws, the wrapper should re-raise."""
    def boom(*_, **__):
        raise RuntimeError("Simulated exception")

    monkeypatch.setattr(um, "_persist_new_user", boom, raising=True)

    with pytest.raises(RuntimeError, match="Simulated exception"):
        um.create_user(
            email="err@mail.com",
            username="validuser",
            country="Romania",
            phone_number="+40123456789",
            birth_date_str="2000-01-01",
        )


# *Happy path* ---------------------------------------------------------------

def test_create_user_happy_path(um):
    """All fields valid ➞ user is persisted and a 200/status message returned."""
    status, msg = um.create_user(
        email="new@mail.com",
        username="validuser",
        country="Romania",
        phone_number="+40123456789",
        birth_date_str="2000-01-01",
    )

    assert (status, msg) == (200, "User successfully created")
    assert any(u.email == "new@mail.com" for u in um.users)
