import pytest

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


def test_tag_effect_adds_tag(planet_state):
    payload = {'effects': [{'op': 'tag', 'path': 'tags', 'value': 'test_tag'}]}
    new_state = DecisionResolver().apply_all(planet_state, payload)
    assert 'test_tag' in new_state.tags


@pytest.mark.parametrize('delta,expected', [(1.0, 1.0), (-1.0, 0.0)])
def test_effects_clamped_to_bounds(planet_state, delta, expected):
    payload = {'effects': [{'op': 'add', 'path': 'economy.value', 'value': delta}]}
    new_state = DecisionResolver().apply_all(planet_state, payload)
    assert new_state.stats['economy']['value'] == expected


def test_unknown_operation_raises_value_error(planet_state):
    payload = {'effects': [{'op': 'noop', 'path': 'economy.value', 'value': 0.1}]}
    with pytest.raises(ValueError):
        DecisionResolver().apply_all(planet_state, payload)
