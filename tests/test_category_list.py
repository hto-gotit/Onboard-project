def test_get_categories(client):
    expected = [
        {
            "id": 1,
            "name": "First category"
        },
        {
            "id": 2,
            "name": "Second category"
        }
    ]
    url = '/categories'
    response = client.get(url)
    assert response.get_json() == expected
    assert response.status_code == 200

