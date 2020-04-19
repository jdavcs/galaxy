import os
from collections import namedtuple
from datetime import timedelta

import pytest

from galaxy import config
import galaxy.util.properties
from galaxy.util import listify

TestData = namedtuple('TestData', ('key', 'expected', 'loaded'))

"""
Test or not:
- config_dict?
- non-schema properties? maybe...
"""

# this should go away
DO_NOT_TEST = [
    'database_connection',  # TODO broken?
    'object_store_store_by',
    'pretty_datetime_format',
    'heartbeat_log',
    'statsd_host',
    'disable_library_comptypes',
    'use_remote_user',
    'ftp_upload_dir_template',
    'workflow_resource_params_mapper',
    'user_tool_filters',
    'user_tool_section_filters',
    'user_tool_label_filters',
    'amqp_internal_connection',
]

#def expected_database_connection(_default):  TODO
#    path = os.path.abspath('database/universe.sqlite?isolation_level=IMMEDIATE')
#    return 'sqlite:////{}'.format(path)




class ExpectedValues:

    RESOLVERS = {
        'password_expiration_period': timedelta,
        'toolbox_filter_base_modules': listify,
        'mulled_channels': listify,
        'user_library_import_symlink_whitelist': listify,
        'tool_filters': listify,
        'tool_label_filters': listify,
        'tool_section_filters': listify,
        'persistent_communication_rooms': listify,
        'tool_config_file': listify,
        'tool_data_table_config_path': listify,
    }
    """
    RESOLVERS is used to generated the expected value for config options
        key: config option
        value: str|callable
    The callable will be called with a single argument, which is the default value  of the config option.
    """

    def __init__(self, config):
        self._config = config
        self._load_paths()

    def _load_paths(self):
        self._expected_paths = {
            'admin_tool_recommendations_path': self._in_config_dir('tool_recommendations_overwrite.yml'),
            'auth_config_file': self._in_config_dir('auth_conf.xml'),
            'build_sites_config_file': self._in_sample_dir('build_sites.yml.sample'),
            'builds_file_path': self._in_root_dir('tool-data/shared/ucsc/builds.txt'),
            'citation_cache_data_dir': self._in_data_dir('citations/data'),
            'citation_cache_lock_dir': self._in_data_dir('citations/locks'),
            'cluster_files_directory': self._in_data_dir('pbs'),
            'config_dir': self._in_config_dir(),
            'data_dir': self._in_data_dir(),
            'data_manager_config_file': self._in_config_dir('data_manager_conf.xml'),
            'datatypes_config_file': self._in_sample_dir('datatypes_conf.xml.sample'),
            'dependency_resolvers_config_file': self._in_config_dir('dependency_resolvers_conf.xml'),
            'dynamic_proxy_session_map': self._in_data_dir('session_map.sqlite'),
            'file_path': self._in_data_dir('objects'),
            'galaxy_data_manager_data_path': self._in_root_dir('tool-data'),
            'integrated_tool_panel_config': self._in_managed_config_dir('integrated_tool_panel.xml'),
            'interactivetools_map': self._in_data_dir('interactivetools_map.sqlite'),
            'involucro_path': self._in_root_dir('involucro'),
            'job_config_file': self._in_config_dir('job_conf.xml'),
            'job_metrics_config_file': self._in_sample_dir('job_metrics_conf.xml.sample'),
            'job_resource_params_file': self._in_config_dir('job_resource_params_conf.xml'),
            'len_file_path': self._in_root_dir('tool-data/shared/ucsc/chrom'),
            'managed_config_dir': self._in_managed_config_dir(),
            'markdown_export_css': self._in_config_dir('markdown_export.css'),
            'markdown_export_css_invocation_reports': self._in_config_dir('markdown_export_invocation_reports.css'),
            'markdown_export_css_pages': self._in_config_dir('markdown_export_pages.css'),
            'migrated_tools_config': self._in_managed_config_dir('migrated_tools_conf.xml'),
            'mulled_resolution_cache_data_dir': self._in_data_dir('mulled/data'),
            'mulled_resolution_cache_lock_dir': self._in_data_dir('mulled/locks'),
            'new_file_path': self._in_data_dir('tmp'),
            'object_store_config_file': self._in_config_dir('object_store_conf.xml'),
            'oidc_backends_config_file': self._in_config_dir('oidc_backends_config.xml'),
            'oidc_config_file': self._in_config_dir('oidc_config.xml'),
            'openid_consumer_cache_path': self._in_data_dir('openid_consumer_cache'), 
            'sanitize_whitelist_file': self._in_managed_config_dir('sanitize_whitelist.txt'),
            'shed_data_manager_config_file': self._in_managed_config_dir('shed_data_manager_conf.xml'),
            'shed_tool_config_file': self._in_managed_config_dir('shed_tool_conf.xml'),
            'shed_tool_data_path': self._in_root_dir('tool-data'),
            'shed_tool_data_table_config': self._in_managed_config_dir('shed_tool_data_table_conf.xml'),
            'template_cache_path': self._in_data_dir('compiled_templates'),
            'tool_config_file': self._in_sample_dir('tool_conf.xml.sample'),
            'tool_data_path': self._in_root_dir('tool-data'),
            'tool_data_table_config_path': self._in_sample_dir('tool_data_table_conf.xml.sample'),
            'tool_path': self._in_root_dir('tools'),
            'tool_sheds_config_file': self._in_config_dir('tool_sheds_conf.xml'),
            'tool_test_data_directories': self._in_root_dir('test-data'),
            'user_preferences_extra_conf_path': self._in_config_dir('user_preferences_extra_conf.yml'),
            'whitelist_file': self._in_config_dir('disposable_email_whitelist.conf'),
            'workflow_resource_params_file': self._in_config_dir('workflow_resource_params_conf.xml'),
            'workflow_schedulers_config_file': self._in_config_dir('workflow_schedulers_conf.xml'),
        }
    
    def _in_root_dir(self, path=None):
        return self._in_dir(self._config.root, path)
    
    def _in_config_dir(self, path=None):
        return self._in_dir(self._config.config_dir, path)
    
    def _in_data_dir(self, path=None):
        return self._in_dir(self._config.data_dir, path)
    
    def _in_managed_config_dir(self, path=None):
        return self._in_dir(self._config.managed_config_dir, path)
    
    def _in_sample_dir(self, path=None):
        return self._in_dir(self._config.sample_config_dir, path)

    def _in_dir(self, _dir, path):
        return os.path.join(_dir, path) if path else _dir

    def get_value(self, key, data):
        value = data.get('default')
        # 1. If this is a path, resolve it
        if key in self._expected_paths:
            value = self._expected_paths[key]
        # 2. AFTER resolving paths, apply callable resolver, if found
        if key in ExpectedValues.RESOLVERS:
            resolver = ExpectedValues.RESOLVERS[key]
            if callable(resolver):
                value = resolver(value)
            else:
                value = resulver
        return value


@pytest.fixture
def mock_config_file(monkeypatch):
    # Set this to return None to force the creation of base config directories
    # in _set_config_directories()
    monkeypatch.setattr(config, 'find_config_file', lambda x: None)


@pytest.fixture
def mock_config_running_from_source(monkeypatch, mock_config_file):
    monkeypatch.setattr(config, 'running_from_source', True)


@pytest.fixture
def mock_config_running_not_from_source(monkeypatch, mock_config_file):
    monkeypatch.setattr(config, 'running_from_source', False)


@pytest.fixture
def appconfig(monkeypatch):
    return config.Configuration()


def test_root(appconfig):
    assert appconfig.root == os.path.abspath('.')


def test_base_config_if_running_from_source(mock_config_running_from_source, appconfig):
    assert not appconfig.config_file
    assert appconfig.config_dir == os.path.join(appconfig.root, 'config')
    assert appconfig.data_dir == os.path.join(appconfig.root, 'database')
    assert appconfig.managed_config_dir == appconfig.config_dir


def test_base_config_if_running_not_from_source(mock_config_running_not_from_source, appconfig):
    assert not appconfig.config_file
    assert appconfig.config_dir == os.getcwd()
    assert appconfig.data_dir == os.path.join(appconfig.config_dir, 'data')
    assert appconfig.managed_config_dir == os.path.join(appconfig.data_dir, 'config')


def test_common_base_config(appconfig):
    assert appconfig.shed_tools_dir == os.path.join(appconfig.data_dir, 'shed_tools')
    assert appconfig.sample_config_dir == \
       os.path.join(appconfig.root, 'lib', 'galaxy', 'config', 'sample')


def get_config_data():
    configuration = config.Configuration()
    ev = ExpectedValues(configuration)
    items = ((k, v) for k, v in configuration.schema.app_schema.items() if k not in DO_NOT_TEST)
    for key, data in items:
        expected = ev.get_value(key, data)
        loaded = getattr(configuration, key)
        test_data = TestData(key=key, expected=expected, loaded=loaded)
        yield pytest.param(test_data)


def get_key(test_data):
    return test_data.key


@pytest.mark.parametrize('test_data', get_config_data(), ids=get_key)
def test_config_defaults(test_data):
    assert test_data.expected == test_data.loaded



#EXPECTED_PATHS = {
#    'admin_tool_recommendations_path': 'config/tool_recommendations_overwrite.yml',
#    'auth_config_file': 'config/auth_conf.xml',
#    'build_sites_config_file': 'lib/galaxy/config/sample/build_sites.yml.sample',
#    'builds_file_path': 'tool-data/shared/ucsc/builds.txt',
#    'citation_cache_data_dir': 'database/citations/data',
#    'citation_cache_lock_dir': 'database/citations/locks',
#    'cluster_files_directory': 'database/pbs',
#    'config_dir': 'config',
#    'data_dir': 'database',
#    'data_manager_config_file': 'config/data_manager_conf.xml',
#    'datatypes_config_file': 'lib/galaxy/config/sample/datatypes_conf.xml.sample',
#    'dependency_resolvers_config_file': 'config/dependency_resolvers_conf.xml',
#    'dynamic_proxy_session_map': 'database/session_map.sqlite',
#    'file_path': 'database/objects',
#    'galaxy_data_manager_data_path': 'tool-data',
#    'integrated_tool_panel_config': 'config/integrated_tool_panel.xml',
#    'interactivetools_map': 'database/interactivetools_map.sqlite',
#    'involucro_path': 'involucro',
#    'job_config_file': 'config/job_conf.xml',
#    'job_metrics_config_file': 'lib/galaxy/config/sample/job_metrics_conf.xml.sample',
#    'job_resource_params_file': 'config/job_resource_params_conf.xml',
#    'len_file_path': 'tool-data/shared/ucsc/chrom',
#    'managed_config_dir': 'config',
#    'markdown_export_css': 'config/markdown_export.css',
#    'markdown_export_css_invocation_reports': 'config/markdown_export_invocation_reports.css',
#    'markdown_export_css_pages': 'config/markdown_export_pages.css',
#    'migrated_tools_config': 'config/migrated_tools_conf.xml',
#    'mulled_resolution_cache_data_dir': 'database/mulled/data',
#    'mulled_resolution_cache_lock_dir': 'database/mulled/locks',
#    'new_file_path': 'database/tmp',
#    'object_store_config_file': 'config/object_store_conf.xml',
#    'oidc_backends_config_file': 'config/oidc_backends_config.xml',
#    'oidc_config_file': 'config/oidc_config.xml',
#    'openid_consumer_cache_path': 'database/openid_consumer_cache', 
#    'sanitize_whitelist_file': 'config/sanitize_whitelist.txt',
#    'shed_data_manager_config_file': 'config/shed_data_manager_conf.xml',
#    'shed_tool_config_file': 'config/shed_tool_conf.xml',
#    'shed_tool_data_path': 'tool-data',
#    'shed_tool_data_table_config': 'config/shed_tool_data_table_conf.xml',
#    'template_cache_path': 'database/compiled_templates',
#    'tool_config_file': 'lib/galaxy/config/sample/tool_conf.xml.sample',
#    'tool_data_path': 'tool-data',
#    'tool_data_table_config_path': 'lib/galaxy/config/sample/tool_data_table_conf.xml.sample',
#    'tool_path': 'tools',
#    'tool_sheds_config_file': 'config/tool_sheds_conf.xml',
#    'tool_test_data_directories': 'test-data',
#    'user_preferences_extra_conf_path': 'config/user_preferences_extra_conf.yml',
#    'whitelist_file': 'config/disposable_email_whitelist.conf',
#    'workflow_resource_params_file': 'config/workflow_resource_params_conf.xml',
#    'workflow_schedulers_config_file': 'config/workflow_schedulers_conf.xml',
#}



