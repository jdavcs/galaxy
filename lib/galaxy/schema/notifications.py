import json
from datetime import datetime
from enum import Enum
from typing import (
    Any,
    List,
    Optional,
    Union,
)

from pydantic import (
    AnyUrl,
    Field,
)
from pydantic.utils import GetterDict
from typing_extensions import (
    Annotated,
    Literal,
)

from galaxy.schema.fields import (
    DecodedDatabaseIdField,
    EncodedDatabaseIdField,
)
from galaxy.schema.schema import (
    CreateTimeField,
    Model,
    UpdateTimeField,
)


class NotificationVariant(str, Enum):
    """The notification variant communicates the intent or relevance of the notification."""

    info = "info"
    warning = "warning"
    urgent = "urgent"


# Register a new category by adding it to the corresponding Enum:
# - NotificationCategory: these notification categories will be always received by the user.
# - OptionalNotificationCategory: these notifications can be opt-out by the user.
# Then register the content model further down below.


class MandatoryNotificationCategory(str, Enum):
    """These notification categories cannot be opt-out by the user.

    The user will always receive notifications from these categories.
    """

    broadcast = "broadcast"


class PersonalNotificationCategory(str, Enum):
    """These notification categories can be opt-out by the user and will be
    displayed in the notification preferences.
    """

    message = "message"
    new_history_shared = "new_history_shared"
    new_workflow_shared = "new_workflow_shared"
    new_page_shared = "new_page_shared"
    new_visualization_shared = "new_visualization_shared"
    # TODO: enable this and create content model when we have a hook for completed workflows
    # workflow_execution_completed = "workflow_execution_completed"


NotificationCategory = Union[MandatoryNotificationCategory, PersonalNotificationCategory]


class MessageNotificationContentBase(Model):
    subject: str
    message: str  # markdown?


class ActionLink(Model):
    action_name: str
    link: AnyUrl


# Create the corresponding model for the registered category below and
# add it to AnyNotificationContent Union.


class BroadcastNotificationContent(MessageNotificationContentBase):
    category: Literal[MandatoryNotificationCategory.broadcast] = MandatoryNotificationCategory.broadcast
    action_links: Optional[List[ActionLink]]


class MessageNotificationContent(MessageNotificationContentBase):
    category: Literal[PersonalNotificationCategory.message] = PersonalNotificationCategory.message


class NewSharedItemNotificationContent(Model):
    item_id: EncodedDatabaseIdField
    owner_id: EncodedDatabaseIdField


class NewHistorySharedNotificationContent(NewSharedItemNotificationContent):
    category: Literal[PersonalNotificationCategory.new_history_shared] = PersonalNotificationCategory.new_history_shared


class NewWorkflowSharedNotificationContent(NewSharedItemNotificationContent):
    category: Literal[
        PersonalNotificationCategory.new_workflow_shared
    ] = PersonalNotificationCategory.new_workflow_shared


class NewPageSharedNotificationContent(NewSharedItemNotificationContent):
    category: Literal[PersonalNotificationCategory.new_page_shared] = PersonalNotificationCategory.new_page_shared


class NewVisualizationSharedNotificationContent(NewSharedItemNotificationContent):
    category: Literal[
        PersonalNotificationCategory.new_visualization_shared
    ] = PersonalNotificationCategory.new_visualization_shared


AnyNotificationContent = Annotated[
    Union[
        BroadcastNotificationContent,
        MessageNotificationContent,
        NewHistorySharedNotificationContent,
        NewWorkflowSharedNotificationContent,
        NewPageSharedNotificationContent,
        NewVisualizationSharedNotificationContent,
    ],
    Field(discriminator="category"),
]


class NotificationGetter(GetterDict):
    """Helper to convert a Notification ORM model into a NotificationResponse.
    For more information: https://docs.pydantic.dev/usage/models/#data-binding
    """

    def get(self, key: Any, default: Any = None) -> Any:
        # The `content` column of the ORM model is a JSON string that needs to be passed
        # as a dictionary to the `from_orm` constructor to build the correct `AnyNotificationContent`.
        if key in {"content"} and isinstance(self._obj.content, str):
            return json.loads(self._obj.content)

        return super().get(key, default)


class NotificationResponse(Model):
    id: EncodedDatabaseIdField
    source: str
    category: NotificationCategory
    variant: NotificationVariant
    create_time: datetime = CreateTimeField
    update_time: datetime = UpdateTimeField
    publication_time: datetime
    expiration_time: Optional[datetime]
    content: AnyNotificationContent

    class Config:
        orm_mode = True
        getter_dict = NotificationGetter


class UserNotificationResponse(NotificationResponse):
    category: PersonalNotificationCategory
    seen_time: Optional[datetime]
    favorite: bool
    deleted: bool


class BroadcastNotificationResponse(NotificationResponse):
    category: Literal[MandatoryNotificationCategory.broadcast] = MandatoryNotificationCategory.broadcast


class UserNotificationListResponse(Model):
    __root__: List[UserNotificationResponse]


class BroadcastNotificationListResponse(Model):
    __root__: List[BroadcastNotificationResponse]


class NotificationStatusSummary(Model):
    total_unread_count: int
    notifications: List[UserNotificationResponse]
    broadcasts: List[BroadcastNotificationResponse]


class NotificationCreateData(Model):
    source: str
    category: NotificationCategory
    variant: NotificationVariant
    content: AnyNotificationContent
    publication_time: Optional[datetime]
    expiration_time: Optional[datetime]


class NotificationRecipients(Model):
    user_ids: List[DecodedDatabaseIdField] = Field(default=[])
    group_ids: List[DecodedDatabaseIdField] = Field(default=[])
    role_ids: List[DecodedDatabaseIdField] = Field(default=[])


class NotificationCreateRequest(Model):
    recipients: NotificationRecipients
    notification: NotificationCreateData


class BroadcastNotificationCreateRequest(NotificationCreateData):
    category: Literal[MandatoryNotificationCategory.broadcast] = MandatoryNotificationCategory.broadcast
    content: BroadcastNotificationContent


class NotificationCreatedResponse(Model):
    total_notifications_sent: int
    notification: NotificationResponse


class NotificationUpdateRequest(Model):
    def has_changes(self) -> bool:
        """Whether the notification update request contains at least one change."""
        return any(getattr(self, field) is not None for field in self.__fields__.keys())


class UserNotificationUpdateRequest(NotificationUpdateRequest):
    seen: Optional[bool]
    favorite: Optional[bool]
    deleted: Optional[bool]


class NotificationBroadcastUpdateRequest(NotificationUpdateRequest):
    source: Optional[str]
    variant: Optional[NotificationVariant]
    publication_time: Optional[datetime]
    expiration_time: Optional[datetime]


class NotificationsBatchRequest(Model):
    notification_ids: List[DecodedDatabaseIdField]


class UserNotificationsBatchUpdateRequest(NotificationsBatchRequest):
    changes: UserNotificationUpdateRequest


class NotificationsBatchUpdateResponse(Model):
    updated_count: int


class NotificationChannelSettings(Model):
    push: bool
    # email: bool # Not supported for now
    # matrix: bool # Possible future Matrix.org integration?


class NotificationCategorySettings(Model):
    category: PersonalNotificationCategory
    enabled: bool
    channels: NotificationChannelSettings


class UpdateUserNotificationPreferencesRequest(Model):
    preferences: List[NotificationCategorySettings]


class UserNotificationPreferencesResponse(Model):
    __root__: List[NotificationCategorySettings]
