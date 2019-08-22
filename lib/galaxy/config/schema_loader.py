import yaml
import os
from collections import OrderedDict


class Schema(object):

    def __init__(self, mapping):
        self.app_schema = mapping

    def get_app_option(self, name):
        try:
            raw_option = self.app_schema[name]
        except KeyError:
            raw_option = UNKNOWN_OPTION
        option = OPTION_DEFAULTS.copy()
        option.update(raw_option)
        return option


class AppSchema(Schema):

    def __init__(self, app_desc):
        schema_path = app_desc.schema_path
        app_name = app_desc.app_name
        with open(schema_path, "r") as f:
            config_all = _ordered_load(f)
        self.raw_schema = config_all
        app_schema = config_all["mapping"][app_name]
        super(AppSchema, self).__init__(app_schema["mapping"])
        self.description = config_all.get("desc", None)
        self.reloadable_options = self._load_reloadable_options(app_schema["mapping"])

    def get_reloadable_option_defaults(self):
        option_dict = {}
        for key in self.reloadable_options:
            option_dict[key] = self.get_app_option(key)["default"]
        return option_dict

    def _load_reloadable_options(self, mapping):
        reloadable_options = []
        for key, option in mapping.items():
            if option.get("reloadable", False):
                reloadable_options.append(key)
        return reloadable_options


def _ordered_load(stream):

    class OrderedLoader(yaml.Loader):

        def __init__(self, stream):
            self._root = os.path.split(stream.name)[0]
            super(OrderedLoader, self).__init__(stream)

        def include(self, node):
            filename = os.path.join(self._root, self.construct_scalar(node))
            with open(filename, 'r') as f:
                return yaml.load(f, OrderedLoader)

    def construct_mapping(loader, node):
        loader.flatten_mapping(node)
        return OrderedDict(loader.construct_pairs(node))

    OrderedLoader.add_constructor(
        yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
        construct_mapping)
    OrderedLoader.add_constructor('!include', OrderedLoader.include)

    return yaml.load(stream, OrderedLoader)


