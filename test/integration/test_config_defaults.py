import os

from base import integration_util


class ConfigDefaultsTestCase(integration_util.IntegrationTestCase):
    """
    Test automatic creation of configuration properties and assignment of
    default values specified in the schema.
    """
    def get_default(self, key):
        return self._app.config.appschema[key]['default']

   # def test_default_database_engine_option_pool_size(self):
   #     expect = self.get_default('database_engine_option_pool_size')
   #     assert expect == self._app.config.database_engine_option_pool_size

   # def test_default_database_engine_option_max_overflow(self):
   #     expect = self.get_default('database_engine_option_max_overflow')
   #     assert expect == self._app.config.database_engine_option_max_overflow

   # def test_default_database_engine_option_pool_recycle(self):
   #     expect = self.get_default('database_engine_option_pool_recycle')
   #     assert expect == self._app.config.database_engine_option_pool_recycle

   # def test_default_database_engine_option_server_side_cursors(self):
   #     expect = self.get_default('database_engine_option_server_side_cursors')
   #     assert expect == self._app.config.database_engine_option_server_side_cursors

   # def test_default_database_query_profiling_proxy(self):
   #     expect = self.get_default('database_query_profiling_proxy')
   #     assert expect == self._app.config.database_query_profiling_proxy

   #def test_default_slow_query_log_threshold(self):
   #    expect = self.get_default('slow_query_log_threshold')
   #    assert expect == self._app.config.slow_query_log_threshold

   #def test_default_enable_per_request_sql_debugging(self):
   #    expect = self.get_default('enable_per_request_sql_debugging')
   #    assert expect == self._app.config.enable_per_request_sql_debugging

   #def test_default_database_auto_migrate(self):
   #    expect = self.get_default('database_auto_migrate')
   #    assert expect == self._app.config.database_auto_migrate

   #def test_default_database_wait(self):
   #    expect = self.get_default('database_wait')
   #    assert expect == self._app.config.database_wait

   #def test_default_database_wait_attempts(self):
   #    expect = self.get_default('database_wait_attempts')
   #    assert expect == self._app.config.database_wait_attempts

   #def test_default_database_wait_sleep(self):
   #    expect = self.get_default('database_wait_sleep')
   #    assert expect == self._app.config.database_wait_sleep

   # def test_default_file_path(self):
   #     # This value is a path; it is resolved during initial configuration
   #     # loading w.r.t. another directory. This test compares only the last
   #     # segment of this option to its schema default.
   #     expect = self.get_default('file_path')
   #     assert expect == os.path.basename(self._app.config.file_path)

   # def test_default_new_file_path(self):
   #     pass  # TODO: cannot be tested with current setup

   # def test_default_tool_config_file(self):  #TODO fails
   #     expect = self.get_default('tool_config_file')
   #     assert expect == self._app.config.tool_config_file

   # def test_default_shed_tool_config_file(self): #TODO fails, can be fixed.
   #     # This value is a path; it is resolved during initial configuration
   #     # loading w.r.t. another directory. This test compares only the last
   #     # segment of this option to its schema default.
   #     expect = self.get_default('shed_tool_config_file')
   #     assert expect == os.path.basename(self._app.config.shed_tool_config_file)

   # def test_default_check_migrate_tools(self):
   #     expect = self.get_default('check_migrate_tools')
   #     assert expect == self._app.config.check_migrate_tools

   # def test_default_migrated_tools_config(self):
   #     # This value is a path; it is resolved during initial configuration
   #     # loading w.r.t. another directory. This test compares only the last
   #     # segment of this option to its schema default.
   #     expect = self.get_default('migrated_tools_config')
   #     assert expect == os.path.basename(self._app.config.migrated_tools_config)

   # def test_default_integrated_tool_panel_config(self):
   #     # This value is a path; it is resolved during initial configuration
   #     # loading w.r.t. another directory. This test compares only the last
   #     # segment of this option to its schema default.
   #     expect = self.get_default('integrated_tool_panel_config')
   #     assert expect == os.path.basename(self._app.config.integrated_tool_panel_config)

   # def test_default_tool_path(self):
   #     # This value is a path; it is resolved during initial configuration
   #     # loading w.r.t. another directory. This test compares only the last
   #     # segment of this option to its schema default.
   #     expect = self.get_default('tool_path')
   #     assert expect == os.path.basename(self._app.config.tool_path)

   # def test_default_tool_dependency_dir(self):
   #     # This value is a path; it is resolved during initial configuration
   #     # loading w.r.t. another directory. This test compares only the last
   #     # segment of this option to its schema default.
   #     expect = self.get_default('tool_dependency_dir')
   #     assert expect == os.path.basename(self._app.config.tool_dependency_dir)

#    def test_default_dependency_resolvers_config_file(self):
#       # TODO remove config/ from default value
#        # This value is a path; it is resolved during initial configuration
#        # loading w.r.t. another directory. This test compares only the last
#        # segment of this option to its schema default.
#        expect = self.get_default('dependency_resolvers_config_file')
#        assert expect == os.path.basename(self._app.config.dependency_resolvers_config_file)

#    def test_default_conda_debug(self):
#        expect = self.get_default('conda_debug')
#        assert expect == self._app.config.conda_debug
#
#    def test_default_conda_ensure_channels(self):
#        expect = self.get_default('conda_ensure_channels')
#        assert expect == self._app.config.conda_ensure_channels
#
#    def test_default_conda_use_local(self):
#        expect = self.get_default('conda_use_local')
#        assert expect == self._app.config.conda_use_local

#    def test_default_conda_auto_install(self):
#        expect = self.get_default('conda_auto_install')
#        assert expect == self._app.config.conda_auto_install
#
#    def test_default_conda_auto_init(self):
#        expect = self.get_default('conda_auto_init')
#        assert expect == self._app.config.conda_auto_init
#
#    def test_default_conda_copy_dependencies(self): # TODO fails
#        expect = self.get_default('conda_copy_dependencies')
#        assert expect == self._app.config.conda_copy_dependencies

#    def test_default_use_cached_dependency_manager(self):
#        expect = self.get_default('use_cached_dependency_manager')
#        assert expect == self._app.config.use_cached_dependency_manager

#    def test_default_precache_dependencies(self):
#        expect = self.get_default('precache_dependencies')
#        assert expect == self._app.config.precache_dependencies

# tool_sheds_config_file : TODO: remove config/ from default

   # def test_default_watch_tools(self):
   #     expect = self.get_default('watch_tools')
   #     assert expect == self._app.config.watch_tools

#    def test_default_watch_job_rules(self):
#        expect = self.get_default('watch_job_rules')
#        assert expect == self._app.config.watch_job_rules
#
#    def test_default_watch_core_config(self):
#        expect = self.get_default('watch_core_config')
#        assert expect == self._app.config.watch_core_config
#
#    def test_default_legacy_eager_objectstore_initialization(self):
#        expect = self.get_default('legacy_eager_objectstore_initialization')
#        assert expect == self._app.config.legacy_eager_objectstore_initialization

    #def test_default_enable_mulled_containers(self):
    #    expect = self.get_default('enable_mulled_containers')
    #    assert expect == self._app.config.enable_mulled_containers

    #def test_default_involucro_auto_init(self):
    #    expect = self.get_default('involucro_auto_init')
    #    assert expect == self._app.config.involucro_auto_init

    ##def test_default_mulled_channels(self): # TODO fails
    ##    expect = self.get_default('mulled_channels')
    ##    assert expect == self._app.config.mulled_channels

    #def test_default_enable_tool_shed_check(self):
    #    expect = self.get_default('enable_tool_shed_check')
    #    assert expect == self._app.config.enable_tool_shed_check

    #def test_default_hours_between_check(self):
    #    expect = self.get_default('hours_between_check')
    #    assert expect == self._app.config.hours_between_check

    #def test_default_manage_dependency_relationships(self):
    #    expect = self.get_default('manage_dependency_relationships')
    #    assert expect == self._app.config.manage_dependency_relationships

    #tool_data_table_config_path  # TODO remove config/ from default
    # shed_tool_data_table_config # TODO remove config/ from default

   # def test_default_tool_data_path(self):
   #     # This value is a path; it is resolved during initial configuration
   #     # loading w.r.t. another directory. This test compares only the last
   #     # segment of this option to its schema default.
   #     expect = self.get_default('tool_data_path')
   #     assert expect == os.path.basename(self._app.config.tool_data_path)

   # def test_default_watch_tool_data_dir(self):
   #     expect = self.get_default('watch_tool_data_dir')
   #     assert expect == self._app.config.watch_tool_data_dir

    #def test_default_builds_file_path(self): # TODO fails
    #    expect = self.get_default('builds_file_path')
    #    assert expect == self._app.config.builds_file_path

   # def test_default_len_file_path(self): # TODO fails
   #     expect = self.get_default('len_file_path')
   #     assert expect == self._app.config.len_file_path

    # datatypes_config_file # TODO remove config/

   # def test_default_sniff_compressed_dynamic_datatypes_default(self):
   #     expect = self.get_default('sniff_compressed_dynamic_datatypes_default')
   #     assert expect == self._app.config.sniff_compressed_dynamic_datatypes_default

   # def test_default_datatypes_disable_auto(self):
   #     expect = self.get_default('datatypes_disable_auto')
   #     assert expect == self._app.config.datatypes_disable_auto

   # def test_default_visualization_plugins_directory(self):
   #     expect = self.get_default('visualization_plugins_directory')
   #     assert expect == self._app.config.visualization_plugins_directory

   # def test_default_tour_config_dir(self): # TODO fails
   #     expect = self.get_default('tour_config_dir')
   #     assert expect == self._app.config.tour_config_dir

   # def test_default_webhooks_dir(self):# TODO fails
   #     expect = self.get_default('webhooks_dir')
   #     assert expect == self._app.config.webhooks_dir

    #def test_default_job_working_directory(self):# TODO fails
    #    expect = self.get_default('job_working_directory')
    #    assert expect == self._app.config.job_working_directory

    #def test_default_cluster_files_directory(self):
    #    expect = self.get_default('cluster_files_directory')
    #    assert expect == os.path.basename(self._app.config.cluster_files_directory)

   # def test_default_template_cache_path(self):# TODO fails
   #     expect = self.get_default('template_cache_path')
   #     assert expect == self._app.config.template_cache_path

   # def test_default_check_job_script_integrity(self):
   #     expect = self.get_default('check_job_script_integrity')
   #     assert expect == self._app.config.check_job_script_integrity

   # def test_default_check_job_script_integrity_count(self):
   #     expect = self.get_default('check_job_script_integrity_count')
   #     assert expect == self._app.config.check_job_script_integrity_count

   # def test_default_check_job_script_integrity_sleep(self):
   #     expect = self.get_default('check_job_script_integrity_sleep')
   #     assert expect == self._app.config.check_job_script_integrity_sleep

   # def test_default_default_job_shell(self):
   #     expect = self.get_default('default_job_shell')
   #     assert expect == self._app.config.default_job_shell

   # def test_default_citation_cache_type(self):
   #     expect = self.get_default('citation_cache_type')
   #     assert expect == self._app.config.citation_cache_type

   #def test_default_citation_cache_data_dir(self): # TODO fails
   #    expect = self.get_default('citation_cache_data_dir')
   #    assert expect == self._app.config.citation_cache_data_dir

   #def test_default_citation_cache_lock_dir(self):  # TODO fails
   #    expect = self.get_default('citation_cache_lock_dir')
   #    assert expect == self._app.config.citation_cache_lock_dir

   #def test_default_object_store_config_file(self):  # TODO remove config
   #    expect = self.get_default('object_store_config_file')
   #    assert expect == self._app.config.object_store_config_file

   # def test_default_object_store_store_by(self):   # TODO fails
   #     expect = self.get_default('object_store_store_by')
   #     assert expect == self._app.config.object_store_store_by
#
#    def test_default_smtp_ssl(self):
#        expect = self.get_default('smtp_ssl')
#        assert expect == self._app.config.smtp_ssl
#
#    def test_default_registration_warning_message(self):
#        expect = self.get_default('registration_warning_message')
#        assert expect == self._app.config.registration_warning_message
#
    #def test_default_user_activation_on(self):
    #    expect = self.get_default('user_activation_on')
    #    assert expect == self._app.config.user_activation_on

    #def test_default_activation_grace_period(self):
    #    expect = self.get_default('activation_grace_period')
    #    assert expect == self._app.config.activation_grace_period

    #def test_default_inactivity_box_content(self):
    #    expect = self.get_default('inactivity_box_content')
    #    assert expect == self._app.config.inactivity_box_content

   ## def test_default_password_expiration_period(self): # TODO FAILS  
   ##     expect = self.get_default('password_expiration_period')
   ##     assert expect == self._app.config.password_expiration_period

    #def test_default_session_duration(self):
    #    expect = self.get_default('session_duration')
    #    assert expect == self._app.config.session_duration

    #def test_default_display_servers(self):
    #    expect = self.get_default('display_servers')
    #    assert expect == self._app.config.display_servers

    #def test_default_enable_old_display_applications(self):
    #    expect = self.get_default('enable_old_display_applications')
    #    assert expect == self._app.config.enable_old_display_applications

    #def test_default_interactivetools_enable(self):
    #    expect = self.get_default('interactivetools_enable')
    #    assert expect == self._app.config.interactivetools_enable

    #def test_default_visualizations_visible(self):
    #    expect = self.get_default('visualizations_visible')
    #    assert expect == self._app.config.visualizations_visible

    #def test_default_message_box_visible(self):
    #    expect = self.get_default('message_box_visible')
    #    assert expect == self._app.config.message_box_visible

    #def test_default_message_box_class(self):
    #    expect = self.get_default('message_box_class')
    #    assert expect == self._app.config.message_box_class

   # def test_default_pretty_datetime_format(self):  #TODO fails
   #     expect = self.get_default('pretty_datetime_format')
   #     assert expect == self._app.config.pretty_datetime_format

# user_preferences_extra_conf_path # TODO fails remove config/

    #def test_default_default_locale(self):  #TODO fails
    #    expect = self.get_default('default_locale')
    #    assert expect == self._app.config.default_locale

   # def test_default_galaxy_infrastructure_url(self)::  #TODO fails
   #     expect = self.get_default('galaxy_infrastructure_url')
   #     assert expect == self._app.config.galaxy_infrastructure_url

   # def test_default_galaxy_infrastructure_web_port(self):  #TODO fails
   #     expect = self.get_default('galaxy_infrastructure_web_port')
   #     assert expect == self._app.config.galaxy_infrastructure_web_port

   # def test_default_welcome_url(self):
   #     expect = self.get_default('welcome_url')
   #     assert expect == self._app.config.welcome_url

   # def test_default_logo_url(self):
   #     expect = self.get_default('logo_url')
   #     assert expect == self._app.config.logo_url

   # def test_default_wiki_url(self):
   #     expect = self.get_default('wiki_url')
   #     assert expect == self._app.config.wiki_url

   # def test_default_support_url(self):
   #     expect = self.get_default('support_url')
   #     assert expect == self._app.config.support_url

   # def test_default_citation_url(self):
   #     expect = self.get_default('citation_url')
   #     assert expect == self._app.config.citation_url

   # def test_default_search_url(self):
   #     expect = self.get_default('search_url')
   #     assert expect == self._app.config.search_url

   # def test_default_mailing_lists_url(self):
   #     expect = self.get_default('mailing_lists_url')
   #     assert expect == self._app.config.mailing_lists_url

   # def test_default_screencasts_url(self):
   #     expect = self.get_default('screencasts_url')
   #     assert expect == self._app.config.screencasts_url

   # def test_default_genomespace_ui_url(self):
   #     expect = self.get_default('genomespace_ui_url')
   #     assert expect == self._app.config.genomespace_ui_url

   # def test_default_static_enabled(self):
   #     expect = self.get_default('static_enabled')
   #     assert expect == self._app.config.static_enabled

   # def test_default_static_cache_time(self):
   #     expect = self.get_default('static_cache_time')
   #     assert expect == self._app.config.static_cache_time

   # def test_default_static_dir(self):
   #     expect = self.get_default('static_dir')
   #     assert expect == self._app.config.static_dir

   # def test_default_static_images_dir(self):
   #     expect = self.get_default('static_images_dir')
   #     assert expect == self._app.config.static_images_dir

   # def test_default_static_favicon_dir(self):
   #     expect = self.get_default('static_favicon_dir')
   #     assert expect == self._app.config.static_favicon_dir

   # def test_default_static_scripts_dir(self):
   #     expect = self.get_default('static_scripts_dir')
   #     assert expect == self._app.config.static_scripts_dir

   # def test_default_static_style_dir(self):
   #     expect = self.get_default('static_style_dir')
   #     assert expect == self._app.config.static_style_dir

   # def test_default_static_robots_txt(self):
   #     expect = self.get_default('static_robots_txt')
   #     assert expect == self._app.config.static_robots_txt


# TESTING THESE



   #def test_default_(self):
   #    expect = self.get_default('')
   #    assert expect == self._app.config.

   #def test_default_(self):
   #    expect = self.get_default('')
   #    assert expect == self._app.config.

   #def test_default_(self):
   #    expect = self.get_default('')
   #    assert expect == self._app.config.

   #def test_default_(self):
   #    expect = self.get_default('')
   #    assert expect == self._app.config.

   #def test_default_(self):
   #    expect = self.get_default('')
   #    assert expect == self._app.config.

   #def test_default_(self):
   #    expect = self.get_default('')
   #    assert expect == self._app.config.

   #def test_default_(self):
   #    expect = self.get_default('')
   #    assert expect == self._app.config.

   #def test_default_(self):
   #    expect = self.get_default('')
   #    assert expect == self._app.config.

   #def test_default_(self):
   #    expect = self.get_default('')
   #    assert expect == self._app.config.

   #def test_default_(self):
   #    expect = self.get_default('')
   #    assert expect == self._app.config.

   #def test_default_(self):
   #    expect = self.get_default('')
   #    assert expect == self._app.config.

   #def test_default_(self):
   #    expect = self.get_default('')
   #    assert expect == self._app.config.

   #def test_default_(self):
   #    expect = self.get_default('')
   #    assert expect == self._app.config.

   #def test_default_(self):
   #    expect = self.get_default('')
   #    assert expect == self._app.config.

   #def test_default_(self):
   #    expect = self.get_default('')
   #    assert expect == self._app.config.

   #def test_default_(self):
   #    expect = self.get_default('')
   #    assert expect == self._app.config.

   #def test_default_(self):
   #    expect = self.get_default('')
   #    assert expect == self._app.config.

   #def test_default_(self):
   #    expect = self.get_default('')
   #    assert expect == self._app.config.

   #def test_default_(self):
   #    expect = self.get_default('')
   #    assert expect == self._app.config.

   #def test_default_(self):
   #    expect = self.get_default('')
   #    assert expect == self._app.config.

   #def test_default_(self):
   #    expect = self.get_default('')
   #    assert expect == self._app.config.

   #def test_default_(self):
   #    expect = self.get_default('')
   #    assert expect == self._app.config.

   #def test_default_(self):
   #    expect = self.get_default('')
   #    assert expect == self._app.config.

   #def test_default_(self):
   #    expect = self.get_default('')
   #    assert expect == self._app.config.

   #def test_default_(self):
   #    expect = self.get_default('')
   #    assert expect == self._app.config.




