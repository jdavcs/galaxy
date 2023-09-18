from typing import (
    Optional,
    TYPE_CHECKING,
)

from galaxy.model import User
from galaxy.model.base import transaction
from galaxy.model.repositories.api_keys import APIKeysRepository
from galaxy.structured_app import BasicSharedApp

if TYPE_CHECKING:
    from galaxy.model import APIKeys


class ApiKeyManager:
    def __init__(self, app: BasicSharedApp):
        self.app = app
        self.apikeys_repo = APIKeysRepository(self.app.model.context)

    def get_api_key(self, user: User) -> Optional["APIKeys"]:
        return self.apikeys_repo.get_api_key(user.id)

    def create_api_key(self, user: User) -> "APIKeys":
        guid = self.app.security.get_new_guid()
        new_key = self.app.model.APIKeys()
        new_key.user_id = user.id
        new_key.key = guid
        sa_session = self.app.model.context
        sa_session.add(new_key)
        with transaction(sa_session):
            sa_session.commit()
        return new_key

    def get_or_create_api_key(self, user: User) -> str:
        # Logic Galaxy has always used - but it would appear to have a race
        # condition. Worth fixing? Would kind of need a message queue to fix
        # in multiple process mode.
        api_key = self.get_api_key(user)
        key = api_key.key if api_key else self.create_api_key(user).key
        return key

    def delete_api_key(self, user: User) -> None:
        """Marks the current user API key as deleted."""
        # Before it was possible to create multiple API keys for the same user although they were not considered valid
        # So all non-deleted keys are marked as deleted for backward compatibility
        self.apikeys_repo.mark_all_as_deleted(user.id)
        sa_session = self.app.model.context
        with transaction(sa_session):
            sa_session.commit()
