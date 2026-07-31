from copy import deepcopy

import pytest
from fastapi.testclient import TestClient

from src.app import activities, app


@pytest.fixture(scope="session")
def original_activities():
    return deepcopy(activities)


@pytest.fixture(autouse=True)
def reset_activities(original_activities):
    activities.clear()
    activities.update(deepcopy(original_activities))


@pytest.fixture
def client():
    return TestClient(app)
