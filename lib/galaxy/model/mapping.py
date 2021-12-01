"""
This module no longer contains the mapping of data model classes to the
relational database.
The module will be revised during migration from SQLAlchemy Migrate to Alembic.
"""

import logging
from threading import local
from typing import Optional, Type

from galaxy import model
from galaxy.model import mapper_registry
from galaxy.model.base import SharedModelMapping
from galaxy.model.security import GalaxyRBACAgent

log = logging.getLogger(__name__)

metadata = mapper_registry.metadata


class GalaxyModelMapping(SharedModelMapping):
    security_agent: GalaxyRBACAgent
    thread_local_log: Optional[local]
    create_tables: bool
    User: Type
    GalaxySession: Type


def init(
    file_path,
    engine,
    map_install_models=False,
    object_store=None,
    use_pbkdf2=True,
    thread_local_log: Optional[local] = None
) -> GalaxyModelMapping:
    model.Dataset.file_path = file_path
    model.Dataset.object_store = object_store
    model.User.use_pbkdf2 = use_pbkdf2

    model_modules = [model]
    if map_install_models:
        from galaxy.model import tool_shed_install
        model_modules.append(tool_shed_install)

    model_mapping = GalaxyModelMapping(model_modules, engine=engine)
    model_mapping.security_agent = GalaxyRBACAgent(model_mapping)
    model_mapping.thread_local_log = thread_local_log
    return model_mapping
