from galaxy.security.validate_user_input import extract_domain_from_email


def test_extract_domain_from_email():
    assert extract_domain_from_email('foo@bar.com') == 'bar.com'
    assert extract_domain_from_email('foo@foo.bar.com') == 'bar.com'
