import pytest

from rules.permissions import (
    ObjectPermissionBackend,
    add_perm,
    has_perm,
    perm_exists,
    permissions,
    remove_perm,
    set_perm,
)
from rules.predicates import always_false, always_true


def test_permissions_ruleset():
    add_perm("can_edit_book", always_true)
    assert "can_edit_book" in permissions
    assert perm_exists("can_edit_book")
    assert has_perm("can_edit_book")

    with pytest.raises(KeyError):
        add_perm("can_edit_book", always_false)

    set_perm("can_edit_book", always_false)
    assert not has_perm("can_edit_book")

    remove_perm("can_edit_book")
    assert not perm_exists("can_edit_book")


def test_backend():
    backend = ObjectPermissionBackend()
    assert backend.authenticate("someuser", "password") is None

    add_perm("can_edit_book", always_true)
    assert "can_edit_book" in permissions
    assert backend.has_perm(None, "can_edit_book")
    assert backend.has_module_perms(None, "can_edit_book")

    with pytest.raises(KeyError):
        add_perm("can_edit_book", always_true)

    set_perm("can_edit_book", always_false)
    assert not backend.has_perm(None, "can_edit_book")

    remove_perm("can_edit_book")
    assert not perm_exists("can_edit_book")
