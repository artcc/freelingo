from datetime import date, timedelta
from unittest.mock import AsyncMock, Mock

import pytest
from redis.exceptions import RedisError

from app.routers import admin_analytics as router


@pytest.mark.parametrize("path", ["/api/admin/analytics", "/api/admin/analytics/activity"])
async def test_admin_access_before_cache(
    client, admin_user, test_user, mock_redis, monkeypatch, path
):
    # A warm cache must never bypass authorization.
    assert (await client.get(path, headers=admin_user[1])).status_code == 200
    cache_read = AsyncMock(wraps=mock_redis.get)
    monkeypatch.setattr(mock_redis, "get", cache_read)
    assert (await client.get(path)).status_code == 401
    assert (await client.get(path, headers=test_user[1])).status_code == 403
    cache_read.assert_not_awaited()


async def test_activity_is_independent_and_cache_rolls_at_midnight(client, admin_user, monkeypatch):
    end = date(2026, 6, 2)
    monkeypatch.setattr(router, "progress_today", lambda: end)
    service = router.admin_analytics
    activity = AsyncMock(wraps=service.activity_series)
    summary = AsyncMock()
    usage = AsyncMock()
    monkeypatch.setattr(service, "activity_series", activity)
    monkeypatch.setattr(service, "analytics_summary", summary)
    monkeypatch.setattr(service, "feature_usage", usage)
    url = "/api/admin/analytics/activity"
    response = await client.get(url, headers=admin_user[1])
    assert response.status_code == 200
    assert response.headers["cache-control"] == "private, no-store"
    days = response.json()["days"]
    assert len(days) == 30
    assert days[0] == {"date": "2026-05-03", "learners": 0}
    assert days[-1] == {"date": "2026-06-01", "learners": 0}
    assert (await client.get(url, headers=admin_user[1])).json() == response.json()
    activity.assert_awaited_once()
    end += timedelta(days=1)
    assert (await client.get(url, headers=admin_user[1])).json()["days"][-1]["date"] == "2026-06-02"
    assert activity.await_count == 2
    summary.assert_not_awaited()
    usage.assert_not_awaited()


async def test_bad_token_is_rejected_before_starting_report_snapshot(
    client, db_session, monkeypatch
):
    get_bind = Mock(wraps=db_session.get_bind)
    monkeypatch.setattr(db_session, "get_bind", get_bind)
    response = await client.get("/api/admin/analytics", headers={"Authorization": "Bearer invalid"})
    assert response.status_code == 401
    get_bind.assert_not_called()


async def test_detail_validates_range_and_reuses_fixed_cohorts(client, admin_user, monkeypatch):
    service = router.admin_analytics
    summary = AsyncMock(wraps=service.analytics_summary)
    usage = AsyncMock(wraps=service.feature_usage)
    monkeypatch.setattr(service, "analytics_summary", summary)
    monkeypatch.setattr(service, "feature_usage", usage)
    url = "/api/admin/analytics"
    headers = admin_user[1]
    assert (await client.get(f"{url}?days=365", headers=headers)).status_code == 422
    summary.assert_not_awaited()
    response = await client.get(url, headers=headers)
    assert response.status_code == 200
    assert response.headers["cache-control"] == "private, no-store"
    report = response.json()
    assert report["weekly"] == {"current": 0, "previous": 0}
    assert report["days"] == (await client.get(f"{url}/activity", headers=headers)).json()["days"]
    assert len(report["features"]) == 7
    assert len(report["movement"]) == len(report["activation"]) == len(report["retention"]) == 8
    assert report["population"] == {"last_7": 0, "days_8_30": 0, "over_30": 0, "never": 0}
    assert all(count == 0 for count in report["frequency"].values())
    assert all(feature["repeat_learners"] == 0 for feature in report["features"])
    assert (await client.get(f"{url}?days=30", headers=headers)).json() == report
    assert (await client.get(f"{url}?days=7", headers=headers)).status_code == 200
    summary.assert_awaited_once()
    assert [call.args[-1] for call in usage.await_args_list] == [30, 7]


async def test_activity_works_without_report_cache(client, admin_user, mock_redis, monkeypatch):
    monkeypatch.setattr(mock_redis, "get", AsyncMock(side_effect=RedisError()))
    monkeypatch.setattr(mock_redis, "setex", AsyncMock(side_effect=RedisError()))
    response = await client.get("/api/admin/analytics/activity", headers=admin_user[1])
    assert response.status_code == 200
    assert len(response.json()["days"]) == 30
