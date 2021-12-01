from galaxy.model import tool_shed_install as install_model
from galaxy.model.base import ModelMapping
from galaxy.model.tool_shed_install import mapper_registry

metadata = mapper_registry.metadata


def init(engine):
    return ModelMapping([install_model], engine=engine)
