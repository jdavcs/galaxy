from galaxy.model.security import GalaxyRBACAgent


def test_set_group_user_and_role_associations(make_user, make_role, make_group):
    users = [make_user() for _ in range(3)]
    roles = [make_role() for _ in range(3)]

    user_ids = [users[0].id, users[1].id]  # first and second user
    role_ids = [role.id for role in roles]   # all roles

    group = make_group()
    assert len(group.users) == 0
    assert len(group.roles) == 0

    db.group.set_group_user_and_role_associations(group, user_ids=user_ids, role_ids=role_ids)

    assert len(group.users) == 2
    assert len(group.roles) == 3
    # also verify ids


