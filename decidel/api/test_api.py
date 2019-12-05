import pytest

route = "/v1/decidels/"

valid_json = {
    "title": "What movie to watch",
    "options": [
        {"title": "Die Hard", "isRemoved": False},
        {"title": "Die Hard 3", "isRemoved": False},
        {"title": "The Rock", "isRemoved": False},
    ],
    "deciders": [{"name": "Jon", "isNext": True}, {"name": "Bob", "isNext": False},],
    "history": [],
}

update_json = {
    "title": "What movie to watch",
    "options": [
        {"title": "Die Hard", "isRemoved": False},
        {"title": "Die Hard 3", "isRemoved": True},
        {"title": "The Rock", "isRemoved": False},
    ],
    "deciders": [{"name": "Jon", "isNext": False}, {"name": "Bob", "isNext": True},],
    "history": [{"userName": "Bob", "action": "REMOVED", "title": "Die Hard 3"}],
}

invalid_json_cases = [
    {},
    {
        "title": "What movie to watch",
        "options": [{"title": "Not Enough options", "isRemoved": False},],
        "deciders": [
            {"name": "Jon", "isNext": True},
            {"name": "Bob", "isNext": False},
        ],
        "history": [],
    },
    {
        "title": "What movie to watch",
        "options": [
            {"title": "Die Hard", "isRemoved": False},
            {"title": "Die Hard 3", "isRemoved": False},
            {"title": "The Rock", "isRemoved": False},
        ],
        "deciders": [{"name": "Not enough deciders", "isNext": True},],
        "history": [],
    },
    {
        "title": "What movie to watch",
        "options": [
            {"foo": "Malformed"},
            {"title": "Die Hard 3", "isRemoved": False},
            {"title": "The Rock", "isRemoved": False},
        ],
        "deciders": [
            {"name": "Jon", "isNext": True},
            {"name": "Bob", "isNext": False},
        ],
        "history": [],
    },
    {
        "title": "What movie to watch",
        "options": [
            {"title": "Die Hard", "isRemoved": False},
            {"title": "Die Hard 3", "isRemoved": False},
            {"title": "The Rock", "isRemoved": False},
        ],
        "deciders": [{"foo": "Malformed"}, {"name": "Bob", "isNext": False},],
        "history": [],
    },
    {
        "title": "What movie to watch",
        "options": [{"title": "Not Enough options", "isRemoved": False},],
        "deciders": [
            {"name": "Jon", "isNext": True},
            {"name": "Bob", "isNext": False},
        ],
        "history": [{"username": "Jon", "title": "Malformed", "action": "FOO"}],
    },
]


def create(client, json=None):
    if json is None:
        json = valid_json

    res = client.post(route, json=json)
    return res.get_json()["id"]


def test_create(client):
    res = client.post(route, json=valid_json)
    assert res.status_code == 201

    created = res.get_json()
    expected = {"id": created["id"]}
    expected.update(valid_json)
    assert created == expected

    # Assert that the resource was actually created
    res = client.get("{}{}".format(route, created["id"]))
    assert res.status_code == 200
    assert res.get_json() == expected


@pytest.mark.parametrize("invalid_json", invalid_json_cases)
def test_create_invalid(invalid_json, client):
    res = client.post(route, json=invalid_json)
    assert res.status_code == 400


def test_update(client):
    id = create(client)

    res = client.put("{}{}".format(route, id), json=update_json)
    assert res.status_code == 200
    expected = {"id": id}
    expected.update(update_json)
    assert res.get_json() == expected

    # Assert that the resource was actually updated
    res = client.get("{}{}".format(route, id))
    assert res.status_code == 200
    assert res.get_json() == expected


@pytest.mark.parametrize("invalid_json", invalid_json_cases)
def test_update_invalid(invalid_json, client):
    res = client.put("{}{}".format(route, create(client)), json=invalid_json)
    assert res.status_code == 400


def test_update_not_found(client):
    res = client.put("{}{}".format(route, 1), json=update_json)
    assert res.status_code == 404


def test_get_not_found(client):
    res = client.get("{}{}".format(route, 1))
    assert res.status_code == 404
