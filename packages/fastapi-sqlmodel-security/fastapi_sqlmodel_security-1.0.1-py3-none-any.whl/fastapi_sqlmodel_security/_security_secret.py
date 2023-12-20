"""Secret dependency."""
import os
import secrets
import uuid
import warnings
from datetime import date, datetime, timedelta
from typing import Optional

from fastapi import Security
from fastapi.security import APIKeyHeader
from starlette.exceptions import HTTPException
from starlette.status import HTTP_403_FORBIDDEN


def generate_secret_key() -> str:
    return str(uuid.uuid4())


def generate_expiration_date(supplied: Optional[date] = None) -> datetime:
    if supplied:
        return datetime.combine(supplied, datetime.min.time())
    else:
        return datetime.now() + timedelta(
            days=int(
                os.environ.get(
                    "FASTAPI_SQLMODEL_SECURITY_AUTOMATIC_EXPIRATION",
                    "15",
                )
            )
        )


class GhostLoadedSecret:
    """Ghost-loaded secret handler"""

    def __init__(self) -> None:
        self._secret = None

    @property
    def value(self):
        if self._secret:
            return self._secret

        else:
            self._secret = self.get_secret_value()
            return self.value

    def get_secret_value(self):
        try:
            secret_value = os.environ["FASTAPI_SQLMODEL_SECURITY_SECRET"]

        except KeyError:
            secret_value = generate_secret_key()

            warnings.warn(
                f"ENVIRONMENT VARIABLE 'FASTAPI_SQLMODEL_SECURITY_SECRET' NOT FOUND\n"
                f"\tGenerated a single-use secret key for this session:\n"
                f"\t{secret_value=}"
            )

        return secret_value


auth_secret = GhostLoadedSecret()


SECRET_KEY_NAME = "x-secret-key"

secret_header = APIKeyHeader(name=SECRET_KEY_NAME, scheme_name="Secret header", auto_error=False)


async def secret_based_security(header_param: Optional[str] = Security(secret_header)):
    """
    Args:
        header_param: parsed header field secret_header

    Returns:
        True if the authentication was successful

    Raises:
        HTTPException if the authentication failed
    """

    if not header_param:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN,
            detail="secret_key must be passed as a header field",
        )

    # We simply return True if the given secret-key has the right value
    if not secrets.compare_digest(header_param, auth_secret.value):
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN,
            detail="Wrong secret key. If not set through environment variable \
                'FASTAPI_SQLMODEL_SECURITY_SECRET', it was "
            "generated automatically at startup and appears in the server logs.",
        )

    else:
        return True
