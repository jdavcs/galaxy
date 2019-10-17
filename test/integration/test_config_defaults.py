import os
from datetime import timedelta
import pytest
from base.driver_util import GalaxyTestDriver
from collections import namedtuple
from galaxy.util import listify

OptionData = namedtuple('OptionData', 'key, expected, loaded')

## TODO: this should MAYBE go away once path_resolves_to is set in the schema
RESOLVE = {
    'sanitize_whitelist_file': 'root_dir',
    'tool_data_path': 'root_dir',
    'involucro_path': 'root_dir',
    'tool_path': 'root_dir',
    'migrated_tools_config': 'config_dir',
    'integrated_tool_panel_config': 'config_dir',
    'shed_tool_data_path': 'tool_data_path',
    'builds_file_path': 'tool_data_path',
    'len_file_path': 'tool_data_path',
}

CUSTOM = {
    'password_expiration_period': timedelta,
    'toolbox_filter_base_modules': listify,
    'mulled_channels': listify,
    'user_library_import_symlink_whitelist': listify,
    'tool_filters': listify,
    'tool_label_filters': listify,
    'tool_section_filters': listify,
    'persistent_communication_rooms': listify,
}

# TODO: the following require fixing OR explicit comments on why they are ignored
DO_NOT_TEST = [
    'config_dir',
    'data_dir',
    'new_file_path',
    'logging',
    'dependency_resolution',
    'job_config', 
    'database_connection',
    'database_engine_option_pool_size',
    'database_engine_option_max_overflow',
    'database_template',
    'tool_config_file',
    'shed_tool_config_file',
    'dependency_resolvers_config_file',
    'conda_auto_init',
    'tool_sheds_config_file',
    'tool_data_table_config_path',
    'shed_tool_data_table_config',
    'datatypes_config_file',
    'webhooks_dir',
    'job_working_directory',
    'template_cache_path',
    'object_store_config_file',
    'object_store_store_by',
    'pretty_datetime_format',
    'user_preferences_extra_conf_path',
    'default_locale',
    'galaxy_infrastructure_url',
    'galaxy_infrastructure_web_port',
    'chunk_upload_size',
    'monitor_thread_join_timeout',
    'heartbeat_log',
    'statsd_host',
    'library_import_dir',
    'user_library_import_dir',
    'disable_library_comptypes',
    'tool_test_data_directories',
    'id_secret',
    'use_remote_user',
    'admin_users',
    'allow_user_deletion',
    'oidc_config_file',
    'oidc_backends_config_file',
    'auth_config_file',
    'api_allow_run_as',
    'master_api_key',
    'ftp_upload_purge',
    'expose_dataset_path',
    'data_manager_config_file',
    'shed_data_manager_config_file',
    'galaxy_data_manager_data_path',
    'job_config_file',
    'use_tasked_jobs',
    'retry_metadata_internally',
    'cleanup_job',
    'job_resource_params_file',
    'workflow_resource_params_file',
    'workflow_resource_params_mapper',
    'workflow_schedulers_config_file',
    'user_tool_filters',
    'user_tool_section_filters',
    'user_tool_label_filters',
    'amqp_internal_connection',
]


@pytest.fixture(scope='module')
def driver(request):
    request.addfinalizer(DRIVER.tear_down)
    return DRIVER


def create_driver():
    global DRIVER
    DRIVER = GalaxyTestDriver()
    DRIVER.setup()


def get_config_data():
    create_driver()  # makes loaded DRIVER availbale globally
    parent_dirs = load_parent_dirs()
    items = ((k, v) for k, v in DRIVER.app.config.appschema.items() if k not in DO_NOT_TEST)
    for key, data in items:
        expected_value = get_expected(key, data, parent_dirs)
        loaded_value = getattr(DRIVER.app.config, key)
        data = OptionData(key=key, expected=expected_value, loaded=loaded_value)
        yield pytest.param(data)


def load_parent_dirs():
    parent_dirs = {
        'root_dir': DRIVER.app.config.root,
        'config_dir': DRIVER.app.config.config_dir,
        'data_dir': DRIVER.app.config.data_dir,
        'tool_data_path': DRIVER.app.config.tool_data_path,
    }
    return parent_dirs


def get_expected(key, data, parent_dirs):
    value = data.get('default')

    parent = data.get('path_resolves_to')
    if parent:
        value = resolve(parent_dirs[parent], value)

    if key in RESOLVE:
        parent = RESOLVE[key]
        value = resolve(parent_dirs[parent], value)

    if key in CUSTOM:
        value = CUSTOM[key](value)

    return value


def resolve(parent, child):
    return os.path.join(parent, child) if child else parent


def get_key(option_data):
    return option_data.key


@pytest.mark.parametrize('data', get_config_data(), ids=get_key)
def test_config_option(data, driver):
    assert data.expected == data.loaded
