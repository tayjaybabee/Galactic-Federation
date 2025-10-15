from galactic_federation.domain.services.issue_engine import DecisionResolver


def test_add_and_mul_effects(planet_state):
    payload = {
        'effects': [
            {'op': 'add', 'path': 'economy.value', 'value': 0.2},
            {'op': 'mul', 'path': 'economy.value', 'value': 0.5},
        ]
    }
    new_state = DecisionResolver().apply_all(planet_state, payload)
    assert 0.0 <= new_state.stats['economy']['value'] <= 1.0
