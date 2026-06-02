def test_hent_access_token(boss_client):
    response = boss_client.hent_access_token()
    assert response.status_code == 200
    data = response.json()
    assert data is not None
    assert isinstance(data.get("access_token"), str)


def test_dan_gracerapport(boss_client):
    response = boss_client.dan_gracerapport()
    assert response is not None


def test_hent_systemer(boss_client):
    response = boss_client.hent_systemer()
    assert response is not None


def test_marker_bruger_som_slettet(boss_client):
    test_user_id = "xxxxx"
    response = boss_client.marker_bruger_som_slettet(test_user_id)
    assert response.status_code == 200
