import pytest
import os

from boss_client.client import BossClient


@pytest.fixture
def boss_client():
    return BossClient(
        login_url=os.getenv("LOGIN_URL"),
        api_url=os.getenv("API_URL"),
        client_id=os.getenv("CLIENT_ID"),
        client_secret=os.getenv("CLIENT_SECRET"),
        base_url=os.getenv("BASE_URL")
    )