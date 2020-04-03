import os
from collections import namedtuple
from datetime import timedelta
import pytest
from galaxy.util import listify
from galaxy_test.driver.driver_util import GalaxyConfigTestDriver
#from galaxy_test.driver.driver_util import GalaxyTestDriver

OptionData = namedtuple('OptionData', ('key', 'expected', 'loaded'))


RESOLVE = {
    'auth_config_file': 'config_dir',
    'builds_file_path': 'tool_data_path',
    'dependency_resolvers_config_file': 'config_dir',
    'integrated_tool_panel_config': 'managed_config_dir',
    'involucro_path': 'root_dir',
    'job_resource_params_file': 'config_dir',
    'len_file_path': 'tool_data_path',
    'object_store_config_file': 'config_dir',
    'oidc_backends_config_file': 'config_dir',
    'oidc_config_file': 'config_dir',
    'sanitize_whitelist_file': 'managed_config_dir',
    'shed_data_manager_config_file': 'managed_config_dir',
    'shed_tool_config_file': 'managed_config_dir',
    'shed_tool_data_path': 'tool_data_path',
    'shed_tool_data_table_config': 'managed_config_dir',
    'tool_data_path': 'root_dir',
    'tool_path': 'root_dir',
    'tool_sheds_config_file': 'config_dir',
    'user_preferences_extra_conf_path': 'config_dir',
    'workflow_resource_params_file': 'config_dir',
    'workflow_schedulers_config_file': 'config_dir',
    'migrated_tools_config': 'config_dir',
}


def expected_default_config_dir(value):
    # expected absolute path to the default config dir (when NO galaxy.yml provided)
    #return os.path.join(DRIVER.app.config.root, 'lib', 'galaxy', 'config', 'sample')
    return os.path.join(DRIVER.app.config.root, 'config')  #, 'lib', 'galaxy', 'config', 'sample')


CUSTOM = {
    #'config_dir': expected_default_config_dir,
    #'data_dir': expected_default_config_dir,  # same as config
    'password_expiration_period': timedelta,
    'toolbox_filter_base_modules': listify,
    'mulled_channels': listify,
    'user_library_import_symlink_whitelist': listify,
    'tool_filters': listify,
    'tool_label_filters': listify,
    'tool_section_filters': listify,
    'persistent_communication_rooms': listify,
    'user_tool_section_filters': listify,
}


DO_NOT_TEST = [
    'amqp_internal_connection',  # may or may not be testable; refactor config/
    'build_sites_config_file',  # broken: remove 'config/' prefix from schema
    'config_dir',  # value overridden for testing
    'data_dir',  # value overridden for testing
    'data_manager_config_file',  # broken: remove 'config/' prefix from schema
    'database_connection',  # untestable; refactor config/__init__ to test
    'datatypes_config_file',  # broken
    'disable_library_comptypes',  # broken: default overridden with empty string
    'ftp_upload_dir_template',  # dynamically sets os.path.sep
    'galaxy_data_manager_data_path',  # broken: review config/, possibly refactor
    'heartbeat_log',  # untestable; refactor config/__init__ to test
    'job_config_file',  # broken: remove 'config/' prefix from schema
    'job_metrics_config_file',
    'managed_config_dir',  # depends on config_dir: see note above
    'markdown_export_css',  # default not used?
    'markdown_export_css_pages',  # default not used?
    'markdown_export_css_invocation_reports',  # default not used?
    'object_store_store_by',  # broken: default overridden
    'pretty_datetime_format',  # untestable; refactor config/__init__ to test
    'statsd_host',  # broken: default overridden with empty string
    'tool_config_file',  # default not used; may or may not be testable
    'tool_data_table_config_path',  # broken: remove 'config/' prefix from schema
    'tool_test_data_directories',  # untestable; refactor config/__init__ to test
    'use_remote_user',  # broken: default overridden
    'user_tool_filters',  # broken: default overridden
    'user_tool_label_filters',  # broken: default overridden
    'workflow_resource_params_mapper',  # broken: remove 'config/' prefix from schema
]

@pytest.fixture(scope='module')
def driver(request):
    request.addfinalizer(DRIVER.tear_down)
    return DRIVER


def create_driver():  # TODO refactor this 
    # Same approach as in functional/test_toolbox_pytest.py:
    # We setup a global driver, so that the driver fixture can tear down the driver.
    # Ideally `create_driver` would be a fixture and clean up after the yield,
    # but that's not compatible with the use use of pytest.mark.parametrize:
    # a fixture is not directly callable, so it cannot be used in place of get_config_data.
    global DRIVER
    DRIVER = GalaxyConfigTestDriver()
    DRIVER.setup()

def get_config():
    create_driver()
    return DRIVER.app.config



def get_config_data():

    def load_parent_dirs():
        return {
            'root_dir': config.root,
            'config_dir': config.config_dir,
            'data_dir': config.data_dir,
            'managed_config_dir': config.managed_config_dir,
            'tool_data_path': config.tool_data_path,
            # sample_config_dir?
            # shed_tools_dir?  
        }

    def resolve(parent, child):
        return os.path.join(parent, child) if child else parent

    def get_expected(key, data):
        value = data.get('default')
        parent = data.get('path_resolves_to') # will this work for more than one step? toposort maybe?
        if parent:
            value = resolve(parent_dirs[parent], value)

        if key in RESOLVE:  # this should be specified in config_schema and done with path_resolves_to
            parent = RESOLVE[key]
            value = resolve(parent_dirs[parent], value)

        if key in CUSTOM:  # apply custom function????
            value = CUSTOM[key](value)

        return value

    config = get_config()
    parent_dirs = load_parent_dirs()
    items = ((k, v) for k, v in config.schema.app_schema.items() if k not in DO_NOT_TEST)
    #items = ((k, v) for k, v in config.schema.app_schema.items())
    for key, data in items:
        expected_value = get_expected(key, data)
        loaded_value = getattr(config, key)
        data = OptionData(key=key, expected=expected_value, loaded=loaded_value)
        yield pytest.param(data)


def get_key(option_data):
    return option_data.key


@pytest.mark.parametrize('data', get_config_data(), ids=get_key)
def test_foo(data, driver):  # 'data' is the OptionData NamedTuple with expected/loaded/key members
   # if data.expected != data.loaded:
   #     s = '\n{}\n{}\n{}\n'.format(data.key, data.expected, data.loaded)
   #     print(s)


   # assert True
    assert data.expected == data.loaded

