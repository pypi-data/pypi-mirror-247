"""Test ProfileService."""

import pytest

from spnkr.services.profile import ProfileService


@pytest.fixture
def service(session):
    return ProfileService(session)


@pytest.mark.asyncio
async def test_get_current_user(session, service: ProfileService):
    session.set_response("get_user.json")
    await service.get_current_user()
    session.get.assert_called_with(
        "https://profile.svc.halowaypoint.com/users/me",
    )


@pytest.mark.asyncio
async def test_get_user_by_gamertag(session, service: ProfileService):
    session.set_response("get_user.json")
    await service.get_user_by_gamertag("MyGamertag")
    session.get.assert_called_with(
        "https://profile.svc.halowaypoint.com/users/gt(MyGamertag)",
    )


@pytest.mark.asyncio
async def test_get_user_by_id(session, service: ProfileService):
    session.set_response("get_user.json")
    await service.get_user_by_id("xuid(2345678901234567)")
    session.get.assert_called_with(
        "https://profile.svc.halowaypoint.com/users/xuid(2345678901234567)",
    )


@pytest.mark.asyncio
async def test_get_users_by_id(session, service: ProfileService):
    session.set_response("get_users.json")
    await service.get_users_by_id(
        ["xuid(1234567890123456)", "xuid(2345678901234567)"]
    )
    session.get.assert_called_with(
        "https://profile.svc.halowaypoint.com/users",
        params={"xuids": [1234567890123456, 2345678901234567]},
    )


@pytest.mark.asyncio
async def test_get_users_by_id_empty(session, service: ProfileService):
    await service.get_users_by_id([])
    session.get.assert_not_called()


@pytest.mark.asyncio
async def test_get_users_by_id_invalid(service: ProfileService):
    with pytest.raises(TypeError):
        await service.get_users_by_id("xuid(1234567890123456)")
