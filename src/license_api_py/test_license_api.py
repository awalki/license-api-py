import pytest
import respx
from httpx import Response, HTTPStatusError

from license_api_py.main import LicenseAPI, LoginRequest

pytestmark = pytest.mark.anyio

@respx.mock
async def test_successful_login():
    api = LicenseAPI("https://example.com")
    creds = LoginRequest(username="testuser", password="testpass", hwid="ABC-123-XYZ")

    login_route = respx.post("https://example.com/auth/login").mock(
        return_value=Response(200)
    )

    result = await api.login(creds)
    assert result is True
    assert login_route.called, "Login route was not called"

@respx.mock
async def test_login_http_error_raises():
    api = LicenseAPI("https://example.com")
    creds = LoginRequest(username="failuser", password="failpass", hwid="HWID-FAIL")

    respx.post("https://example.com/auth/login").mock(return_value=Response(401))

    with pytest.raises(HTTPStatusError):
        await api.login(creds)