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



    
@pytest.fixture
def patch_allowlist(monkeypatch):
    monkeypatch.setattr(validation_module, "get_email_domain_allowlist_content", lambda a: None)

@pytest.fixture
def patch_blocklist(monkeypatch):
    monkeypatch.setattr(validation_module, "get_email_domain_blocklist_content", lambda a: None)

@pytest.fixture
def patch_check_existing(monkeypatch):
    monkeypatch.setattr(validation_module, "check_for_existing_email", lambda a, b: False)


class TestValidateEmail:
    
    class MockUser:
        pass

    def test_email_is_empty(self):
        assert validate_email(None, "", allow_empty=True) == ""
    
    def test_email_is_user_email(self):
        my_email = "foo"
        my_user = self.MockUser()
        my_user.email = my_email
        assert validate_email(None, my_email, user=my_user) == ""
    
    def test_check_existing(self, monkeypatch, patch_allowlist, patch_blocklist):
        monkeypatch.setattr(validation_module, "check_for_existing_email", lambda a, b: True)
        result = validate_email(None, "duplicate_email@example.com")
        assert "exists" in result
    
        monkeypatch.setattr(validation_module, "check_for_existing_email", lambda a, b: False)
        result = validate_email(None, "unique_email@example.com")
        assert result == ""
    
    def test_allowlist_not_empty(self, monkeypatch, patch_blocklist, patch_check_existing):
        allowlist = ['good_domain.com']
        monkeypatch.setattr(validation_module, "get_email_domain_allowlist_content", lambda a: allowlist)
        assert validate_email(None, "email@good_domain.com") == ""
        assert "enter an allowed domain" in validate_email(None, "email@bad_domain.com")

    def test_ignore_blocklist_if_allowlist_not_empty(self, monkeypatch, patch_check_existing):
        allowlist = ['good_domain.com']
        monkeypatch.setattr(validation_module, "get_email_domain_allowlist_content", lambda a: allowlist)

        # but add that domain to blocklist too!
        blocklist = ['good_domain.com']
        monkeypatch.setattr(validation_module, "get_email_domain_blocklist_content", lambda a: blocklist)

        assert validate_email(None, "email@good_domain.com") == ""  # we expect blocklist to be ignored
