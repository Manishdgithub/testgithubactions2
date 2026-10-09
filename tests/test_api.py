from fastapi.testclient import TestClient


def test_shorten_url_success(client: TestClient):
    response = client.post(
        "/api/shorten", json={"url": "https://example.com/some/long/path"}
    )
    assert response.status_code == 201
    data = response.json()
    assert "short_code" in data
    assert len(data["short_code"]) == 6
    assert data["original_url"] == "https://example.com/some/long/path"


def test_redirect_and_analytics(client: TestClient):
    # 1. Create short URL
    create_res = client.post("/api/shorten", json={"url": "https://python.org/"})
    code = create_res.json()["short_code"]

    # 2. Hit redirect twice
    res1 = client.get(f"/{code}", follow_redirects=False)
    assert res1.status_code == 307
    assert res1.headers["location"] == "https://python.org/"

    client.get(f"/{code}", follow_redirects=False)

    # 3. Check analytics click count
    analytics_res = client.get(f"/api/analytics/{code}")
    assert analytics_res.status_code == 200
    data = analytics_res.json()
    assert data["clicks"] == 2
    assert data["short_code"] == code


def test_not_found_routes(client: TestClient):
    res_redirect = client.get("/nonexistent")
    assert res_redirect.status_code == 404

    res_analytics = client.get("/api/analytics/nonexistent")
    assert res_analytics.status_code == 404
