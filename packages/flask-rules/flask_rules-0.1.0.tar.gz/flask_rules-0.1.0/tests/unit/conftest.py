import pytest

from rules.permissions import permissions


@pytest.fixture(autouse=True)
def reset_ruleset():
    def _reset(ruleset):
        for k in list(ruleset.keys()):
            ruleset.pop(k)

    _reset(permissions)
    yield
    _reset(permissions)
