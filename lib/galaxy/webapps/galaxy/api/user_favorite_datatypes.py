from typing import List

from fastapi import Path

from galaxy.managers.context import ProvidesUserContext
from galaxy.managers.users import UserManager
from . import (
    depends,
    DependsOnTrans,
    Router,
)

router = Router(tags=["user_favorites"])

DatatypePath: str = Path(
    ...,  # Mark this Path parameter as required
    title="Datatype",
    description="Target file extension for target operation.",
)


@router.cbv
class FastAPIUserFavoriteDatatypes:
    user_manager: UserManager = depends(UserManager)

    @router.get(
        "/api/users/current/favorite_datatypes",
        summary="List user favorite datatypes",
        response_description="List of datatypes",
    )
    def index(
        self,
        trans: ProvidesUserContext = DependsOnTrans,
    ) -> List[str]:
        """Gets the list of user's favorite datatypes."""
        return self.user_manager.get_favorite_datatypes(trans.user)

    @router.post(
        "/api/users/current/favorite_datatypes/{datatype}",
        summary="Mark a datatype as the current user's favorite.",
    )
    def create(
        self,
        datatype: str = DatatypePath,
        trans: ProvidesUserContext = DependsOnTrans,
    ) -> str:
        self.user_manager.add_favorite_datatype(trans.user, datatype)
        return datatype

    @router.delete(
        "/api/users/current/favorite_datatypes/{datatype}",
        summary="Unmark a datatype as the current user's favorite.",
    )
    def delete(
        self,
        datatype: str = DatatypePath,
        trans: ProvidesUserContext = DependsOnTrans,
    ) -> None:
        self.user_manager.delete_favorite_datatype(trans.user, datatype)
