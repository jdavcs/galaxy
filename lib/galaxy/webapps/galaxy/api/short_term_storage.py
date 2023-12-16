"""
API operations around galaxy.short_term_storage infrastructure.
"""
from uuid import UUID

from galaxy.short_term_storage import (
    ShortTermStorageMonitor,
    ShortTermStorageServeCancelledInformation,
    ShortTermStorageServeCompletedInformation,
)
from galaxy.webapps.base.api import GalaxyFileResponse
from . import (
    depends,
    Router,
)

router = Router(tags=["short_term_storage"])


class FastAPIShortTermStorage:
    @router.get(
        "/api/short_term_storage/{storage_request_id}/ready",
        summary="Determine if specified storage request ID is ready for download.",
        response_description="Boolean indicating if the storage is ready.",
    )
    def is_ready(
        storage_request_id: UUID,
        short_term_storage_monitor: ShortTermStorageMonitor = depends(ShortTermStorageMonitor),  # type: ignore[type-abstract]  # https://github.com/python/mypy/issues/4717
    ) -> bool:
        storage_target = short_term_storage_monitor.recover_target(storage_request_id)
        return short_term_storage_monitor.is_ready(storage_target)

    @router.get(
        "/api/short_term_storage/{storage_request_id}",
        summary="Serve the staged download specified by request ID.",
        response_description="Raw contents of the file.",
        response_class=GalaxyFileResponse,
        responses={
            200: {
                "description": "The archive file containing the History.",
            },
            204: {
                "description": "Request was cancelled without an exception condition recorded.",
            },
        },
    )
    def serve(
        storage_request_id: UUID,
        short_term_storage_monitor: ShortTermStorageMonitor = depends(ShortTermStorageMonitor),  # type: ignore[type-abstract]  # https://github.com/python/mypy/issues/4717
    ):
        storage_target = short_term_storage_monitor.recover_target(storage_request_id)
        serve_info = short_term_storage_monitor.get_serve_info(storage_target)
        if isinstance(serve_info, ShortTermStorageServeCompletedInformation):
            return GalaxyFileResponse(
                path=serve_info.target.path,
                media_type=serve_info.mime_type,
                filename=serve_info.filename,
            )

        assert isinstance(serve_info, ShortTermStorageServeCancelledInformation)
        raise serve_info.message_exception
