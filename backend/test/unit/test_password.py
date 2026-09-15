from app.modules.auth.security.password import verify_password


def test_hash_password_does_not_return_plaintext(password, password_hash):

    assert password_hash != password


def test_correct_password_is_verified(password, password_hash):
    
    assert verify_password(password, password_hash)


def test_wrong_password_is_rejected(password_hash):

    assert not verify_password("wrong-password", password_hash)