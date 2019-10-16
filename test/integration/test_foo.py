import pytest
from base.driver_util import GalaxyTestDriver

from collections import namedtuple

OptionData = namedtuple(
    'OptionData', ['default_value', 'attribute_value', 'path_resolves_to'])



@pytest.fixture(scope='module')
def driver(request):
    driver = GalaxyTestDriver()
    driver.setup()
    yield driver
    driver.tear_down()


CONFIG_OPTIONS = ['']


@pytest.fixture(scope='module')
def config_data(driver):
    test_params = {}
    for key, data in driver.app.config.appschema.items():
        default_value = data.get('default')
        path_resolves_to = data.get('path_resolves_to')
        attr_value = getattr(driver.app.config, key)
        test_params[key] = OptionData(default_value, attr_value, path_resolves_to)
    return test_params


@pytest.mark.parametrize('mydata', get_config_data())
def test_config_option(mydata, config_data):
    assert True

    #expect = driver.app.config.appschema['slow_query_log_threshold'].get('default', None)
    #assert expect == driver.app.config.slow_query_log_threshold



"""
1. collect all configs from app.config
2. load dict: key > value
3. test uses dict as parameter


"""


#jOPTIONS_IN_ROOT = [
#j    'tool_path',
#j    'involucro_path',
#j    'tool_data_path',
#j    'sanitize_whitelist_file',
#j]
#j
#jOPTIONS_IN_CONFIG_DIR = [
#j    ('migrated_tools_config')
#j    ('integrated_tool_panel_config')
#j]
#j
#jOPTIONS_IN_DATA_DIR = [
#j    'file_path')
#j    'cluster_files_directory')
#j    'citation_cache_data_dir')
#j    'citation_cache_lock_dir')
#j    'dynamic_proxy_session_map')
#j    'openid_consumer_cache_path')
#j]
#j
#jOPTIONS_IN_TOOL_DATA_PATH_DIR = [
#j    'shed_tool_data_path')
#j    'builds_file_path')
#j    'len_file_path')
#j]
#j
#j
#j
#j
#j
#jCONFIG_OPTIONS = [
#j    'database_engine_option_pool_recycle',
#j    'database_engine_option_server_side_cursors',
#j    'database_query_profiling_proxy',
#j    'slow_query_log_threshold',
#j    'enable_per_request_sql_debugging',
#j    'database_auto_migrate',
#j    'database_wait',
#j    'database_wait_attempts',
#j    'database_wait_sleep',
#j    'check_migrate_tools',
#j    'tool_dependency_dir',
#j    'conda_debug',
#j    'conda_ensure_channels',
#j    'conda_use_local',
#j    'conda_auto_install',
#j    'conda_copy_dependencies',
#j    'use_cached_dependency_manager',
#j    'precache_dependencies',
#j    'watch_tools',
#j    'watch_job_rules',
#j    'watch_core_config',
#j    'legacy_eager_objectstore_initialization',
#j    'enable_mulled_containers',
#j    'involucro_auto_init',
#j    'enable_tool_shed_check',
#j    'hours_between_check',
#j    'manage_dependency_relationships',
#j    'watch_tool_data_dir',
#j    'sniff_compressed_dynamic_datatypes_default',
#j    'datatypes_disable_auto',
#j    'visualization_plugins_directory',
#j    'tour_config_dir',
#j    'check_job_script_integrity',
#j    'check_job_script_integrity_count',
#j    'check_job_script_integrity_sleep',
#j    'default_job_shell',
#j    'citation_cache_type',
#j    'smtp_ssl',
#j    'registration_warning_message',
#j    'user_activation_on',
#j    'activation_grace_period',
#j    'inactivity_box_content',
#j    'password_expiration_period',
#j    'session_duration',
#j    'display_servers',
#j    'enable_old_display_applications',
#j    'interactivetools_enable',
#j    'visualizations_visible',
#j    'message_box_visible',
#j    'message_box_class',
#j    'default_locale',
#j    'galaxy_infrastructure_url',
#j    'galaxy_infrastructure_web_port',
#j    'welcome_url',
#j    'logo_url',
#j    'wiki_url',
#j    'support_url',
#j    'citation_url',
#j    'search_url',
#j    'mailing_lists_url',
#j    'screencasts_url',
#j    'genomespace_ui_url',
#j    'static_enabled',
#j    'static_cache_time',
#j    'static_dir',
#j    'static_images_dir',
#j    'static_favicon_dir',
#j    'static_scripts_dir',
#j    'static_style_dir',
#j    'static_robots_txt',
#j    'display_chunk_size',
#j    'apache_xsendfile',
#j    'upstream_gzip',
#j    'x_frame_options',
#j    'dynamic_proxy_manage',
#j    'dynamic_proxy',
#j    'dynamic_proxy_bind_port',
#j    'dynamic_proxy_bind_ip',
#j    'dynamic_proxy_debug',
#j    'dynamic_proxy_external_proxy',
#j    'dynamic_proxy_prefix',
#j    'dynamic_proxy_golang_noaccess',
#j    'dynamic_proxy_golang_clean_interval',
#j    'dynamic_proxy_golang_docker_address',
#j    'auto_configure_logging',
#j    'log_level',
#j    'database_engine_option_echo',
#j    'database_engine_option_echo_pool',
#j    'log_events',
#j    'log_actions',
#j    'fluent_log',
#j    'fluent_host',
#j    'fluent_port',
#j    'sanitize_all_html',
#j    'serve_xss_vulnerable_mimetypes',
#j    'trust_jupyter_notebook_conversion',
#j    'debug',
#j    'use_lint',
#j    'use_profile',
#j    'use_printdebug',
#j    'use_interactive',
#j    'use_heartbeat',
#j    'heartbeat_interval',
#j    'sentry_sloreq_threshold',
#j    'statsd_port',
#j    'statsd_prefix',
#j    'statsd_influxdb',
#j    'user_library_import_dir_auto_creation',
#j    'user_library_import_check_permissions',
#j    'allow_path_paste',
#j    'transfer_manager_port',
#j    'tool_name_boost',
#j    'tool_section_boost',
#j    'tool_description_boost',
#j    'tool_label_boost',
#j    'tool_stub_boost',
#j    'tool_help_boost',
#j    'tool_search_limit',
#j    'tool_enable_ngram_search',
#j    'tool_ngram_minsize',
#j    'tool_ngram_maxsize',
#j    'remote_user_header',
#j    'remote_user_secret',
#j    'normalize_remote_user_email',
#j    'require_login',
#j    'show_welcome_with_login',
#j    'allow_user_creation',
#j    'allow_user_impersonation',
#j    'show_user_prepopulate_form',
#j    'allow_user_dataset_purge',
#j    'new_user_dataset_access_role_default_private',
#j    'expose_user_name',
#j    'expose_user_email',
#j    'enable_beta_gdpr',
#j    'enable_beta_containers_interface',
#j    'enable_beta_workflow_modules',
#j    'default_workflow_export_format',
#j    'force_beta_workflow_scheduled_min_steps',
#j    'force_beta_workflow_scheduled_for_collections',
#j    'parallelize_workflow_scheduling_within_histories',
#j    'maximum_workflow_invocation_duration',
#j    'maximum_workflow_jobs_per_scheduling_iteration',
#j    'history_local_serial_workflow_scheduling',
#j    'enable_oidc',
#j    'enable_openid',
#j    'enable_tool_tags',
#j    'enable_unique_workflow_defaults',
#j    'myexperiment_url',
#j    'ftp_upload_dir_identifier',
#j    'ftp_upload_dir_template',
#j    'enable_quotas',
#j    'expose_potentially_sensitive_job_metrics',
#j    'enable_legacy_sample_tracking_api',
#j    'enable_data_manager_user_view',
#j    'track_jobs_in_database',
#j    'local_task_queue_workers',
#j    'enable_job_recovery',
#j    'max_metadata_value_size',
#j    'outputs_to_working_directory',
#j    'retry_job_output_collection',
#j    'preserve_python_environment',
#j    'real_system_username',
#j    'cache_user_job_count',
#j    'enable_communication_server',
#j    'communication_server_host',
#j    'communication_server_port',
#j    'use_pbkdf2',
#j]





