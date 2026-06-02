def test_hent_access_token(boss_client):
    response = boss_client.hent_access_token()
    assert response.status_code == 200
    data = response.json()
    assert data is not None
    assert isinstance(data.get("access_token"), str)

def test_dan_gracerapport(boss_client):
    response = boss_client.dan_gracerapport()
    assert response is not None


    