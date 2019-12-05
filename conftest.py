import pytest
from decidel import create_app, redis_store


def create_test_app():
    return create_app(
        test_config=dict(REDIS_URL="redis://:@localhost:6379/1", TESTING=True,)
    )


@pytest.fixture(autouse=True, scope="session")
def redis_cleanup():
    yield
    redis_store.flushdb()


@pytest.fixture(scope="function")
def client():
    app = create_test_app()
    with app.test_client() as client:
        yield client
