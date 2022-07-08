from galaxy.security.validate_user_input import (
    extract_domain,
    validate_domain_resolves,
    validate_email_str,
    validate_publicname_str,
    validate_email,
)
from galaxy.security import  validate_user_input as validation_module
import pytest

#def test_extract_full_domain():
#    assert extract_domain("jack@foo.com") == "foo.com"
#    assert extract_domain("jack@foo.bar.com") == "foo.bar.com"
#    assert extract_domain("foo.bar.com") == "foo.bar.com"
#    assert extract_domain('"i-like-to-break-email-valid@tors"@foo.com') == "foo.com"
#
#
#def test_extract_base_domain():
#    # Use case: ignore subdomains to filter out disposable email addresses
#    assert extract_domain("jack@foo.com", base_only=True) == "foo.com"
#    assert extract_domain("jack@foo.bar.com", base_only=True) == "bar.com"
#
#
#def test_validate_domain():
#    assert validate_domain_resolves("example.org") == ""
#    assert validate_domain_resolves("this is an invalid domain!") != ""
#
#
#def test_validate_username():
#    assert validate_publicname_str("testuser") == ""
#    assert validate_publicname_str("test.user") == ""
#    assert validate_publicname_str("test-user") == ""
#    assert validate_publicname_str("test@user") != ""
#    assert validate_publicname_str("test user") != ""
#
#
#def test_validate_email_str():
#    assert validate_email_str("test@foo.com") == ""
#    assert validate_email_str("test-dot.user@foo.com") == ""
#    assert validate_email_str("test-plus+user@foo.com") == ""
#    assert validate_email_str("test-ünicode-user@foo.com") == ""
#    assert validate_email_str("test@ünicode-domain.com") == ""
#    assert validate_email_str("test-missing-domain@") != ""
#    assert validate_email_str("@test-missing-local") != ""
#    assert validate_email_str("test-invalid-local\\character@foo.com") != ""
#    assert validate_email_str("test@invalid-domain-character!com") != ""
#    assert validate_email_str("test@newlines.in.address.are.invalid\n\n.com") != ""
#    assert validate_email_str('"i-like-to-break-email-valid@tors"@foo.com') != ""
#    too_long_email = "N" * 255 + "@foo.com"
#    assert validate_email_str(too_long_email) != ""



class MockUser:
    pass

@pytest.fixture
def patch_allowlist(monkeypatch):
    monkeypatch.setattr(validation_module, "get_email_domain_allowlist_content", lambda a: None)

@pytest.fixture
def patch_blocklist(monkeypatch):
    monkeypatch.setattr(validation_module, "get_email_domain_blocklist_content", lambda a: None)

class MockTransaction:
    def __init__(self):
        pass

def test_validate_email__empty():
    assert validate_email(None, "", allow_empty=True) == ""

    my_email = "foo"
    my_user = MockUser()
    my_user.email = my_email
    assert validate_email(None, my_email, user=my_user) == ""


def test_validate_email__check_existing(monkeypatch, patch_allowlist, patch_blocklist):
    monkeypatch.setattr(validation_module, "check_for_existing_email", lambda a, b: True)
    result = validate_email(None, "duplicate_email@example.com")
    assert "exists" in result

    monkeypatch.setattr(validation_module, "check_for_existing_email", lambda a, b: False)
    result = validate_email(None, "unique_email@example.com")
    assert result == ""

#def test_validate_email__allowlist(monkeypatch):
#    allowlist = ['foo@example.com']

