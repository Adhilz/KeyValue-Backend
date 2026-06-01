from auth.utils import hash_password, verify_password
import pytest


@pytest.fixture
def hashed():
    return hash_password("Secret123")


@pytest.fixture
def test_verify_password_accepts_correct_password(hashed):

    assert verify_password("Secret123", hashed) is True


def test_verify_password_rejects_wrong_password(hashed):

    assert verify_password("wrong-pass", hashed) is False


def test_verify_password_rejects_empty_string(hashed):

    assert verify_password("", hashed) is False
