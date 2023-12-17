"""
API operations allowing clients to determine datatype supported by Galaxy.
"""
import logging
from typing import (
    cast,
    Dict,
    List,
    Optional,
    Union,
)

from fastapi import Query

from galaxy.datatypes.registry import Registry
from galaxy.managers.datatypes import (
    DatatypeConverterList,
    DatatypeDetails,
    DatatypesCombinedMap,
    DatatypesEDAMDetailsDict,
    DatatypesMap,
    view_converters,
    view_edam_data,
    view_edam_formats,
    view_index,
    view_mapping,
    view_sniffers,
)
from . import (
    depends,
    Router,
)

log = logging.getLogger(__name__)

router = Router(tags=["datatypes"])

ExtensionOnlyQueryParam: Optional[bool] = Query(
    default=True,
    title="Extension only",
    description="Whether to return only the datatype's extension rather than the datatype's details",
)

UploadOnlyQueryParam: Optional[bool] = Query(
    default=True,
    title="Upload only",
    description="Whether to return only datatypes which can be uploaded",
)

IdentifierOnly: Optional[bool] = Query(
    default=True,
    title="prefixIRI only",
    description="Whether to return only the EDAM prefixIRI rather than the EDAM details",
)


@router.get(
    "/api/datatypes",
    summary="Lists all available data types",
    response_description="List of data types",
)
async def index(
    extension_only: Optional[bool] = ExtensionOnlyQueryParam,
    upload_only: Optional[bool] = UploadOnlyQueryParam,
    datatypes_registry: Registry = depends(Registry),
) -> Union[List[DatatypeDetails], List[str]]:
    """Gets the list of all available data types."""
    return view_index(datatypes_registry, extension_only, upload_only)


@router.get(
    "/api/datatypes/mapping",
    summary="Returns mappings for data types and their implementing classes",
    response_description="Dictionary to map data types with their classes",
)
async def mapping(datatypes_registry: Registry = depends(Registry)) -> DatatypesMap:
    """Gets mappings for data types."""
    return view_mapping(datatypes_registry)


@router.get(
    "/api/datatypes/types_and_mapping",
    summary="Returns all the data types extensions and their mappings",
    response_description="Dictionary to map data types with their classes",
)
async def types_and_mapping(
    extension_only: Optional[bool] = ExtensionOnlyQueryParam,
    upload_only: Optional[bool] = UploadOnlyQueryParam,
    datatypes_registry: Registry = depends(Registry),
) -> DatatypesCombinedMap:
    """Combines the datatype information from (/api/datatypes) and the
    mapping information from (/api/datatypes/mapping) into a single
    response."""
    return DatatypesCombinedMap(
        datatypes=view_index(datatypes_registry, extension_only, upload_only),
        datatypes_mapping=view_mapping(datatypes_registry),
    )


@router.get(
    "/api/datatypes/sniffers",
    summary="Returns the list of all installed sniffers",
    response_description="List of datatype sniffers",
)
async def sniffers(datatypes_registry: Registry = depends(Registry)) -> List[str]:
    """Gets the list of all installed data type sniffers."""
    return view_sniffers(datatypes_registry)


@router.get(
    "/api/datatypes/converters",
    summary="Returns the list of all installed converters",
    response_description="List of all datatype converters",
)
async def converters(datatypes_registry: Registry = depends(Registry)) -> DatatypeConverterList:
    """Gets the list of all installed converters."""
    return view_converters(datatypes_registry)


@router.get(
    "/api/datatypes/edam_formats",
    summary="Returns a dictionary/map of datatypes and EDAM formats",
    response_description="Dictionary/map of datatypes and EDAM formats",
)
async def edam_formats(datatypes_registry: Registry = depends(Registry)) -> Dict[str, str]:
    """Gets a map of datatypes and their corresponding EDAM formats."""
    return cast(Dict[str, str], view_edam_formats(datatypes_registry))


@router.get(
    "/api/datatypes/edam_formats/detailed",
    summary="Returns a dictionary of datatypes and EDAM format details",
    response_description="Dictionary of EDAM format details containing the EDAM iri, label, and definition",
    response_model=DatatypesEDAMDetailsDict,
)
async def edam_formats_detailed(datatypes_registry: Registry = depends(Registry)):
    """Gets a map of datatypes and their corresponding EDAM formats.
    EDAM formats contain the EDAM iri, label, and definition."""
    return view_edam_formats(datatypes_registry, True)


@router.get(
    "/api/datatypes/edam_data",
    summary="Returns a dictionary/map of datatypes and EDAM data",
    response_description="Dictionary/map of datatypes and EDAM data",
)
async def edam_data(datatypes_registry: Registry = depends(Registry)) -> Dict[str, str]:
    """Gets a map of datatypes and their corresponding EDAM data."""
    return cast(Dict[str, str], view_edam_data(datatypes_registry))


@router.get(
    "/api/datatypes/edam_data/detailed",
    summary="Returns a dictionary of datatypes and EDAM data details",
    response_description="Dictionary of EDAM data details containing the EDAM iri, label, and definition",
    response_model=DatatypesEDAMDetailsDict,
)
async def edam_data_detailed(datatypes_registry: Registry = depends(Registry)):
    """Gets a map of datatypes and their corresponding EDAM data.
    EDAM data contains the EDAM iri, label, and definition."""
    return view_edam_data(datatypes_registry, True)
