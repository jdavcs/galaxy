from typing import (
    Any,
    Dict,
    List,
)

from galaxy import model
from galaxy.exceptions import (
    Conflict,
    ObjectAttributeMissingException,
    ObjectNotFound,
)
from galaxy.managers.base import decode_id
from galaxy.managers.context import ProvidesAppContext
from galaxy.model.base import transaction
from galaxy.model.repository.group import GroupRepository
from galaxy.model.repository.role import RoleRepository
from galaxy.model.repository.user import UserRepository
from galaxy.model.scoped_session import galaxy_scoped_session
from galaxy.schema.fields import (
    DecodedDatabaseIdField,
    EncodedDatabaseIdField,
)
from galaxy.structured_app import MinimalManagerApp
from galaxy.web import url_for


class GroupsManager:
    """Interface/service object shared by controllers for interacting with groups."""

    def __init__(self, app: MinimalManagerApp) -> None:
        self._app = app

    def index(self, trans: ProvidesAppContext):
        """
        Displays a collection (list) of groups.
        """
        rval = []
        group_repo = GroupRepository(trans.sa_session)
        for group in group_repo.get_not_deleted_groups():
            item = group.to_dict(value_mapper={"id": DecodedDatabaseIdField.encode})
            encoded_id = DecodedDatabaseIdField.encode(group.id)
            item["url"] = url_for("group", id=encoded_id)
            rval.append(item)
        return rval

    def create(self, trans: ProvidesAppContext, payload: Dict[str, Any]):
        """
        Creates a new group.
        """
        sa_session = trans.sa_session
        name = payload.get("name", None)
        if name is None:
            raise ObjectAttributeMissingException("Missing required name")
        self._check_duplicated_group_name(sa_session, name)

        group = model.Group(name=name)
        sa_session.add(group)
        encoded_user_ids = payload.get("user_ids", [])
        users = self._get_users_by_encoded_ids(sa_session, encoded_user_ids)
        encoded_role_ids = payload.get("role_ids", [])
        roles = self._get_roles_by_encoded_ids(sa_session, encoded_role_ids)
        trans.app.security_agent.set_entity_group_associations(groups=[group], roles=roles, users=users)
        with transaction(sa_session):
            sa_session.commit()

        encoded_id = DecodedDatabaseIdField.encode(group.id)
        item = group.to_dict(view="element", value_mapper={"id": DecodedDatabaseIdField.encode})
        item["url"] = url_for("group", id=encoded_id)
        return [item]

    def show(self, trans: ProvidesAppContext, group_id: int):
        """
        Displays information about a group.
        """
        encoded_id = DecodedDatabaseIdField.encode(group_id)
        group = self._get_group(trans.sa_session, group_id)
        item = group.to_dict(view="element", value_mapper={"id": DecodedDatabaseIdField.encode})
        item["url"] = url_for("group", id=encoded_id)
        item["users_url"] = url_for("group_users", group_id=encoded_id)
        item["roles_url"] = url_for("group_roles", group_id=encoded_id)
        return item

    def update(self, trans: ProvidesAppContext, group_id: int, payload: Dict[str, Any]):
        """
        Modifies a group.
        """
        sa_session = trans.sa_session
        group = self._get_group(sa_session, group_id)
        name = payload.get("name", None)
        if name:
            self._check_duplicated_group_name(sa_session, name)
            group.name = name
            sa_session.add(group)
        encoded_user_ids = payload.get("user_ids", [])
        users = self._get_users_by_encoded_ids(sa_session, encoded_user_ids)
        encoded_role_ids = payload.get("role_ids", [])
        roles = self._get_roles_by_encoded_ids(sa_session, encoded_role_ids)
        self._app.security_agent.set_entity_group_associations(
            groups=[group], roles=roles, users=users, delete_existing_assocs=False
        )
        with transaction(sa_session):
            sa_session.commit()

    def _check_duplicated_group_name(self, sa_session: galaxy_scoped_session, group_name: str) -> None:
        if GroupRepository(sa_session).get_by_name(group_name):
            raise Conflict(f"A group with name '{group_name}' already exists")

    def _get_group(self, sa_session: galaxy_scoped_session, group_id: int) -> model.Group:
        group = GroupRepository(sa_session).get(group_id)
        if group is None:
            raise ObjectNotFound("Group with the provided id was not found.")
        return group

    def _get_users_by_encoded_ids(
        self, sa_session: galaxy_scoped_session, encoded_user_ids: List[EncodedDatabaseIdField]
    ) -> List[model.User]:
        user_ids = self._decode_ids(encoded_user_ids)
        return UserRepository(sa_session).get_users_by_ids(user_ids)

    def _get_roles_by_encoded_ids(
        self, sa_session: galaxy_scoped_session, encoded_role_ids: List[EncodedDatabaseIdField]
    ) -> List[model.Role]:
        role_ids = self._decode_ids(encoded_role_ids)
        return RoleRepository(sa_session).get_roles_by_ids(role_ids)

    def _decode_id(self, encoded_id: EncodedDatabaseIdField) -> int:
        return decode_id(self._app, encoded_id)

    def _decode_ids(self, encoded_ids: List[EncodedDatabaseIdField]) -> List[int]:
        return [self._decode_id(encoded_id) for encoded_id in encoded_ids]
