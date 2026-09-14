import pytest
import jwt
import hashlib


from datetime import datetime, timezone


""" 

    Access Token

"""


from app.modules.auth.security.jwt import (
    create_access_token, 
    decode_access_token
)


def test_create_access_token_payload_and_claims():

    user_id = 50
    token = create_access_token(user_id=user_id)
    decoded_payload = decode_access_token(token=token)

    # These check 'sub' matches user_id converted to string
    assert decoded_payload["sub"] == "50"
    assert isinstance(decoded_payload["sub"], str)

    # Check the 'exp' claim is included
    assert "exp" in decoded_payload


def test_create_access_token_expiration_time(expected_duration_seconds):

    user_id = 101
    before_creation = datetime.now(timezone.utc).timestamp()
    token = create_access_token(user_id=user_id)
    after_creation = datetime.now(timezone.utc).timestamp()
    decoded_payload = decode_access_token(token)

    exp_timestamp = decoded_payload["exp"]
    
    # Verify 'exp' falls accurately within the expected range
    assert int(before_creation) + expected_duration_seconds <= exp_timestamp
    assert exp_timestamp <= after_creation + expected_duration_seconds


def test_create_access_token_invalid_secret_fails(algorithms):

    user_id = 1
    token = create_access_token(user_id=user_id)

    with pytest.raises(jwt.InvalidSignatureError):
        jwt.decode(
            token,
            "WRONG_SECRET_KEY",
            algorithms=[algorithms]
        )


"""  

    Refresh Token

"""


from app.modules.auth.security.refresh_token import (
    generate_refresh_token,
    hash_refresh_token
)


def test_generate_refresh_token_returns_unique_strings():

    token_1 = generate_refresh_token()
    token_2 = generate_refresh_token()

    assert isinstance(token_1, str)
    assert isinstance(token_2, str)
    assert len(token_1) > 0

    # Check is two generated token does not match
    assert token_1 != token_2


def test_hash_refresh_token_is_deterministic():

    raw_token = "some-sample_urlsafe_token_string"

    hash_1 = hash_refresh_token(raw_token)
    hash_2 = hash_refresh_token(raw_token)

    assert hash_1 == hash_2


def test_hash_refresh_token_correct_sha256():

    raw_token = "test_token_123"
    expected_hash = hashlib.sha256(raw_token.encode()).hexdigest()
    actual_hash = hash_refresh_token(raw_token)

    assert actual_hash == expected_hash
    assert len(actual_hash) == 64


def test_different_token_produce_different_hashes():

    token_1 = generate_refresh_token()
    token_2 = generate_refresh_token()

    hash_1 = hash_refresh_token(token_1)
    hash_2 = hash_refresh_token(token_2)

    assert hash_1 != hash_2