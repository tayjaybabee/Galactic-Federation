import pytest
from galactic_federation.domain.entities import PlanetState

@pytest.fixture
def planet_state():
    return PlanetState()
