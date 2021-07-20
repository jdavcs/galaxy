"""
TODO: documentaion on writing model tests goes here

Example:

TestFoo(BaseTest):  # BaseTest is parent class

    # test table-level properties (e.g. table name, indexes, unique constraints)
    def test_table(self, cls_):  # cls_ is fixture defined in parent class, returns class under test.
        assert cls_.__tablename__ == 'foo'  # assert table name
        assert has_index(cls.__table__, ('foo',))  # second arg is a tuple containg field names

    # test column-mapped fields
    def test_columns(self, session, cls_):
        some_foo, some_bar = 42, 'stuff'  # create test values here
        obj = cls_(foo=some_foo)  # pass test values to constructor
        obj.bar = some_bar  # assign test values to obj if can't pass to constructor

        with persist2(session, obj) as obj_id:  # use context manager to ensure obj is deleted from db on exit.
            stored_obj = get_stored_obj(session, cls_, obj_id)  # retrieve data from db and create new obj.
            # check ALL column-mapped fields
            assert stored_obj.id == obj_id
            assert stored_obj.create_time == create_time
            assert stored_obj.user_id == user_id
            assert stored_obj.key == key

    # test relationship-mapped fields
    def test_relationships(self, session, cls_):
        obj = cls_()  # use minimal possible constructor

        with persist2(session, obj) as obj_id:
            stored_obj = get_stored_obj(session, cls_, obj_id)
            # check ALL relationship-mapped fields

# TODO: ADD MORE EXAMPLES!
# TODO: explain why we test for columns: 
            assert stored_obj.user_id == user_id
            and for relationships:
            assert stored_obj.user.id == user_id
"""

import random
from contextlib import contextmanager
from datetime import datetime, timedelta

import pytest
from sqlalchemy import (
    delete,
    select,
    UniqueConstraint,
)

import galaxy.model.mapping as mapping


class BaseTest:
    @pytest.fixture
    def cls_(self, model):
        """
        Return class under test.
        Assumptions: if the class under test is Foo, then the class grouping
        the tests should be a subclass of BaseTest, named TestFoo.
        """
        prefix = len('Test')
        class_name = self.__class__.__name__[prefix:]
        return getattr(model, class_name)


# TODO remove this
#class Test(BaseTest):
#
#    def test_table(self, cls_):
#        assert cls_.__tablename__ == ''
#
#    def test_columns(self, session, cls_):
#        obj = cls_()
#
#        with persist2(session, obj) as obj_id:
#            stored_obj = get_stored_obj(session, cls_, obj_id)
#            assert stored_obj.id == obj_id
#
#    def test_relationships(self, session, cls_):
#        obj = cls_()
#
#        with persist2(session, obj) as obj_id:
#            stored_obj = get_stored_obj(session, cls_, obj_id)


class TestAPIKeys(BaseTest):

    def test_table(self, cls_):
        assert cls_.__tablename__ == 'api_keys'

    def test_columns(self, session, cls_, user):
        create_time, user_id, key = datetime.now(), user.id, get_random_string()
        obj = cls_(user_id=user_id, key=key, create_time=create_time)

        with persist2(session, obj) as obj_id:
            stored_obj = get_stored_obj(session, cls_, obj_id)
            assert stored_obj.id == obj_id
            assert stored_obj.create_time == create_time
            assert stored_obj.user_id == user_id
            assert stored_obj.key == key

    def test_relationships(self, session, cls_, user):
        user_id, key = user.id, get_random_string()
        obj = cls_(user_id=user.id, key=key)

        with persist2(session, obj) as obj_id:
            stored_obj = get_stored_obj(session, cls_, obj_id)
            assert stored_obj.user.id == user.id


class TestCloudAuthz(BaseTest):

    def test_table(self, cls_):
        assert cls_.__tablename__ == 'cloudauthz'

    def test_columns(self, session, cls_, user, user_authnz_token):
        provider, config, description = 'a', 'b', 'c'
        obj = cls_(user.id, provider, config, user_authnz_token.id, description)

        with persist2(session, obj) as obj_id:
            stored_obj = get_stored_obj(session, cls_, obj_id)
            assert stored_obj.id == obj_id
            assert stored_obj.user_id == user.id
            assert stored_obj.provider == provider
            assert stored_obj.config == config
            assert stored_obj.authn_id == user_authnz_token.id
            assert stored_obj.tokens is None
            assert stored_obj.last_update
            assert stored_obj.last_activity
            assert stored_obj.description == description
            assert stored_obj.create_time
 
    def test_relationships(self, session, cls_, user, user_authnz_token):
        obj = cls_(user.id, None, None, user_authnz_token.id, 'c')

        with persist2(session, obj) as obj_id:
            stored_obj = get_stored_obj(session, cls_, obj_id)
            assert stored_obj.user.id == user.id
            assert stored_obj.authn.id == user_authnz_token.id


class TestDatasetHash(BaseTest):

    def test_table(self, cls_):
        assert cls_.__tablename__ == 'dataset_hash'

    def test_columns(self, session, cls_, dataset):
        hash_function, hash_value, extra_files_path = 'a', 'b', 'c'
        obj = cls_()
        obj.dataset = dataset
        obj.hash_function = hash_function
        obj.hash_value = hash_value
        obj.extra_files_path = extra_files_path
 
        with persist2(session, obj) as obj_id:
            stored_obj = get_stored_obj(session, cls_, obj_id)
            assert stored_obj.id == obj_id
            assert stored_obj.dataset_id == dataset.id
            assert stored_obj.hash_function == hash_function
            assert stored_obj.hash_value == hash_value
            assert stored_obj.extra_files_path == extra_files_path

    def test_relationships(self, session, cls_, dataset):
        obj = cls_()
        obj.dataset = dataset

        with persist2(session, obj) as obj_id:
            stored_obj = get_stored_obj(session, cls_, obj_id)
            assert stored_obj.dataset.id == dataset.id


class TestDatasetSource(BaseTest):

    def test_table(self, cls_):
        assert cls_.__tablename__ == 'dataset_source'

    def test_columns(self, session, cls_, dataset, dataset_source_hash):
        source_uri, extra_files_path, transform = 'a', 'b', 'c'
        obj = cls_()
        obj.dataset = dataset
        obj.source_uri = source_uri
        obj.extra_files_path = extra_files_path
        obj.transform = transform

        with persist2(session, obj) as obj_id:
            stored_obj = get_stored_obj(session, cls_, obj_id)
            assert stored_obj.id == obj_id
            assert stored_obj.dataset_id == dataset.id
            assert stored_obj.source_uri == source_uri
            assert stored_obj.extra_files_path == extra_files_path
            assert stored_obj.transform == transform

    def test_relationships(self, session, cls_, dataset, dataset_source_hash):
        obj = cls_()
        obj.dataset = dataset
        obj.hashes.append(dataset_source_hash)

        with persist2(session, obj) as obj_id:
            stored_obj = get_stored_obj(session, cls_, obj_id)
            assert stored_obj.dataset.id == dataset.id
            assert stored_obj.hashes == [dataset_source_hash]


class TestDatasetSourceHash(BaseTest):

    def test_table(self, cls_):
        assert cls_.__tablename__ == 'dataset_source_hash'

    def test_columns(self, session, cls_, dataset_source):
        hash_function, hash_value = 'a', 'b'
        obj = cls_()
        obj.source = dataset_source
        obj.hash_function = hash_function
        obj.hash_value = hash_value

        with persist2(session, obj) as obj_id:
            stored_obj = get_stored_obj(session, cls_, obj_id)
            assert stored_obj.id == obj_id
            assert stored_obj.dataset_source_id == dataset_source.id
            assert stored_obj.hash_function == hash_function
            assert stored_obj.hash_value == hash_value

    def test_relationships(self, session, cls_, dataset_source):
        obj = cls_()
        obj.source = dataset_source

        with persist2(session, obj) as obj_id:
            stored_obj = get_stored_obj(session, cls_, obj_id)
            assert stored_obj.source.id == dataset_source.id


class TestDatasetPermissions(BaseTest):

    def test_table(self, cls_):
        assert cls_.__tablename__ == 'dataset_permissions'

    def test_columns(self, session, cls_, dataset, role):
        action = 'a'
        create_time = datetime.now()
        update_time = create_time + timedelta(hours=1)
        obj = cls_(action, dataset, role)
        obj.create_time = create_time
        obj.update_time = update_time

        with persist2(session, obj) as obj_id:
            stored_obj = get_stored_obj(session, cls_, obj_id)
            assert stored_obj.id == obj_id
            assert stored_obj.update_time == update_time
            assert stored_obj.action == action
            assert stored_obj.dataset_id == dataset.id
            assert stored_obj.role_id == role.id

    def test_relationships(self, session, cls_, dataset, role):
        obj = cls_(None, dataset, role)

        with persist2(session, obj) as obj_id:
            stored_obj = get_stored_obj(session, cls_, obj_id)
            assert stored_obj.dataset == dataset
            assert stored_obj.role == role


class TestDefaultHistoryPermissions(BaseTest):

    def test_table(self, cls_):
        assert cls_.__tablename__ == 'default_history_permissions'

    def test_columns(self, session, cls_, history, role):
        action = 'a'
        obj = cls_(history, action, role)

        with persist2(session, obj) as obj_id:
            stored_obj = get_stored_obj(session, cls_, obj_id)
            assert stored_obj.id == obj_id
            assert stored_obj.action == action
            assert stored_obj.history_id == history.id
            assert stored_obj.role_id == role.id

    def test_relationships(self, session, cls_, history, role):
        obj = cls_(history, None, role)

        with persist2(session, obj) as obj_id:
            stored_obj = get_stored_obj(session, cls_, obj_id)
            assert stored_obj.history.id == history.id
            assert stored_obj.role == role


class TestDefaultQuotaAssociation(BaseTest):

    def test_table(self, cls_):
        assert cls_.__tablename__ == 'default_quota_association'

    def test_columns(self, session, cls_, quota):
        type_ = cls_.types.REGISTERED
        create_time = datetime.now()
        update_time = create_time + timedelta(hours=1)
        obj = cls_(type_, quota)
        obj.create_time = create_time
        obj.update_time = update_time

        with persist2(session, obj) as obj_id:
            stored_obj = get_stored_obj(session, cls_, obj_id)
            assert stored_obj.id == obj_id
            assert stored_obj.create_time == create_time
            assert stored_obj.update_time == update_time
            assert stored_obj.type == type_
            assert stored_obj.quota_id == quota.id

    def test_relationships(self, session, cls_, quota):
        obj = cls_(cls_.types.REGISTERED, quota)

        with persist2(session, obj) as obj_id:
            stored_obj = get_stored_obj(session, cls_, obj_id)
            assert stored_obj.quota.id == quota.id


class TestDefaultUserPermissions(BaseTest):

    def test_table(self, cls_):
        assert cls_.__tablename__ == 'default_user_permissions'

    def test_columns(self, session, cls_, user, role):
        action = 'a'
        obj = cls_(user, action, role)

        with persist2(session, obj) as obj_id:
            stored_obj = get_stored_obj(session, cls_, obj_id)
            assert stored_obj.id == obj_id
            assert stored_obj.user_id == user.id
            assert stored_obj.action == action
            assert stored_obj.role_id == role.id

    def test_relationships(self, session, cls_, user, role):
        obj = cls_(user, None, role)

        with persist2(session, obj) as obj_id:
            stored_obj = get_stored_obj(session, cls_, obj_id)
            assert stored_obj.user.id == user.id
            assert stored_obj.role.id == role.id


class TestDynamicTool(BaseTest):

    def test_table(self, cls_):
        assert cls_.__tablename__ == 'dynamic_tool'

    def test_columns(self, session, cls_):
        tool_format = 'a'
        tool_id = 'b'
        tool_version = 'c'
        tool_path = 'd'
        tool_directory = 'e'
        uuid = None
        active = True
        hidden = True
        value = 'f'
        create_time = datetime.now()
        update_time = create_time + timedelta(hours=1)
        obj = cls_(tool_format, tool_id, tool_version, tool_path, tool_directory, uuid,
                active, hidden, value)
        obj.create_time = create_time
        obj.update_time = update_time

        with persist2(session, obj) as obj_id:
            stored_obj = get_stored_obj(session, cls_, obj_id)
            assert stored_obj.id == obj_id
            assert stored_obj.uuid
            assert stored_obj.create_time == create_time
            assert stored_obj.update_time == update_time
            assert stored_obj.tool_id == tool_id
            assert stored_obj.tool_version == tool_version
            assert stored_obj.tool_format == tool_format
            assert stored_obj.tool_path == tool_path
            assert stored_obj.tool_directory == tool_directory
            assert stored_obj.hidden == hidden
            assert stored_obj.active == active
            assert stored_obj.value == value

    def test_relationships(self, session, cls_, workflow_step):
        obj = cls_()
        obj.workflow_steps.append(workflow_step)

        with persist2(session, obj) as obj_id:
            stored_obj = get_stored_obj(session, cls_, obj_id)
            assert stored_obj.workflow_steps == [workflow_step]


class TestFormDefinition(BaseTest):

    def test_table(self, cls_):
        assert cls_.__tablename__ == 'form_definition'

    def test_columns(self, session, cls_, form_definition_current):
        name, desc, fields, type, layout = 'a', 'b', 'c', 'd', 'e'
        create_time = datetime.now()
        update_time = create_time + timedelta(hours=1)
        obj = cls_()
        obj.name = name
        obj.desc = desc
        obj.form_definition_current = form_definition_current
        obj.fields = fields
        obj.type = type
        obj.layout = layout
        obj.create_time = create_time
        obj.update_time = update_time

        with persist2(session, obj) as obj_id:
            stored_obj = get_stored_obj(session, cls_, obj_id)
            assert stored_obj.id == obj_id
            assert stored_obj.create_time == create_time
            assert stored_obj.update_time == update_time
            assert stored_obj.name == name
            assert stored_obj.desc == desc
            assert stored_obj.form_definition_current_id == form_definition_current.id
            assert stored_obj.fields == fields
            assert stored_obj.type == type
            assert stored_obj.layout == layout

    def test_relationships(self, session, cls_, form_definition_current):
        obj = cls_(name='a', form_definition_current=form_definition_current)

        with persist2(session, obj) as obj_id:
            stored_obj = get_stored_obj(session, cls_, obj_id)
            assert stored_obj.form_definition_current.id == form_definition_current.id


class TestFormDefinitionCurrent(BaseTest):

    def test_table(self, cls_):
        assert cls_.__tablename__ == 'form_definition_current'

    def test_columns(self, session, cls_, form_definition):
        create_time = datetime.now()
        update_time = create_time + timedelta(hours=1)
        deleted = True
        obj = cls_()
        obj.create_time = create_time
        obj.update_time = update_time
        obj.latest_form = form_definition
        obj.deleted = deleted

        with persist2(session, obj) as obj_id:
            stored_obj = get_stored_obj(session, cls_, obj_id)
            assert stored_obj.id == obj_id
            assert stored_obj.create_time == create_time
            assert stored_obj.update_time == update_time
            assert stored_obj.latest_form_id == form_definition.id
            assert stored_obj.deleted == deleted

    def test_relationships(self, session, cls_, form_definition):
        obj = cls_(form_definition)
        obj.forms.append(form_definition)

        with persist2(session, obj) as obj_id:
            stored_obj = get_stored_obj(session, cls_, obj_id)
            assert stored_obj.latest_form.id == form_definition.id
            assert stored_obj.forms == [form_definition]


class TestFormValues(BaseTest):

    def test_table(self, cls_):
        assert cls_.__tablename__ == 'form_values'

    def test_columns(self, session, cls_, form_definition):
        content = 'a'
        create_time = datetime.now()
        update_time = create_time + timedelta(hours=1)
        obj = cls_()
        obj.form_definition = form_definition
        obj.content = content
        obj.create_time = create_time
        obj.update_time = update_time

        with persist2(session, obj) as obj_id:
            stored_obj = get_stored_obj(session, cls_, obj_id)
            assert stored_obj.id == obj_id
            assert stored_obj.create_time == create_time
            assert stored_obj.update_time == update_time
            assert stored_obj.content == content
            assert stored_obj.form_definition_id == form_definition.id

    def test_relationships(self, session, cls_, form_definition):
        obj = cls_(form_definition)

        with persist2(session, obj) as obj_id:
            stored_obj = get_stored_obj(session, cls_, obj_id)
            assert stored_obj.form_definition.id == form_definition.id


class TestGroupQuotaAssociation(BaseTest):

    def test_table(self, cls_):
        assert cls_.__tablename__ == 'group_quota_association'

    def test_columns(self, session, cls_, group, quota):
        create_time = datetime.now()
        update_time = create_time + timedelta(hours=1)
        obj = cls_(group, quota)
        obj.create_time = create_time
        obj.update_time = update_time

        with persist2(session, obj) as obj_id:
            stored_obj = get_stored_obj(session, cls_, obj_id)
            assert stored_obj.id == obj_id
            assert stored_obj.group_id == group.id
            assert stored_obj.quota_id == quota.id
            assert stored_obj.create_time == create_time
            assert stored_obj.update_time == update_time

    def test_relationships(self, session, cls_, group, quota):
        obj = cls_(group, quota)

        with persist2(session, obj) as obj_id:
            stored_obj = get_stored_obj(session, cls_, obj_id)
            assert stored_obj.group.id == group.id
            assert stored_obj.quota.id == quota.id


class TestGroupRoleAssociation(BaseTest):

    def test_table(self, cls_):
        assert cls_.__tablename__ == 'group_role_association'

    def test_columns(self, session, cls_, group, role):
        obj = cls_(group, role)
        create_time = datetime.now()
        update_time = create_time + timedelta(hours=1)
        obj.create_time = create_time
        obj.update_time = update_time

        with persist2(session, obj) as obj_id:
            stored_obj = get_stored_obj(session, cls_, obj_id)
            assert stored_obj.id == obj_id
            assert stored_obj.group_id == group.id
            assert stored_obj.role_id == role.id
            assert stored_obj.create_time == create_time
            assert stored_obj.update_time == update_time

    def test_relationships(self, session, cls_, group, role):
        obj = cls_(group, role)

        with persist2(session, obj) as obj_id:
            stored_obj = get_stored_obj(session, cls_, obj_id)
            assert stored_obj.group.id == group.id
            assert stored_obj.role.id == role.id


class TestHistoryUserShareAssociation(BaseTest):

    def test_table(self, cls_):
        assert cls_.__tablename__ == 'history_user_share_association'

    def test_columns(self, session, cls_, history, user):
        obj = cls_()
        obj.history = history
        obj.user = user

        with persist2(session, obj) as obj_id:
            stored_obj = get_stored_obj(session, cls_, obj_id)
            assert stored_obj.id == obj_id
            assert stored_obj.history_id == history.id
            assert stored_obj.user_id == user.id

    def test_relationships(self, session, cls_, history, user):
        obj = cls_()
        obj.history = history
        obj.user = user

        with persist2(session, obj) as obj_id:
            stored_obj = get_stored_obj(session, cls_, obj_id)
            assert stored_obj.history_id == history.id
            assert stored_obj.user_id == user.id

class TestHistoryAudit(BaseTest):

    def test_table(self, cls_):
        assert cls_.__tablename__ == 'history_audit'

    def test_columns_and_relationships(self, session, cls_, history):
        update_time = datetime.now()
        obj = cls_(history, update_time)

        stmt = select(cls_).where(cls_.history_id == history.id, cls_.update_time == update_time)

        with persist_no_id(session, obj, stmt):
            stored_obj = get_stored_obj(session, cls_, stmt=stmt)
            # test columns
            assert stored_obj.history_id == history.id
            assert stored_obj.update_time == update_time
            # test relationships
            assert stored_obj.history.id == history.id


class TestHistoryAnnotationAssociation(BaseTest):

    def test_table(self, cls_):
        assert cls_.__tablename__ == 'history_annotation_association'
        assert has_index(cls_.__table__, ('annotation',))

    def test_columns(self, session, cls_, history, user):
        annotation = 'a'
        obj = cls_()
        obj.user = user
        obj.history = history
        obj.annotation = annotation

        with persist2(session, obj) as obj_id:
            stored_obj = get_stored_obj(session, cls_, obj_id)
            assert stored_obj.id == obj_id
            assert stored_obj.history_id == history.id
            assert stored_obj.user_id == user.id
            assert stored_obj.annotation == annotation

    def test_relationships(self, session, cls_, history, user):
        obj = cls_()
        obj.user = user
        obj.history = history

        with persist2(session, obj) as obj_id:
            stored_obj = get_stored_obj(session, cls_, obj_id)
            assert stored_obj.history.id == history.id
            assert stored_obj.user.id == user.id


class TestHistoryDatasetAssociationAnnotationAssociation(BaseTest):

    def test_table(self, cls_):
        assert cls_.__tablename__ == 'history_dataset_association_annotation_association'
        assert has_index(cls_.__table__, ('annotation',))

    def test_columns(self, session, cls_, history_dataset_association, user):
        annotation = 'a'
        obj = cls_()
        obj.user = user
        obj.hda = history_dataset_association
        obj.annotation = annotation

        with persist2(session, obj) as obj_id:
            stored_obj = get_stored_obj(session, cls_, obj_id)
            assert stored_obj.id == obj_id
            assert stored_obj.history_dataset_association_id == history_dataset_association.id
            assert stored_obj.user_id == user.id
            assert stored_obj.annotation == annotation

    def test_relationships(self, session, cls_, history_dataset_association, user):
        obj = cls_()
        obj.user = user
        obj.hda = history_dataset_association

        with persist2(session, obj) as obj_id:
            stored_obj = get_stored_obj(session, cls_, obj_id)
            assert stored_obj.hda.id == history_dataset_association.id
            assert stored_obj.user.id == user.id


class TestHistoryDatasetAssociationRatingAssociation(BaseTest):

    def test_table(self, cls_):
        assert cls_.__tablename__ == 'history_dataset_association_rating_association'

    def test_columns(self, session, cls_, history_dataset_association, user):
        rating = 9
        obj = cls_(user, history_dataset_association, rating)

        with persist2(session, obj) as obj_id:
            stored_obj = get_stored_obj(session, cls_, obj_id)
            assert stored_obj.id == obj_id
            assert stored_obj.user_id == user.id
            assert stored_obj.rating == rating

    def test_relationships(self, session, cls_, history_dataset_association, user):
        obj = cls_(user, history_dataset_association, 1)

        with persist2(session, obj) as obj_id:
            stored_obj = get_stored_obj(session, cls_, obj_id)
            assert stored_obj.history_dataset_association.id == history_dataset_association.id
            assert stored_obj.user.id == user.id


class TestHistoryDatasetAssociationTagAssociation(BaseTest):

    def test_table(self, cls_):
        assert cls_.__tablename__ == 'history_dataset_association_tag_association'

    def test_columns(self, session, cls_, history_dataset_association, tag, user):
        user_tname, value, user_value = 'a', 'b', 'c'
        obj = cls_(user=user, tag=tag, user_tname=user_tname, value=value, user_value=user_value)
        obj.history_dataset_association = history_dataset_association

        with persist2(session, obj) as obj_id:
            stored_obj = get_stored_obj(session, cls_, obj_id)
            assert stored_obj.id == obj_id
            assert stored_obj.history_dataset_association_id == history_dataset_association.id
            assert stored_obj.tag_id == tag.id
            assert stored_obj.user_id == user.id
            assert stored_obj.user_tname == user_tname
            assert stored_obj.value == value
            assert stored_obj.user_value == user_value

    def test_relationships(self, session, cls_, history_dataset_association, tag, user):
        obj = cls_(user=user, tag=tag)
        obj.history_dataset_association = history_dataset_association

        with persist2(session, obj) as obj_id:
            stored_obj = get_stored_obj(session, cls_, obj_id)
            assert stored_obj.history_dataset_association.id == history_dataset_association.id
            assert stored_obj.tag.id == tag.id
            assert stored_obj.user.id == user.id


class TestHistoryDatasetCollectionAssociationAnnotationAssociation(BaseTest):

    def test_table(self, cls_):
        assert cls_.__tablename__ == 'history_dataset_collection_annotation_association'

    def test_columns(self, session, cls_, history_dataset_collection_association, user):
        annotation = 'a'
        obj = cls_()
        obj.user = user
        obj.history_dataset_collection = history_dataset_collection_association
        obj.annotation = annotation

        with persist2(session, obj) as obj_id:
            stored_obj = get_stored_obj(session, cls_, obj_id)
            assert stored_obj.id == obj_id
            assert stored_obj.history_dataset_collection_id == history_dataset_collection_association.id
            assert stored_obj.user_id == user.id
            assert stored_obj.annotation == annotation

    def test_relationships(self, session, cls_, history_dataset_collection_association, user):
        obj = cls_()
        obj.user = user
        obj.history_dataset_collection = history_dataset_collection_association

        with persist2(session, obj) as obj_id:
            stored_obj = get_stored_obj(session, cls_, obj_id)
            assert stored_obj.history_dataset_collection.id == history_dataset_collection_association.id
            assert stored_obj.user.id == user.id


class TestHistoryDatasetCollectionRatingAssociation(BaseTest):

    def test_table(self, cls_):
        assert cls_.__tablename__ == 'history_dataset_collection_rating_association'

    def test_columns(self, session, cls_, history_dataset_collection_association, user):
        rating = 9
        obj = cls_(user, history_dataset_collection_association, rating)

        with persist2(session, obj) as obj_id:
            stored_obj = get_stored_obj(session, cls_, obj_id)
            assert stored_obj.id == obj_id
            assert stored_obj.history_dataset_collection_id == history_dataset_collection_association.id
            assert stored_obj.user.id == user.id
            assert stored_obj.rating == rating

    def test_relationships(self, session, cls_, history_dataset_collection_association, user):
        obj = cls_(user, history_dataset_collection_association, 1)

        with persist2(session, obj) as obj_id:
            stored_obj = get_stored_obj(session, cls_, obj_id)
            assert stored_obj.dataset_collection.id == history_dataset_collection_association.id
            assert stored_obj.user.id == user.id


class TestHistoryDatasetCollectionTagAssociation(BaseTest):

    def test_table(self, cls_):
        assert cls_.__tablename__ == 'history_dataset_collection_tag_association'

    def test_columns(self, session, cls_, history_dataset_collection_association, tag, user):
        user_tname, value, user_value = 'a', 'b', 'c'
        obj = cls_(user=user, tag=tag, user_tname=user_tname, value=value, user_value=user_value)
        obj.dataset_collection = history_dataset_collection_association

        with persist2(session, obj) as obj_id:
            stored_obj = get_stored_obj(session, cls_, obj_id)
            assert stored_obj.id == obj_id
            assert stored_obj.history_dataset_collection_id == history_dataset_collection_association.id
            assert stored_obj.tag_id == tag.id
            assert stored_obj.user_id == user.id
            assert stored_obj.user_tname == user_tname
            assert stored_obj.value == value
            assert stored_obj.user_value == user_value

    def test_relationships(self, session, cls_, history_dataset_collection_association, tag, user):
        obj = cls_(user=user, tag=tag)
        obj.dataset_collection = history_dataset_collection_association

        with persist2(session, obj) as obj_id:
            stored_obj = get_stored_obj(session, cls_, obj_id)
            assert stored_obj.dataset_collection.id == history_dataset_collection_association.id
            assert stored_obj.tag.id == tag.id
            assert stored_obj.user.id == user.id

class TestHistoryRatingAssociation(BaseTest):

    def test_table(self, cls_):
        assert cls_.__tablename__ == 'history_rating_association'

    def test_columns(self, session, cls_, history, user):
        rating = 9
        obj = cls_(user, history, rating)

        with persist2(session, obj) as obj_id:
            stored_obj = get_stored_obj(session, cls_, obj_id)
            assert stored_obj.id == obj_id
            assert stored_obj.history_id == history.id
            assert stored_obj.user_id == user.id
            assert stored_obj.rating == rating

    def test_relationships(self, session, cls_, history, user):
        obj = cls_(user, history, 1)

        with persist2(session, obj) as obj_id:
            stored_obj = get_stored_obj(session, cls_, obj_id)
            assert stored_obj.history.id == history.id
            assert stored_obj.user.id == user.id


class TestHistoryTagAssociation(BaseTest):

    def test_table(self, cls_):
        assert cls_.__tablename__ == 'history_tag_association'

    def test_columns(self, session, cls_, history, tag, user):
        user_tname, value, user_value = 'a', 'b', 'c'
        obj = cls_(user=user, tag=tag, user_tname=user_tname, value=value)
        obj.user_value = user_value
        obj.history = history

        with persist2(session, obj) as obj_id:
            stored_obj = get_stored_obj(session, cls_, obj_id)
            assert stored_obj.id == obj_id
            assert stored_obj.history_id == history.id
            assert stored_obj.tag_id == tag.id
            assert stored_obj.user_id == user.id
            assert stored_obj.user_tname == user_tname
            assert stored_obj.value == value
            assert stored_obj.user_value == user_value

    def test_relationships(self, session, cls_, history, tag, user):
        obj = cls_(user=user, tag=tag)
        obj.history = history

        with persist2(session, obj) as obj_id:
            stored_obj = get_stored_obj(session, cls_, obj_id)
            assert stored_obj.history.id == history.id
            assert stored_obj.tag.id == tag.id
            assert stored_obj.user.id == user.id


class TestJobMetricNumeric(BaseTest):

    def test_table(self, cls_):
        assert cls_.__tablename__ == 'job_metric_numeric'

    def test_columns(self, session, cls_, job):
        plugin, metric_name, metric_value = 'a', 'b', 9
        obj = cls_(plugin, metric_name, metric_value)
        obj.job = job

        with persist2(session, obj) as obj_id:
            stored_obj = get_stored_obj(session, cls_, obj_id)
            assert stored_obj.id == obj_id
            assert stored_obj.job_id == job.id
            assert stored_obj.plugin == plugin
            assert stored_obj.metric_value == metric_value

    def test_relationships(self, session, cls_, job):
        obj = cls_(None, None, None)
        obj.job = job

        with persist2(session, obj) as obj_id:
            stored_obj = get_stored_obj(session, cls_, obj_id)
            assert stored_obj.job.id == job.id


class TestJobMetricText(BaseTest):

    def test_table(self, cls_):
        assert cls_.__tablename__ == 'job_metric_text'

    def test_columns(self, session, cls_, job):
        plugin, metric_name, metric_value = 'a', 'b', 'c'
        obj = cls_(plugin, metric_name, metric_value)
        obj.job = job

        with persist2(session, obj) as obj_id:
            stored_obj = get_stored_obj(session, cls_, obj_id)
            assert stored_obj.id == obj_id
            assert stored_obj.job_id == job.id
            assert stored_obj.plugin == plugin
            assert stored_obj.metric_value == metric_value

    def test_relationships(self, session, cls_, job):
        obj = cls_(None, None, None)
        obj.job = job

        with persist2(session, obj) as obj_id:
            stored_obj = get_stored_obj(session, cls_, obj_id)
            assert stored_obj.job.id == job.id


class TestJobParameter(BaseTest):

    def test_table(self, cls_):
        assert cls_.__tablename__ == 'job_parameter'

    def test_columns(self, session, cls_, job):
        name, value = 'a', 'b'
        obj = cls_(name, value)
        obj.job_id = job.id

        with persist2(session, obj) as obj_id:
            stored_obj = get_stored_obj(session, cls_, obj_id)
            assert stored_obj.id == obj_id
            assert stored_obj.job_id == job.id
            assert stored_obj.name == name
            assert stored_obj.value == value


class TestJobStateHistory(BaseTest):

    def test_table(self, cls_):
        assert cls_.__tablename__ == 'job_state_history'

    def test_columns(self, session, cls_, job):
        state, info = job.state, job.info
        create_time = datetime.now()
        update_time = create_time + timedelta(hours=1)
        obj = cls_(job)
        obj.create_time = create_time
        obj.update_time = update_time

        with persist2(session, obj) as obj_id:
            stored_obj = get_stored_obj(session, cls_, obj_id)
            assert stored_obj.id == obj_id
            assert stored_obj.create_time == create_time
            assert stored_obj.update_time == update_time
            assert stored_obj.job_id == job.id
            assert stored_obj.state == state
            assert stored_obj.info == info

    def test_relationships(self, session, cls_, job):
        obj = cls_(job)

        with persist2(session, obj) as obj_id:
            stored_obj = get_stored_obj(session, cls_, obj_id)
        assert stored_obj.job.id == job.id


class TestJobToImplicitOutputDatasetCollectionAssociation(BaseTest):

    def test_table(self, cls_):
        assert cls_.__tablename__ == 'job_to_implicit_output_dataset_collection'

    def test_columns(self, session, cls_, dataset_collection, job):
        name = 'a'
        obj = cls_(name, dataset_collection)
        obj.job = job

        with persist2(session, obj) as obj_id:
            stored_obj = get_stored_obj(session, cls_, obj_id)
            assert stored_obj.id == obj_id
            assert stored_obj.job_id == job.id
            assert stored_obj.dataset_collection_id == dataset_collection.id
            assert stored_obj.name == name

    def test_relationships(self, session, cls_, dataset_collection, job):
        obj = cls_(None, dataset_collection)
        obj.job = job

        with persist2(session, obj) as obj_id:
            stored_obj = get_stored_obj(session, cls_, obj_id)
            assert stored_obj.job.id == job.id
            assert stored_obj.dataset_collection.id == dataset_collection.id

            
class TestJobToInputDatasetCollectionAssociation(BaseTest):

    def test_table(self, cls_):
        assert cls_.__tablename__ == 'job_to_input_dataset_collection'

    def test_columns(self, session, cls_, history_dataset_collection_association, job):
        name = 'a'
        obj = cls_(name, history_dataset_collection_association)
        obj.job = job

        with persist2(session, obj) as obj_id:
            stored_obj = get_stored_obj(session, cls_, obj_id)
            assert stored_obj.id == obj_id
            assert stored_obj.job_id == job.id
            assert stored_obj.dataset_collection_id == history_dataset_collection_association.id
            assert stored_obj.name == name

    def test_relationships(self, session, cls_, history_dataset_collection_association, job):
        obj = cls_(None, history_dataset_collection_association)
        obj.job = job

        with persist2(session, obj) as obj_id:
            stored_obj = get_stored_obj(session, cls_, obj_id)
            assert stored_obj.job.id == job.id
            assert stored_obj.dataset_collection.id == history_dataset_collection_association.id


class TestJobToInputDatasetCollectionElementAssociation(BaseTest):

    def test_table(self, cls_):
        assert cls_.__tablename__ == 'job_to_input_dataset_collection_element'

    def test_columns(self, session, cls_, dataset_collection_element, job):
        name = 'a'
        obj = cls_(name, dataset_collection_element)
        obj.job = job

        with persist2(session, obj) as obj_id:
            stored_obj = get_stored_obj(session, cls_, obj_id)
            assert stored_obj.id == obj_id
            assert stored_obj.job_id == job.id
            assert stored_obj.dataset_collection_element_id == dataset_collection_element.id
            assert stored_obj.name == name

    def test_relationships(self, session, cls_, dataset_collection_element, job):
        obj = cls_(None, dataset_collection_element)
        obj.job = job

        with persist2(session, obj) as obj_id:
            stored_obj = get_stored_obj(session, cls_, obj_id)
            assert stored_obj.job.id == job.id
            assert stored_obj.dataset_collection_element.id == dataset_collection_element.id


class TestJobToInputDatasetAssociation(BaseTest):

    def test_table(self, cls_):
        assert cls_.__tablename__ == 'job_to_input_dataset'

    def test_columns(self, session, cls_, history_dataset_association, job):
        name, dataset_version = 'a', 9
        obj = cls_(name, history_dataset_association)
        obj.job = job
        obj.dataset_version = dataset_version

        with persist2(session, obj) as obj_id:
            stored_obj = get_stored_obj(session, cls_, obj_id)
            assert stored_obj.id == obj_id
            assert stored_obj.job_id == job.id
            assert stored_obj.dataset_id == history_dataset_association.id
            assert stored_obj.dataset_version == dataset_version
            assert stored_obj.name == name

    def test_relationships(self, session, cls_, history_dataset_association, job):
        obj = cls_(None, history_dataset_association)
        obj.job = job

        with persist2(session, obj) as obj_id:
            stored_obj = get_stored_obj(session, cls_, obj_id)
            assert stored_obj.job.id == job.id
            assert stored_obj.dataset.id == history_dataset_association.id


class TestJobToInputLibraryDatasetAssociation(BaseTest):

    def test_table(self, cls_):
        assert cls_.__tablename__ == 'job_to_input_library_dataset'

    def test_columns(self, session, cls_, library_dataset_dataset_association, job):
        name = 'a'
        obj = cls_(name, library_dataset_dataset_association)
        obj.job = job

        with persist2(session, obj) as obj_id:
            stored_obj = get_stored_obj(session, cls_, obj_id)
            assert stored_obj.id == obj_id
            assert stored_obj.job_id == job.id
            assert stored_obj.ldda_id == library_dataset_dataset_association.id
            assert stored_obj.name == name

    def test_relationships(self, session, cls_, library_dataset_dataset_association, job):
        obj = cls_(None, library_dataset_dataset_association)
        obj.job = job

        with persist2(session, obj) as obj_id:
            stored_obj = get_stored_obj(session, cls_, obj_id)
            assert stored_obj.job.id == job.id
            assert stored_obj.dataset.id == library_dataset_dataset_association.id


class TestJobToOutputDatasetAssociation(BaseTest):

    def test_table(self, cls_):
        assert cls_.__tablename__ == 'job_to_output_dataset'

    def test_columns(self, session, cls_, history_dataset_association, job):
        name = 'a'
        obj = cls_(name, history_dataset_association)
        obj.job = job

        with persist2(session, obj) as obj_id:
            stored_obj = get_stored_obj(session, cls_, obj_id)
            assert stored_obj.id == obj_id
            assert stored_obj.job_id == job.id
            assert stored_obj.dataset_id == history_dataset_association.id
            assert stored_obj.name == name

    def test_relationships(self, session, cls_, history_dataset_association, job):
        obj = cls_(None, history_dataset_association)
        obj.job = job

        with persist2(session, obj) as obj_id:
            stored_obj = get_stored_obj(session, cls_, obj_id)
            assert stored_obj.job.id == job.id
            assert stored_obj.dataset.id == history_dataset_association.id


class TestJobToOutputDatasetCollectionAssociation(BaseTest):

    def test_table(self, cls_):
        assert cls_.__tablename__ == 'job_to_output_dataset_collection'

    def test_columns(self, session, cls_, history_dataset_collection_association, job):
        name = 'a'
        obj = cls_(name, history_dataset_collection_association)
        obj.job = job

        with persist2(session, obj) as obj_id:
            stored_obj = get_stored_obj(session, cls_, obj_id)
            assert stored_obj.id == obj_id
            assert stored_obj.job_id == job.id
            assert stored_obj.dataset_collection_id == history_dataset_collection_association.id
            assert stored_obj.name == name

    def test_relationships(self, session, cls_, history_dataset_collection_association, job):
        obj = cls_(None, history_dataset_collection_association)
        obj.job = job

        with persist2(session, obj) as obj_id:
            stored_obj = get_stored_obj(session, cls_, obj_id)
            assert stored_obj.job.id == job.id
            assert stored_obj.dataset_collection_instance.id == history_dataset_collection_association.id


#TODO
#class TestLibraryDataset(BaseTest):
#
#    def test_table(self, cls_, model):
#        assert cls_.__tablename__ == 'library_dataset'
#
#    def test_columns(
#            self, cls_, model, session, library_dataset_dataset_association, library_folder):
#        with dbcleanup(session, cls_):
#            folder = library_folder
#            order_id = 9
#            create_time = datetime.now()
#            update_time = create_time + timedelta(hours=1)
#            name = 'a'
#            info = 'b'
#            deleted = False
#            purged = False
#
#            obj = cls_()
#            obj.folder = folder
#            obj.order_id = order_id
#            obj.create_time = create_time
#            obj.update_time = update_time
#            obj.name = name
#            obj.info = info
#            obj.deleted = deleted
#            obj.purged = purged
#            obj_id = persist(session, obj)
#
#            stored_obj = get_stored_obj(session, cls_, obj_id)
#            assert stored_obj.id == obj_id
#            assert stored_obj.folder_id == folder.id
#            assert stored_obj.order_id == order_id
#            assert stored_obj.create_time == create_time
#            assert stored_obj.update_time == update_time
#            assert stored_obj.name == name
#            assert stored_obj.info == info
#            assert stored_obj.deleted == deleted
#            assert stored_obj.purged == purged
#
#    def test_relationships(self, cls_, model, session, library_dataset_dataset_association,
#            library_folder, library_dataset_permission):
#        with dbcleanup(session, cls_):
#            folder = library_folder
#            obj = cls_()
#            obj.library_dataset_dataset_association = library_dataset_dataset_association
#            obj.folder = folder
#
#            ldda = model.LibraryDatasetDatasetAssociation()
#            ldda.library_dataset = obj
#            persist(session, ldda)
#
#            obj.actions.append(library_dataset_permission)
#            obj_id = persist(session, obj)
#
#            stored_obj = get_stored_obj(session, cls_, obj_id)
#            assert stored_obj.library_dataset_dataset_association.id == library_dataset_dataset_association.id
#            assert stored_obj.folder.id == folder.id
#            assert stored_obj.expired_datasets[0].id == ldda.id
#            assert stored_obj.actions == [library_dataset_permission]


class TestJobToOutputLibraryDatasetAssociation(BaseTest):

    def test_table(self, cls_):
        assert cls_.__tablename__ == 'job_to_output_library_dataset'

    def test_columns(self, session, cls_, library_dataset_dataset_association, job):
        name = 'a'
        obj = cls_(name, library_dataset_dataset_association)
        obj.job = job

        with persist2(session, obj) as obj_id:
            stored_obj = get_stored_obj(session, cls_, obj_id)
            assert stored_obj.id == obj_id
            assert stored_obj.job_id == job.id
            assert stored_obj.ldda_id == library_dataset_dataset_association.id
            assert stored_obj.name == name

    def test_relationships(self, session, cls_, library_dataset_dataset_association, job):
        obj = cls_(None, library_dataset_dataset_association)
        obj.job = job

        with persist2(session, obj) as obj_id:
            stored_obj = get_stored_obj(session, cls_, obj_id)
            assert stored_obj.job.id == job.id
            assert stored_obj.dataset.id == library_dataset_dataset_association.id


class TestLibrary(BaseTest):

    def test_table(self, cls_):
        assert cls_.__tablename__ == 'library'

    def test_columns(self, session, cls_, library_folder):
        name, deleted, purged, description, synopsis = 'a', True, True, 'b', 'c'
        create_time = datetime.now()
        update_time = create_time + timedelta(hours=1)
        obj = cls_(name, description, synopsis, library_folder)
        obj.create_time = create_time
        obj.update_time = update_time
        obj.deleted = deleted
        obj.purged = purged

        with persist2(session, obj) as obj_id:
            stored_obj = get_stored_obj(session, cls_, obj_id)
            assert stored_obj.id == obj_id
            assert stored_obj.root_folder_id == library_folder.id
            assert stored_obj.create_time == create_time
            assert stored_obj.update_time == update_time
            assert stored_obj.name == name
            assert stored_obj.deleted == deleted
            assert stored_obj.purged == purged
            assert stored_obj.description == description
            assert stored_obj.synopsis == synopsis

    def test_relationships(self, session, cls_, library_folder, library_permission):
        obj = cls_(None, None, None, library_folder)
        obj.actions.append(library_permission)

        with persist2(session, obj) as obj_id:
            stored_obj = get_stored_obj(session, cls_, obj_id)
            assert stored_obj.root_folder.id == library_folder.id
            assert stored_obj.actions == [library_permission]


class TestLibraryDatasetCollectionAnnotationAssociation(BaseTest):

    def test_table(self, cls_):
        assert cls_.__tablename__ == 'library_dataset_collection_annotation_association'

    def test_columns(self, session, cls_, library_dataset_collection_association, user):
        annotation = 'a'
        obj = cls_()
        obj.user = user
        obj.dataset_collection = library_dataset_collection_association
        obj.annotation = annotation

        with persist2(session, obj) as obj_id:
            stored_obj = get_stored_obj(session, cls_, obj_id)
            assert stored_obj.id == obj_id
            assert stored_obj.library_dataset_collection_id == library_dataset_collection_association.id
            assert stored_obj.user_id == user.id
            assert stored_obj.annotation == annotation

    def test_relationships(self, session, cls_, library_dataset_collection_association, user):
        obj = cls_()
        obj.user = user
        obj.dataset_collection = library_dataset_collection_association

        with persist2(session, obj) as obj_id:
            stored_obj = get_stored_obj(session, cls_, obj_id)
            assert stored_obj.dataset_collection.id == library_dataset_collection_association.id
            assert stored_obj.user.id == user.id


class TestLibraryDatasetCollectionTagAssociation(BaseTest):

    def test_table(self, cls_):
        assert cls_.__tablename__ == 'library_dataset_collection_tag_association'

    def test_columns(self, session, cls_, library_dataset_collection_association, tag, user):
        user_tname, value, user_value = 'a', 'b', 'c'
        obj = cls_(user=user, tag=tag, user_tname=user_tname, value=value)
        obj.user_value = user_value
        obj.dataset_collection = library_dataset_collection_association

        with persist2(session, obj) as obj_id:
            stored_obj = get_stored_obj(session, cls_, obj_id)
            assert stored_obj.id == obj_id
            assert stored_obj.library_dataset_collection_id == library_dataset_collection_association.id
            assert stored_obj.tag_id == tag.id
            assert stored_obj.user_id == user.id
            assert stored_obj.user_tname == user_tname
            assert stored_obj.value == value
            assert stored_obj.user_value == user_value

    def test_relationships(self, session, cls_, library_dataset_collection_association, tag, user):
        obj = cls_(user=user, tag=tag)
        obj.dataset_collection = library_dataset_collection_association

        with persist2(session, obj) as obj_id:
            stored_obj = get_stored_obj(session, cls_, obj_id)
            assert stored_obj.dataset_collection.id == library_dataset_collection_association.id
            assert stored_obj.tag.id == tag.id
            assert stored_obj.user.id == user.id


class TestLibraryDatasetCollectionRatingAssociation(BaseTest):

    def test_table(self, cls_):
        assert cls_.__tablename__ == 'library_dataset_collection_rating_association'

    def test_columns(self, session, cls_, library_dataset_collection_association, user):
        rating = 9
        obj = cls_(user, library_dataset_collection_association, rating)

        with persist2(session, obj) as obj_id:
            stored_obj = get_stored_obj(session, cls_, obj_id)
            assert stored_obj.id == obj_id
            assert stored_obj.library_dataset_collection_id == library_dataset_collection_association.id
            assert stored_obj.user_id == user.id
            assert stored_obj.rating == rating

    def test_relationships(self, session, cls_, library_dataset_collection_association, user):
        obj = cls_(user, library_dataset_collection_association, 1)

        with persist2(session, obj) as obj_id:
            stored_obj = get_stored_obj(session, cls_, obj_id)
            assert stored_obj.dataset_collection.id == library_dataset_collection_association.id
            assert stored_obj.user.id == user.id


class TestLibraryDatasetDatasetAssociationPermissions(BaseTest):

    def test_table(self, cls_):
        assert cls_.__tablename__ == 'library_dataset_dataset_association_permissions'

    def test_columns(self, session, cls_, library_dataset_dataset_association, role):
        action = 'a'
        create_time = datetime.now()
        update_time = create_time + timedelta(hours=1)
        obj = cls_(action, library_dataset_dataset_association, role)
        obj.create_time = create_time
        obj.update_time = update_time

        with persist2(session, obj) as obj_id:
            stored_obj = get_stored_obj(session, cls_, obj_id)
            assert stored_obj.id == obj_id
            assert stored_obj.create_time == create_time
            assert stored_obj.update_time == update_time
            assert stored_obj.action == action
            assert stored_obj.library_dataset_dataset_association_id == library_dataset_dataset_association.id
            assert stored_obj.role_id == role.id

    def test_relationships(self, session, cls_, library_dataset_dataset_association, role):
        obj = cls_(None, library_dataset_dataset_association, role)

        with persist2(session, obj) as obj_id:
            stored_obj = get_stored_obj(session, cls_, obj_id)
            assert stored_obj.library_dataset_dataset_association.id == library_dataset_dataset_association.id
            assert stored_obj.role.id == role.id


class TestLibraryDatasetDatasetAssociationTagAssociation(BaseTest):

    def test_table(self, cls_):
        assert cls_.__tablename__ == 'library_dataset_dataset_association_tag_association'

    def test_columns(self, session, cls_, library_dataset_dataset_association, tag, user):
        user_tname, value, user_value = 'a', 'b', 'c'
        obj = cls_(user=user, tag=tag, user_tname=user_tname, value=value)
        obj.user_value = user_value
        obj.library_dataset_dataset_association = library_dataset_dataset_association

        with persist2(session, obj) as obj_id:
            stored_obj = get_stored_obj(session, cls_, obj_id)
            assert stored_obj.id == obj_id
            assert stored_obj.library_dataset_dataset_association_id == library_dataset_dataset_association.id
            assert stored_obj.tag_id == tag.id
            assert stored_obj.user_id == user.id
            assert stored_obj.user_tname == user_tname
            assert stored_obj.value == value
            assert stored_obj.user_value == user_value

    def test_relationships(self, session, cls_, library_dataset_dataset_association, tag, user):
        obj = cls_(user=user, tag=tag)
        obj.library_dataset_dataset_association = library_dataset_dataset_association

        with persist2(session, obj) as obj_id:
            stored_obj = get_stored_obj(session, cls_, obj_id)
            assert stored_obj.library_dataset_dataset_association.id == library_dataset_dataset_association.id
            assert stored_obj.tag.id == tag.id
            assert stored_obj.user.id == user.id


class TestLibraryDatasetPermissions(BaseTest):

    def test_table(self, cls_):
        assert cls_.__tablename__ == 'library_dataset_permissions'

    def test_columns(self, session, cls_, library_dataset, role):
        action = 'a'
        create_time = datetime.now()
        update_time = create_time + timedelta(hours=1)
        obj = cls_(action, library_dataset, role)
        obj.create_time = create_time
        obj.update_time = update_time

        with persist2(session, obj) as obj_id:
            stored_obj = get_stored_obj(session, cls_, obj_id)
            assert stored_obj.id == obj_id
            assert stored_obj.create_time == create_time
            assert stored_obj.update_time == update_time
            assert stored_obj.action == action
            assert stored_obj.library_dataset_id == library_dataset.id
            assert stored_obj.role_id == role.id

    def test_relationships(self, session, cls_, library_dataset, role):
        obj = cls_(None, library_dataset, role)

        with persist2(session, obj) as obj_id:
            stored_obj = get_stored_obj(session, cls_, obj_id)
            assert stored_obj.library_dataset.id == library_dataset.id
            assert stored_obj.role.id == role.id

# TODO
#class TestLibraryFolder(BaseTest):
#
#    def test_table(self, cls_, model):
#        assert cls_.__tablename__ == 'library_folder'
#        assert has_index(cls_.__table__, ('name',))
#
#    def test_columns(self, cls_, model, session, library_folder):
#        with dbcleanup(session, cls_):
#            parent = library_folder
#            create_time = datetime.now()
#            update_time = create_time + timedelta(hours=1)
#            name = 'a'
#            description = 'b'
#            order_id = 9
#            item_count = 1
#            deleted = False
#            purged = False
#            genome_build = 'c'
#
#            obj = cls_()
#            obj.parent = parent
#            obj.create_time = create_time
#            obj.update_time = update_time
#            obj.name = name
#            obj.description = description
#            obj.order_id = order_id
#            obj.item_count = item_count
#            obj.deleted = deleted
#            obj.purged = purged
#            obj.genome_build = genome_build
#            obj_id = persist(session, obj)
#
#            stored_obj = get_stored_obj(session, cls_, obj_id)
#            assert stored_obj.id == obj_id
#            assert stored_obj.parent_id == parent.id
#            assert stored_obj.create_time == create_time
#            assert stored_obj.update_time == update_time
#            assert stored_obj.name == name
#            assert stored_obj.description == description
#            assert stored_obj.order_id == order_id
#            assert stored_obj.item_count == item_count
#            assert stored_obj.deleted == deleted
#            assert stored_obj.purged == purged
#            assert stored_obj.genome_build == genome_build
#
#    def test_relationships(
#            self, cls_, model, session, library_folder, library_dataset, library, library_folder_permission):
#        with dbcleanup(session, cls_):
#            folder1 = model.LibraryFolder()
#
#            obj = cls_()
#            # no back reference, so dataset does not update folder; so we have to flush to the db
#            # todo: ..but why is there no back reference?
#            library_dataset.folder = obj
#            persist(session, library_dataset)
#
#            obj.parent = library_folder
#            obj.folders.append(folder1)
#            obj.library_root.append(library)
#            obj.actions.append(library_folder_permission)
#            obj_id = persist(session, obj)
#
#            stored_obj = get_stored_obj(session, cls_, obj_id)
#            assert stored_obj.parent.id == library_folder.id
#            assert stored_obj.folders == [folder1]
#            assert stored_obj.active_folders == [folder1]
#            assert stored_obj.library_root == [library]
#            assert stored_obj.actions == [library_folder_permission]
#            # use identity equality instread of object equality.
#            assert stored_obj.datasets[0].id == library_dataset.id
#            assert stored_obj.active_datasets[0].id == library_dataset.id
#

class TestLibraryFolderPermissions(BaseTest):

    def test_table(self, cls_):
        assert cls_.__tablename__ == 'library_folder_permissions'

    def test_columns(self, session, cls_, library_folder, role):
        action = 'a'
        obj = cls_(action, library_folder, role)
        create_time = datetime.now()
        update_time = create_time + timedelta(hours=1)
        obj.create_time = create_time
        obj.update_time = update_time

        with persist2(session, obj) as obj_id:
            stored_obj = get_stored_obj(session, cls_, obj_id)
            assert stored_obj.id == obj_id
            assert stored_obj.create_time == create_time
            assert stored_obj.update_time == update_time
            assert stored_obj.action == action
            assert stored_obj.library_folder_id == library_folder.id
            assert stored_obj.role_id == role.id

    def test_relationships(self, session, cls_, library_folder, role):
        obj = cls_(None, library_folder, role)

        with persist2(session, obj) as obj_id:
            stored_obj = get_stored_obj(session, cls_, obj_id)
            assert stored_obj.folder.id == library_folder.id
            assert stored_obj.role.id == role.id


class TestLibraryPermissions(BaseTest):

    def test_table(self, cls_):
        assert cls_.__tablename__ == 'library_permissions'

    def test_columns(self, session, cls_, library, role):
        action = 'a'
        obj = cls_(action, library, role)
        create_time = datetime.now()
        update_time = create_time + timedelta(hours=1)
        obj = cls_(action, library, role)
        obj.create_time = create_time
        obj.update_time = update_time

        with persist2(session, obj) as obj_id:
            stored_obj = get_stored_obj(session, cls_, obj_id)
            assert stored_obj.id == obj_id
            assert stored_obj.create_time == create_time
            assert stored_obj.update_time == update_time
            assert stored_obj.action == action
            assert stored_obj.library_id == library.id
            assert stored_obj.role_id == role.id

    def test_relationships(self, session, cls_, library, role):
        obj = cls_(None, library, role)

        with persist2(session, obj) as obj_id:
            stored_obj = get_stored_obj(session, cls_, obj_id)
            assert stored_obj.library.id == library.id
            assert stored_obj.role.id == role.id


class TestPage(BaseTest):

    def test_table(self, cls_):
        assert cls_.__tablename__ == 'page'
        assert has_index(cls_.__table__, ('slug',))

    def test_columns(self, session, cls_, user, page_revision):
        title, deleted, importable, slug, published = 'a', True, True, 'b', True
        create_time = datetime.now()
        update_time = create_time + timedelta(hours=1)
        obj = cls_()
        obj.user = user
        obj.title = title
        obj.deleted = deleted
        obj.importable = importable
        obj.slug = slug
        obj.published = published
        obj.create_time = create_time
        obj.update_time = update_time
        # This is OK for this test; however, page_revision.page != obj. Can we do better?
        obj.latest_revision = page_revision

        with persist2(session, obj) as obj_id:
            stored_obj = get_stored_obj(session, cls_, obj_id)
            assert stored_obj.id == obj_id
            assert stored_obj.create_time == create_time
            assert stored_obj.update_time == update_time
            assert stored_obj.user_id == user.id
            assert stored_obj.latest_revision_id == page_revision.id
            assert stored_obj.title == title
            assert stored_obj.deleted == deleted
            assert stored_obj.importable == importable
            assert stored_obj.slug == slug
            assert stored_obj.published == published

    def test_relationships(
        self,
        session,
        cls_,
        user,
        page_revision,
        page_tag_association,
        page_annotation_association,
        page_rating_association,
        page_user_share_association,
    ):
        obj = cls_()
        obj.user = user
        # This is OK for this test; however, page_revision.page != obj. Can we do better?
        obj.latest_revision = page_revision
        obj.revisions.append(page_revision)
        obj.tags.append(page_tag_association)
        obj.annotations.append(page_annotation_association)
        obj.ratings.append(page_rating_association)
        obj.users_shared_with.append(page_user_share_association)

        with persist2(session, obj) as obj_id:
            stored_obj = get_stored_obj(session, cls_, obj_id)
            assert stored_obj.user.id == user.id
            assert stored_obj.revisions == [page_revision]
            assert stored_obj.latest_revision.id == page_revision.id
            assert stored_obj.tags == [page_tag_association]
            assert stored_obj.annotations == [page_annotation_association]
            assert stored_obj.ratings == [page_rating_association]
            assert stored_obj.users_shared_with == [page_user_share_association]
            # This doesn't test the average amount, just the mapping.
            assert stored_obj.average_rating == page_rating_association.rating


#class Test(BaseTest):
#
#    def test_table(self, cls_):
#        assert cls_.__tablename__ == ''
#
#    def test_columns(self, session, cls_):
#        obj = cls_()
#
#        with persist2(session, obj) as obj_id:
#            stored_obj = get_stored_obj(session, cls_, obj_id)
#            assert stored_obj.id == obj_id
#
#    def test_relationships(self, session, cls_):
#        obj = cls_()
#
#        with persist2(session, obj) as obj_id:
#            stored_obj = get_stored_obj(session, cls_, obj_id)
# TODO: this is an inconsistent name. Why?
def test_Page_average_rating(model, session, page, user):
    cls = model.PageRatingAssociation
    with dbcleanup(session, cls):
        # Page has been expunged; to access its deferred properties,
        # it needs to be added back to the session.
        session.add(page)
        assert page.average_rating is None  # With no ratings, we expect None.
        # Create ratings
        for rating in (1, 2, 3, 4, 5):
            r = cls(user, page)
            r.rating = rating
            persist(session, r)
        assert page.average_rating == 3.0  # Expect average after ratings added.


class TestPageAnnotationAssociation(BaseTest):

    def test_table(self, cls_):
        assert cls_.__tablename__ == 'page_annotation_association'
        assert has_index(cls_.__table__, ('annotation',))

    def test_columns(self, session, cls_, page, user):
        annotation = 'a'
        obj = cls_()
        obj.user = user
        obj.page = page
        obj.annotation = annotation

        with persist2(session, obj) as obj_id:
            stored_obj = get_stored_obj(session, cls_, obj_id)
            assert stored_obj.id == obj_id
            assert stored_obj.page_id == page.id
            assert stored_obj.user_id == user.id
            assert stored_obj.annotation == annotation

    def test_relationships(self, session, cls_, page, user):
        obj = cls_()
        obj.user = user
        obj.page = page

        with persist2(session, obj) as obj_id:
            stored_obj = get_stored_obj(session, cls_, obj_id)
            assert stored_obj.page.id == page.id
            assert stored_obj.user.id == user.id


class TestPageRatingAssociation(BaseTest):

    def test_table(self, cls_):
        assert cls_.__tablename__ == 'page_rating_association'

    def test_columns(self, session, cls_, page, user):
        rating = 9
        obj = cls_(user, page, rating)

        with persist2(session, obj) as obj_id:
            stored_obj = get_stored_obj(session, cls_, obj_id)
            assert stored_obj.id == obj_id
            assert stored_obj.page_id == page.id
            assert stored_obj.user_id == user.id
            assert stored_obj.rating == rating

    def test_relationships(self, session, cls_, page, user):
        obj = cls_(user, page, 1)

        with persist2(session, obj) as obj_id:
            stored_obj = get_stored_obj(session, cls_, obj_id)
            assert stored_obj.page.id == page.id
            assert stored_obj.user.id == user.id


class TestPageRevision(BaseTest):

    def test_table(self, cls_):
        assert cls_.__tablename__ == 'page_revision'

    def test_columns(self, session, cls_, model, page):
        title, content = 'a', 'b'
        create_time = datetime.now()
        update_time = create_time + timedelta(hours=1)
        obj = cls_()
        obj.page = page
        obj.create_time = create_time
        obj.update_time = update_time
        obj.title = title
        obj.content = content

        with persist2(session, obj) as obj_id:
            stored_obj = get_stored_obj(session, cls_, obj_id)
            assert stored_obj.id == obj_id
            assert stored_obj.create_time == create_time
            assert stored_obj.update_time == update_time
            assert stored_obj.page_id == page.id
            assert stored_obj.title == title
            assert stored_obj.content == content
            assert stored_obj.content_format == model.PageRevision.DEFAULT_CONTENT_FORMAT

    def test_relationships(self, session, cls_, page):
        obj = cls_()
        obj.page = page

        with persist2(session, obj) as obj_id:
            stored_obj = get_stored_obj(session, cls_, obj_id)
            assert stored_obj.page.id == page.id


class TestPageTagAssociation(BaseTest):

    def test_table(self, cls_):
        assert cls_.__tablename__ == 'page_tag_association'

    def test_columns(self, session, cls_, page, tag, user):
        user_tname, value, user_value = 'a', 'b', 'c'
        obj = cls_(user=user, tag=tag, user_tname=user_tname, value=value)
        obj.user_value = user_value
        obj.page = page

        with persist2(session, obj) as obj_id:
            stored_obj = get_stored_obj(session, cls_, obj_id)
            assert stored_obj.id == obj_id
            assert stored_obj.page_id == page.id
            assert stored_obj.tag_id == tag.id
            assert stored_obj.user_id == user.id
            assert stored_obj.user_tname == user_tname
            assert stored_obj.value == value
            assert stored_obj.user_value == user_value

    def test_relationships(self, session, cls_, page, tag, user):
        obj = cls_(user=user, tag=tag)
        obj.page = page

        with persist2(session, obj) as obj_id:
            stored_obj = get_stored_obj(session, cls_, obj_id)
            assert stored_obj.page.id == page.id
            assert stored_obj.tag.id == tag.id
            assert stored_obj.user.id == user.id


class TestPageUserShareAssociation(BaseTest):

    def test_table(self, cls_):
        assert cls_.__tablename__ == 'page_user_share_association'

    def test_columns(self, session, cls_, page, user):
        obj = cls_()
        obj.page = page
        obj.user = user

        with persist2(session, obj) as obj_id:
            stored_obj = get_stored_obj(session, cls_, obj_id)
            assert stored_obj.id == obj_id
            assert stored_obj.page_id == page.id
            assert stored_obj.user_id == user.id

    def test_relationships(self, session, cls_, page, user):
        obj = cls_()
        obj.page = page
        obj.user = user

        with persist2(session, obj) as obj_id:
            stored_obj = get_stored_obj(session, cls_, obj_id)
            assert stored_obj.page.id == page.id
            assert stored_obj.user.id == user.id


#class Test(BaseTest):
#
#    def test_table(self, cls_):
#        assert cls_.__tablename__ == ''
#
#    def test_columns(self, session, cls_):
#        obj = cls_()
#
#        with persist2(session, obj) as obj_id:
#            stored_obj = get_stored_obj(session, cls_, obj_id)
#            assert stored_obj.id == obj_id
#
#    def test_relationships(self, session, cls_):
#        obj = cls_()
#
#        with persist2(session, obj) as obj_id:
#            stored_obj = get_stored_obj(session, cls_, obj_id)


def test_PasswordResetToken(model, session, user):
    cls = model.PasswordResetToken
    assert cls.__tablename__ == 'password_reset_token'
    with dbcleanup(session, cls):
        token = get_random_string()
        expiration_time = datetime.now()
        obj = cls(user, token)
        obj.expiration_time = expiration_time
        persist(session, obj, return_id=False)

        stmt = select(cls).where(cls.token == token)
        stored_obj = get_stored_obj(session, cls, stmt=stmt)
        # test mapped columns
        assert stored_obj.token == token
        assert stored_obj.expiration_time == expiration_time
        # test mapped relationships
        assert stored_obj.user.id == user.id


#class Test(BaseTest):
#
#    def test_table(self, cls_):
#        assert cls_.__tablename__ == ''
#
#    def test_columns(self, session, cls_):
#        obj = cls_()
#
#        with persist2(session, obj) as obj_id:
#            stored_obj = get_stored_obj(session, cls_, obj_id)
#            assert stored_obj.id == obj_id
#
#    def test_relationships(self, session, cls_):
#        obj = cls_()
#
#        with persist2(session, obj) as obj_id:
#            stored_obj = get_stored_obj(session, cls_, obj_id)


def test_PSAAssociation(model, session):
    cls = model.PSAAssociation
    assert cls.__tablename__ == 'psa_association'
    with dbcleanup(session, cls):
        server_url, handle, secret, issued, lifetime, assoc_type = 'a', 'b', 'c', 1, 2, 'd'
        obj = cls(server_url, handle, secret, issued, lifetime, assoc_type)
        obj_id = persist(session, obj)

        stored_obj = get_stored_obj(session, cls, obj_id)
        # test mapped columns
        assert stored_obj.id == obj_id
        assert stored_obj.server_url == server_url
        assert stored_obj.handle == handle
        assert stored_obj.secret == secret
        assert stored_obj.issued == issued
        assert stored_obj.lifetime == lifetime
        assert stored_obj.assoc_type == assoc_type


#class Test(BaseTest):
#
#    def test_table(self, cls_):
#        assert cls_.__tablename__ == ''
#
#    def test_columns(self, session, cls_):
#        obj = cls_()
#
#        with persist2(session, obj) as obj_id:
#            stored_obj = get_stored_obj(session, cls_, obj_id)
#            assert stored_obj.id == obj_id
#
#    def test_relationships(self, session, cls_):
#        obj = cls_()
#
#        with persist2(session, obj) as obj_id:
#            stored_obj = get_stored_obj(session, cls_, obj_id)


def test_PSACode(model, session):
    cls = model.PSACode
    assert cls.__tablename__ == 'psa_code'
    assert has_unique_constraint(cls.__table__, ('code', 'email'))
    with dbcleanup(session, cls):
        email, code = 'a', get_random_string()
        obj = cls(email, code)
        obj_id = persist(session, obj)

        stored_obj = get_stored_obj(session, cls, obj_id)
        # test mapped columns
        assert stored_obj.id == obj_id
        assert stored_obj.email == email
        assert stored_obj.code == code


#class Test(BaseTest):
#
#    def test_table(self, cls_):
#        assert cls_.__tablename__ == ''
#
#    def test_columns(self, session, cls_):
#        obj = cls_()
#
#        with persist2(session, obj) as obj_id:
#            stored_obj = get_stored_obj(session, cls_, obj_id)
#            assert stored_obj.id == obj_id
#
#    def test_relationships(self, session, cls_):
#        obj = cls_()
#
#        with persist2(session, obj) as obj_id:
#            stored_obj = get_stored_obj(session, cls_, obj_id)


def test_PSANonce(model, session):
    cls = model.PSANonce
    assert cls.__tablename__ == 'psa_nonce'
    with dbcleanup(session, cls):
        server_url, timestamp, salt = 'a', 1, 'b'
        obj = cls(server_url, timestamp, salt)
        obj_id = persist(session, obj)

        stored_obj = get_stored_obj(session, cls, obj_id)
        # test mapped columns
        assert stored_obj.id == obj_id
        assert stored_obj.server_url
        assert stored_obj.timestamp == timestamp
        assert stored_obj.salt == salt


#class Test(BaseTest):
#
#    def test_table(self, cls_):
#        assert cls_.__tablename__ == ''
#
#    def test_columns(self, session, cls_):
#        obj = cls_()
#
#        with persist2(session, obj) as obj_id:
#            stored_obj = get_stored_obj(session, cls_, obj_id)
#            assert stored_obj.id == obj_id
#
#    def test_relationships(self, session, cls_):
#        obj = cls_()
#
#        with persist2(session, obj) as obj_id:
#            stored_obj = get_stored_obj(session, cls_, obj_id)


def test_PSAPartial(model, session):
    cls = model.PSAPartial
    assert cls.__tablename__ == 'psa_partial'
    with dbcleanup(session, cls):
        token, data, next_step, backend = 'a', 'b', 1, 'c'
        obj = cls(token, data, next_step, backend)
        obj_id = persist(session, obj)

        stored_obj = get_stored_obj(session, cls, obj_id)
        # test mapped columns
        assert stored_obj.id == obj_id
        assert stored_obj.token == token
        assert stored_obj.data == data
        assert stored_obj.next_step == next_step
        assert stored_obj.backend == backend


#class Test(BaseTest):
#
#    def test_table(self, cls_):
#        assert cls_.__tablename__ == ''
#
#    def test_columns(self, session, cls_):
#        obj = cls_()
#
#        with persist2(session, obj) as obj_id:
#            stored_obj = get_stored_obj(session, cls_, obj_id)
#            assert stored_obj.id == obj_id
#
#    def test_relationships(self, session, cls_):
#        obj = cls_()
#
#        with persist2(session, obj) as obj_id:
#            stored_obj = get_stored_obj(session, cls_, obj_id)


def test_Quota(
        model,
        session,
        default_quota_association,
        group_quota_association,
        user_quota_association
):
    cls = model.Quota
    assert cls.__tablename__ == 'quota'
    with dbcleanup(session, cls):
        name, description, amount, operation = get_random_string(), 'b', 42, '+'
        obj = cls(name, description, amount, operation)
        create_time = datetime.now()
        update_time = create_time + timedelta(hours=1)
        obj.create_time = create_time
        obj.update_time = update_time

        def add_association(assoc_object, assoc_attribute):
            assoc_object.quota = obj
            getattr(obj, assoc_attribute).append(assoc_object)

        add_association(default_quota_association, 'default')
        add_association(group_quota_association, 'groups')
        add_association(user_quota_association, 'users')

        obj_id = persist(session, obj)

        stored_obj = get_stored_obj(session, cls, obj_id)
        # test mapped columns
        assert stored_obj.id == obj_id
        assert stored_obj.create_time == create_time
        assert stored_obj.update_time == update_time
        assert stored_obj.name == name
        assert stored_obj.description == description
        assert stored_obj.bytes == amount
        assert stored_obj.operation == operation
        assert stored_obj.deleted is False
        # test mapped relationships
        assert stored_obj.default == [default_quota_association]
        assert stored_obj.groups == [group_quota_association]
        assert stored_obj.users == [user_quota_association]


#class Test(BaseTest):
#
#    def test_table(self, cls_):
#        assert cls_.__tablename__ == ''
#
#    def test_columns(self, session, cls_):
#        obj = cls_()
#
#        with persist2(session, obj) as obj_id:
#            stored_obj = get_stored_obj(session, cls_, obj_id)
#            assert stored_obj.id == obj_id
#
#    def test_relationships(self, session, cls_):
#        obj = cls_()
#
#        with persist2(session, obj) as obj_id:
#            stored_obj = get_stored_obj(session, cls_, obj_id)


def test_Role(
        model,
        session,
        dataset_permission,
        group_role_association,
        library_permission,
        library_folder_permission,
        library_dataset_permission,
        library_dataset_dataset_association_permission,
):
    cls = model.Role
    assert cls.__tablename__ == 'role'
    with dbcleanup(session, cls):
        name, description, type_, deleted = get_random_string(), 'b', cls.types.SYSTEM, True
        obj = cls(name, description, type_, deleted)
        create_time = datetime.now()
        update_time = create_time + timedelta(hours=1)
        obj.create_time = create_time
        obj.update_time = update_time
        obj.dataset_actions.append(dataset_permission)
        obj.library_actions.append(library_permission)
        obj.library_folder_actions.append(library_folder_permission)
        obj.library_dataset_actions.append(library_dataset_permission)
        obj.library_dataset_dataset_actions.append(library_dataset_dataset_association_permission)
        obj.groups.append(group_role_association)
        obj_id = persist(session, obj)

        stored_obj = get_stored_obj(session, cls, obj_id)
        # test mapped columns
        assert stored_obj.id == obj_id
        assert stored_obj.create_time == create_time
        assert stored_obj.update_time == update_time
        assert stored_obj.name == name
        assert stored_obj.description == description
        assert stored_obj.type == type_
        assert stored_obj.deleted == deleted
        # test mapped relationships
        assert stored_obj.dataset_actions == [dataset_permission]
        assert stored_obj.groups == [group_role_association]
        assert stored_obj.library_actions == [library_permission]
        assert stored_obj.library_folder_actions == [library_folder_permission]
        assert stored_obj.library_dataset_actions == [library_dataset_permission]
        assert stored_obj.library_dataset_dataset_actions == [library_dataset_dataset_association_permission]


#class Test(BaseTest):
#
#    def test_table(self, cls_):
#        assert cls_.__tablename__ == ''
#
#    def test_columns(self, session, cls_):
#        obj = cls_()
#
#        with persist2(session, obj) as obj_id:
#            stored_obj = get_stored_obj(session, cls_, obj_id)
#            assert stored_obj.id == obj_id
#
#    def test_relationships(self, session, cls_):
#        obj = cls_()
#
#        with persist2(session, obj) as obj_id:
#            stored_obj = get_stored_obj(session, cls_, obj_id)


def test_StoredWorkflowAnnotationAssociation(model, session, stored_workflow, user):
    cls = model.StoredWorkflowAnnotationAssociation
    assert cls.__tablename__ == 'stored_workflow_annotation_association'
    assert has_index(cls.__table__, ('annotation',))
    with dbcleanup(session, cls):
        annotation = 'a'
        obj = cls()
        obj.stored_workflow = stored_workflow
        obj.user = user
        obj.annotation = annotation
        obj_id = persist(session, obj)

        stored_obj = get_stored_obj(session, cls, obj_id)
        # test mapped columns
        assert stored_obj.id == obj_id
        assert stored_obj.stored_workflow_id == stored_workflow.id
        assert stored_obj.user_id == user.id
        assert stored_obj.annotation == annotation
        # test mapped relationships
        assert stored_obj.stored_workflow.id == stored_workflow.id
        assert stored_obj.user.id == user.id


#class Test(BaseTest):
#
#    def test_table(self, cls_):
#        assert cls_.__tablename__ == ''
#
#    def test_columns(self, session, cls_):
#        obj = cls_()
#
#        with persist2(session, obj) as obj_id:
#            stored_obj = get_stored_obj(session, cls_, obj_id)
#            assert stored_obj.id == obj_id
#
#    def test_relationships(self, session, cls_):
#        obj = cls_()
#
#        with persist2(session, obj) as obj_id:
#            stored_obj = get_stored_obj(session, cls_, obj_id)


def test_StoredWorkflowRatingAssociation(model, session, stored_workflow, user):
    cls = model.StoredWorkflowRatingAssociation
    assert cls.__tablename__ == 'stored_workflow_rating_association'
    with dbcleanup(session, cls):
        rating = 9
        obj = cls(user, stored_workflow, rating)
        obj_id = persist(session, obj)

        stored_obj = get_stored_obj(session, cls, obj_id)
        # test mapped columns
        assert stored_obj.id == obj_id
        assert stored_obj.stored_workflow_id == stored_workflow.id
        assert stored_obj.user_id == user.id
        assert stored_obj.rating == rating
        # test mapped relationships
        assert stored_obj.stored_workflow.id == stored_workflow.id
        assert stored_obj.user.id == user.id


#class Test(BaseTest):
#
#    def test_table(self, cls_):
#        assert cls_.__tablename__ == ''
#
#    def test_columns(self, session, cls_):
#        obj = cls_()
#
#        with persist2(session, obj) as obj_id:
#            stored_obj = get_stored_obj(session, cls_, obj_id)
#            assert stored_obj.id == obj_id
#
#    def test_relationships(self, session, cls_):
#        obj = cls_()
#
#        with persist2(session, obj) as obj_id:
#            stored_obj = get_stored_obj(session, cls_, obj_id)


def test_StoredWorkflowTagAssociation(model, session, stored_workflow, tag, user):
    cls = model.StoredWorkflowTagAssociation
    assert cls.__tablename__ == 'stored_workflow_tag_association'
    with dbcleanup(session, cls):
        user_tname, value, user_value = 'a', 'b', 'c'
        obj = cls(user=user, tag_id=tag.id, user_tname=user_tname, value=value)
        obj.user_value = user_value
        obj.stored_workflow = stored_workflow
        obj_id = persist(session, obj)

        stored_obj = get_stored_obj(session, cls, obj_id)
        # test mapped columns
        assert stored_obj.id == obj_id
        assert stored_obj.stored_workflow_id == stored_workflow.id
        assert stored_obj.tag_id == tag.id
        assert stored_obj.user_id == user.id
        assert stored_obj.user_tname == user_tname
        assert stored_obj.value == value
        assert stored_obj.user_value == user_value
        # test mapped relationships
        assert stored_obj.stored_workflow.id == stored_workflow.id
        assert stored_obj.tag.id == tag.id
        assert stored_obj.user.id == user.id


#class Test(BaseTest):
#
#    def test_table(self, cls_):
#        assert cls_.__tablename__ == ''
#
#    def test_columns(self, session, cls_):
#        obj = cls_()
#
#        with persist2(session, obj) as obj_id:
#            stored_obj = get_stored_obj(session, cls_, obj_id)
#            assert stored_obj.id == obj_id
#
#    def test_relationships(self, session, cls_):
#        obj = cls_()
#
#        with persist2(session, obj) as obj_id:
#            stored_obj = get_stored_obj(session, cls_, obj_id)


def test_Tag(
        model,
        session,
        history_tag_association,
        history_dataset_association_tag_association,
        library_dataset_dataset_association_tag_association,
        page_tag_association,
        workflow_step_tag_association,
        stored_workflow_tag_association,
        visualization_tag_association,
        history_dataset_collection_tag_association,
        library_dataset_collection_tag_association,
        tool_tag_association,
):
    cls = model.Tag
    assert cls.__tablename__ == 'tag'
    assert has_unique_constraint(cls.__table__, ('name',))

    with dbcleanup(session, cls):
        parent_tag = cls()
        child_tag = cls()
        type_, name = 1, 'a'
        obj = cls(type=type_, name=name)
        obj.parent = parent_tag
        obj.children.append(child_tag)

        def add_association(assoc_object, assoc_attribute):
            assoc_object.tag = obj
            getattr(obj, assoc_attribute).append(assoc_object)

        add_association(history_tag_association, 'tagged_histories')
        add_association(history_dataset_association_tag_association, 'tagged_history_dataset_associations')
        add_association(library_dataset_dataset_association_tag_association, 'tagged_library_dataset_dataset_associations')
        add_association(page_tag_association, 'tagged_pages')
        add_association(workflow_step_tag_association, 'tagged_workflow_steps')
        add_association(stored_workflow_tag_association, 'tagged_stored_workflows')
        add_association(visualization_tag_association, 'tagged_visualizations')
        add_association(history_dataset_collection_tag_association, 'tagged_history_dataset_collections')
        add_association(library_dataset_collection_tag_association, 'tagged_library_dataset_collections')
        add_association(tool_tag_association, 'tagged_tools')

        obj_id = persist(session, obj)

        stored_obj = get_stored_obj(session, cls, obj_id)
        # test mapped columns
        assert stored_obj.id == obj_id
        assert stored_obj.type == type_
        assert stored_obj.parent_id == parent_tag.id
        assert stored_obj.name == name
        # test mapped relationships
        assert stored_obj.parent.id == parent_tag.id
        assert stored_obj.children == [child_tag]
        assert stored_obj.tagged_histories == [history_tag_association]
        assert stored_obj.tagged_history_dataset_associations == [history_dataset_association_tag_association]
        assert stored_obj.tagged_library_dataset_dataset_associations == [library_dataset_dataset_association_tag_association]
        assert stored_obj.tagged_pages == [page_tag_association]
        assert stored_obj.tagged_workflow_steps == [workflow_step_tag_association]
        assert stored_obj.tagged_stored_workflows == [stored_workflow_tag_association]
        assert stored_obj.tagged_visualizations == [visualization_tag_association]
        assert stored_obj.tagged_history_dataset_collections == [history_dataset_collection_tag_association]
        assert stored_obj.tagged_library_dataset_collections == [library_dataset_collection_tag_association]
        assert stored_obj.tagged_tools == [tool_tag_association]


#class Test(BaseTest):
#
#    def test_table(self, cls_):
#        assert cls_.__tablename__ == ''
#
#    def test_columns(self, session, cls_):
#        obj = cls_()
#
#        with persist2(session, obj) as obj_id:
#            stored_obj = get_stored_obj(session, cls_, obj_id)
#            assert stored_obj.id == obj_id
#
#    def test_relationships(self, session, cls_):
#        obj = cls_()
#
#        with persist2(session, obj) as obj_id:
#            stored_obj = get_stored_obj(session, cls_, obj_id)


def test_Task(model, session, job, task_metric_numeric, task_metric_text):
    cls = model.Task
    assert cls.__tablename__ == 'task'
    with dbcleanup(session, cls):
        create_time = datetime.now()
        execution_time = create_time + timedelta(hours=1)
        update_time = execution_time + timedelta(hours=1)
        state = model.Task.states.WAITING
        command_line = 'a'
        param_filename = 'b'
        runner_name = 'c'
        job_stdout = 'd'
        job_stderr = 'e'
        tool_stdout = 'f'
        tool_stderr = 'g'
        exit_code = 9
        job_messages = 'h'
        info = 'i'
        traceback = 'j'
        working_directory = 'k'
        task_runner_name = 'l'
        task_runner_external_id = 'm'
        prepare_input_files_cmd = 'n'

        obj = cls(job, working_directory, prepare_input_files_cmd)
        obj.create_time = create_time
        obj.execution_time = execution_time
        obj.update_time = update_time
        obj.state = state
        obj.command_line = command_line
        obj.param_filename = param_filename
        obj.runner_name = runner_name
        obj.job_stdout = job_stdout
        obj.job_stderr = job_stderr
        obj.tool_stdout = tool_stdout
        obj.tool_stderr = tool_stderr
        obj.exit_code = exit_code
        obj.job_messages = job_messages
        obj.info = info
        obj.traceback = traceback
        obj.task_runner_name = task_runner_name
        obj.task_runner_external_id = task_runner_external_id
        obj.numeric_metrics.append(task_metric_numeric)
        obj.text_metrics.append(task_metric_text)
        obj_id = persist(session, obj)

        stored_obj = get_stored_obj(session, cls, obj_id)
        # test mapped columns
        assert stored_obj.id == obj_id
        assert stored_obj.create_time == create_time
        assert stored_obj.execution_time == execution_time
        assert stored_obj.update_time == update_time
        assert stored_obj.state == state
        assert stored_obj.command_line == command_line
        assert stored_obj.param_filename == param_filename
        assert stored_obj.runner_name == runner_name
        assert stored_obj.job_stdout == job_stdout
        assert stored_obj.job_stderr == job_stderr
        assert stored_obj.tool_stdout == tool_stdout
        assert stored_obj.tool_stderr == tool_stderr
        assert stored_obj.exit_code == exit_code
        assert stored_obj.job_messages == job_messages
        assert stored_obj.info == info
        assert stored_obj.traceback == traceback
        assert stored_obj.task_runner_name == task_runner_name
        assert stored_obj.task_runner_external_id == task_runner_external_id
        # test mapped relationships
        assert stored_obj.job.id == job.id
        assert stored_obj.numeric_metrics == [task_metric_numeric]
        assert stored_obj.text_metrics == [task_metric_text]


#class Test(BaseTest):
#
#    def test_table(self, cls_):
#        assert cls_.__tablename__ == ''
#
#    def test_columns(self, session, cls_):
#        obj = cls_()
#
#        with persist2(session, obj) as obj_id:
#            stored_obj = get_stored_obj(session, cls_, obj_id)
#            assert stored_obj.id == obj_id
#
#    def test_relationships(self, session, cls_):
#        obj = cls_()
#
#        with persist2(session, obj) as obj_id:
#            stored_obj = get_stored_obj(session, cls_, obj_id)


def test_TaskMetricNumeric(model, session, task):
    cls = model.TaskMetricNumeric
    assert cls.__tablename__ == 'task_metric_numeric'
    with dbcleanup(session, cls):
        plugin, metric_name, metric_value = 'a', 'b', 9
        obj = cls(plugin, metric_name, metric_value)
        obj.task = task
        obj_id = persist(session, obj)

        stored_obj = get_stored_obj(session, cls, obj_id)
        # test mapped columns
        assert stored_obj.id == obj_id
        assert stored_obj.task_id == task.id
        assert stored_obj.plugin == plugin
        assert stored_obj.metric_value == metric_value
        # test mapped relationships
        assert stored_obj.task.id == task.id


#class Test(BaseTest):
#
#    def test_table(self, cls_):
#        assert cls_.__tablename__ == ''
#
#    def test_columns(self, session, cls_):
#        obj = cls_()
#
#        with persist2(session, obj) as obj_id:
#            stored_obj = get_stored_obj(session, cls_, obj_id)
#            assert stored_obj.id == obj_id
#
#    def test_relationships(self, session, cls_):
#        obj = cls_()
#
#        with persist2(session, obj) as obj_id:
#            stored_obj = get_stored_obj(session, cls_, obj_id)


def test_TaskMetricText(model, session, task):
    cls = model.TaskMetricText
    assert cls.__tablename__ == 'task_metric_text'
    with dbcleanup(session, cls):
        plugin, metric_name, metric_value = 'a', 'b', 'c'
        obj = cls(plugin, metric_name, metric_value)
        obj.task = task
        obj_id = persist(session, obj)

        stored_obj = get_stored_obj(session, cls, obj_id)
        # test mapped columns
        assert stored_obj.id == obj_id
        assert stored_obj.task_id == task.id
        assert stored_obj.plugin == plugin
        assert stored_obj.metric_value == metric_value
        # test mapped relationships
        assert stored_obj.task.id == task.id


#class Test(BaseTest):
#
#    def test_table(self, cls_):
#        assert cls_.__tablename__ == ''
#
#    def test_columns(self, session, cls_):
#        obj = cls_()
#
#        with persist2(session, obj) as obj_id:
#            stored_obj = get_stored_obj(session, cls_, obj_id)
#            assert stored_obj.id == obj_id
#
#    def test_relationships(self, session, cls_):
#        obj = cls_()
#
#        with persist2(session, obj) as obj_id:
#            stored_obj = get_stored_obj(session, cls_, obj_id)


def test_ToolTagAssociation(model, session, tag, user):
    cls = model.ToolTagAssociation
    assert cls.__tablename__ == 'tool_tag_association'
    with dbcleanup(session, cls):
        user_tname, value, user_value, tool_id = 'a', 'b', 'c', 'd'
        obj = cls(user=user, tag_id=tag.id, user_tname=user_tname, value=value)
        obj.user_value = user_value
        obj.tool_id = tool_id
        obj_id = persist(session, obj)

        stored_obj = get_stored_obj(session, cls, obj_id)
        # test mapped columns
        assert stored_obj.id == obj_id
        assert stored_obj.tool_id == tool_id
        assert stored_obj.tag_id == tag.id
        assert stored_obj.user_id == user.id
        assert stored_obj.user_tname == user_tname
        assert stored_obj.value == value
        assert stored_obj.user_value == user_value
        # test mapped relationships
        assert stored_obj.tag.id == tag.id
        assert stored_obj.user.id == user.id


#class Test(BaseTest):
#
#    def test_table(self, cls_):
#        assert cls_.__tablename__ == ''
#
#    def test_columns(self, session, cls_):
#        obj = cls_()
#
#        with persist2(session, obj) as obj_id:
#            stored_obj = get_stored_obj(session, cls_, obj_id)
#            assert stored_obj.id == obj_id
#
#    def test_relationships(self, session, cls_):
#        obj = cls_()
#
#        with persist2(session, obj) as obj_id:
#            stored_obj = get_stored_obj(session, cls_, obj_id)


def test_UserAction(model, session, user, galaxy_session):
    cls = model.UserAction
    assert cls.__tablename__ == 'user_action'
    with dbcleanup(session, cls):
        action, params, context = 'a', 'b', 'c'
        obj = cls(user, galaxy_session.id, action, params, context)
        create_time = datetime.now()
        obj.create_time = create_time
        obj_id = persist(session, obj)

        stored_obj = get_stored_obj(session, cls, obj_id)
        # test mapped columns
        assert stored_obj.id == obj_id
        assert stored_obj.create_time == create_time
        assert stored_obj.user_id == user.id
        assert stored_obj.session_id == galaxy_session.id
        assert stored_obj.action == action
        assert stored_obj.context == context
        assert stored_obj.params == params
        # test mapped relationships
        assert stored_obj.user.id == user.id


#class Test(BaseTest):
#
#    def test_table(self, cls_):
#        assert cls_.__tablename__ == ''
#
#    def test_columns(self, session, cls_):
#        obj = cls_()
#
#        with persist2(session, obj) as obj_id:
#            stored_obj = get_stored_obj(session, cls_, obj_id)
#            assert stored_obj.id == obj_id
#
#    def test_relationships(self, session, cls_):
#        obj = cls_()
#
#        with persist2(session, obj) as obj_id:
#            stored_obj = get_stored_obj(session, cls_, obj_id)


def test_UserAddress(model, session, user):
    cls = model.UserAddress
    assert cls.__tablename__ == 'user_address'
    with dbcleanup(session, cls):
        desc, name, institution, address, city, state, postal_code, country, phone, deleted, purged = \
            'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', True, False
        obj = cls(user, desc, name, institution, address, city, state, postal_code, country, phone)
        create_time = datetime.now()
        update_time = create_time + timedelta(hours=1)
        obj.create_time = create_time
        obj.update_time = update_time
        obj.deleted = deleted
        obj.purged = purged
        obj_id = persist(session, obj)

        stored_obj = get_stored_obj(session, cls, obj_id)
        # test mapped columns
        assert stored_obj.id == obj_id
        assert stored_obj.create_time == create_time
        assert stored_obj.update_time == update_time
        assert stored_obj.user_id == user.id
        assert stored_obj.desc == desc
        assert stored_obj.name == name
        assert stored_obj.institution == institution
        assert stored_obj.address == address
        assert stored_obj.city == city
        assert stored_obj.state == state
        assert stored_obj.postal_code == postal_code
        assert stored_obj.country == country
        assert stored_obj.phone == phone
        assert stored_obj.deleted == deleted
        assert stored_obj.purged == purged
        # test mapped relationships
        assert stored_obj.user.id == user.id


#class Test(BaseTest):
#
#    def test_table(self, cls_):
#        assert cls_.__tablename__ == ''
#
#    def test_columns(self, session, cls_):
#        obj = cls_()
#
#        with persist2(session, obj) as obj_id:
#            stored_obj = get_stored_obj(session, cls_, obj_id)
#            assert stored_obj.id == obj_id
#
#    def test_relationships(self, session, cls_):
#        obj = cls_()
#
#        with persist2(session, obj) as obj_id:
#            stored_obj = get_stored_obj(session, cls_, obj_id)


def test_UserAuthnzToken(model, session, user, cloud_authz):
    cls = model.UserAuthnzToken
    assert cls.__tablename__ == 'oidc_user_authnz_tokens'
    assert has_unique_constraint(cls.__table__, ('provider', 'uid'))
    with dbcleanup(session, cls):
        provider, uid, extra_data, lifetime, assoc_type = get_random_string(), 'b', 'c', 1, 'd'
        obj = cls(provider, uid, extra_data, lifetime, assoc_type, user)
        obj.cloudauthz.append(cloud_authz)
        obj_id = persist(session, obj)

        stored_obj = get_stored_obj(session, cls, obj_id)
        # test mapped columns
        assert stored_obj.id == obj_id
        assert stored_obj.user_id == user.id
        assert stored_obj.uid == uid
        assert stored_obj.provider == provider
        assert stored_obj.extra_data == extra_data
        assert stored_obj.lifetime == lifetime
        assert stored_obj.assoc_type == assoc_type
        # test mapped relationships
        assert stored_obj.cloudauthz == [cloud_authz]
        assert stored_obj.user.id == user.id


#class Test(BaseTest):
#
#    def test_table(self, cls_):
#        assert cls_.__tablename__ == ''
#
#    def test_columns(self, session, cls_):
#        obj = cls_()
#
#        with persist2(session, obj) as obj_id:
#            stored_obj = get_stored_obj(session, cls_, obj_id)
#            assert stored_obj.id == obj_id
#
#    def test_relationships(self, session, cls_):
#        obj = cls_()
#
#        with persist2(session, obj) as obj_id:
#            stored_obj = get_stored_obj(session, cls_, obj_id)


def test_UserGroupAssociation(model, session, user, group):
    cls = model.UserGroupAssociation
    assert cls.__tablename__ == 'user_group_association'
    with dbcleanup(session, cls):
        obj = cls(user, group)
        create_time = datetime.now()
        update_time = create_time + timedelta(hours=1)
        obj.create_time = create_time
        obj.update_time = update_time
        obj_id = persist(session, obj)

        stored_obj = get_stored_obj(session, cls, obj_id)
        # test mapped columns
        assert stored_obj.id == obj_id
        assert stored_obj.user_id == user.id
        assert stored_obj.group_id == group.id
        assert stored_obj.create_time == create_time
        assert stored_obj.update_time == update_time
        # test mapped relationships
        assert stored_obj.user.id == user.id
        assert stored_obj.group.id == group.id


#class Test(BaseTest):
#
#    def test_table(self, cls_):
#        assert cls_.__tablename__ == ''
#
#    def test_columns(self, session, cls_):
#        obj = cls_()
#
#        with persist2(session, obj) as obj_id:
#            stored_obj = get_stored_obj(session, cls_, obj_id)
#            assert stored_obj.id == obj_id
#
#    def test_relationships(self, session, cls_):
#        obj = cls_()
#
#        with persist2(session, obj) as obj_id:
#            stored_obj = get_stored_obj(session, cls_, obj_id)


def test_UserQuotaAssociation(model, session, user, quota):
    cls = model.UserQuotaAssociation
    assert cls.__tablename__ == 'user_quota_association'
    with dbcleanup(session, cls):
        obj = cls(user, quota)
        create_time = datetime.now()
        update_time = create_time + timedelta(hours=1)
        obj.create_time = create_time
        obj.update_time = update_time
        obj_id = persist(session, obj)

        stored_obj = get_stored_obj(session, cls, obj_id)
        # test mapped columns
        assert stored_obj.id == obj_id
        assert stored_obj.user_id == user.id
        assert stored_obj.quota_id == quota.id
        assert stored_obj.create_time == create_time
        assert stored_obj.update_time == update_time
        # test mapped relationships
        assert stored_obj.user.id == user.id
        assert stored_obj.quota.id == quota.id


#class Test(BaseTest):
#
#    def test_table(self, cls_):
#        assert cls_.__tablename__ == ''
#
#    def test_columns(self, session, cls_):
#        obj = cls_()
#
#        with persist2(session, obj) as obj_id:
#            stored_obj = get_stored_obj(session, cls_, obj_id)
#            assert stored_obj.id == obj_id
#
#    def test_relationships(self, session, cls_):
#        obj = cls_()
#
#        with persist2(session, obj) as obj_id:
#            stored_obj = get_stored_obj(session, cls_, obj_id)


def test_VisualizationAnnotationAssociation(model, session, visualization, user):
    cls = model.VisualizationAnnotationAssociation
    assert cls.__tablename__ == 'visualization_annotation_association'
    assert has_index(cls.__table__, ('annotation',))
    with dbcleanup(session, cls):
        annotation = 'a'
        obj = cls()
        obj.user = user
        obj.visualization = visualization
        obj.annotation = annotation
        obj_id = persist(session, obj)

        stored_obj = get_stored_obj(session, cls, obj_id)
        # test mapped columns
        assert stored_obj.id == obj_id
        assert stored_obj.visualization_id == visualization.id
        assert stored_obj.user_id == user.id
        assert stored_obj.annotation == annotation
        # test mapped relationships
        assert stored_obj.visualization.id == visualization.id
        assert stored_obj.user.id == user.id


#class Test(BaseTest):
#
#    def test_table(self, cls_):
#        assert cls_.__tablename__ == ''
#
#    def test_columns(self, session, cls_):
#        obj = cls_()
#
#        with persist2(session, obj) as obj_id:
#            stored_obj = get_stored_obj(session, cls_, obj_id)
#            assert stored_obj.id == obj_id
#
#    def test_relationships(self, session, cls_):
#        obj = cls_()
#
#        with persist2(session, obj) as obj_id:
#            stored_obj = get_stored_obj(session, cls_, obj_id)


def test_VisualizationRatingAssociation(model, session, visualization, user):
    cls = model.VisualizationRatingAssociation
    assert cls.__tablename__ == 'visualization_rating_association'
    with dbcleanup(session, cls):
        rating = 9
        obj = cls(user, visualization, rating)
        obj_id = persist(session, obj)

        stored_obj = get_stored_obj(session, cls, obj_id)
        # test mapped columns
        assert stored_obj.id == obj_id
        assert stored_obj.visualization_id == visualization.id
        assert stored_obj.user_id == user.id
        assert stored_obj.rating == rating
        # test mapped relationships
        assert stored_obj.visualization.id == visualization.id
        assert stored_obj.user.id == user.id


#class Test(BaseTest):
#
#    def test_table(self, cls_):
#        assert cls_.__tablename__ == ''
#
#    def test_columns(self, session, cls_):
#        obj = cls_()
#
#        with persist2(session, obj) as obj_id:
#            stored_obj = get_stored_obj(session, cls_, obj_id)
#            assert stored_obj.id == obj_id
#
#    def test_relationships(self, session, cls_):
#        obj = cls_()
#
#        with persist2(session, obj) as obj_id:
#            stored_obj = get_stored_obj(session, cls_, obj_id)


def test_VisualizationRevision(model, session, visualization):
    cls = model.VisualizationRevision
    assert cls.__tablename__ == 'visualization_revision'
    assert has_index(cls.__table__, ('dbkey',))
    with dbcleanup(session, cls):
        visualization, title, dbkey, config = visualization, 'a', 'b', 'c'
        obj = cls(visualization, title, dbkey, config)
        create_time = datetime.now()
        update_time = create_time + timedelta(hours=1)
        obj.create_time = create_time
        obj.update_time = update_time
        obj_id = persist(session, obj)

        stored_obj = get_stored_obj(session, cls, obj_id)
        # test mapped columns
        assert stored_obj.id == obj_id
        assert stored_obj.create_time == create_time
        assert stored_obj.update_time == update_time
        assert stored_obj.visualization_id == visualization.id
        assert stored_obj.title == title
        assert stored_obj.dbkey == dbkey
        assert stored_obj.config == config
        # test mapped relationships
        assert stored_obj.visualization.id == visualization.id


#class Test(BaseTest):
#
#    def test_table(self, cls_):
#        assert cls_.__tablename__ == ''
#
#    def test_columns(self, session, cls_):
#        obj = cls_()
#
#        with persist2(session, obj) as obj_id:
#            stored_obj = get_stored_obj(session, cls_, obj_id)
#            assert stored_obj.id == obj_id
#
#    def test_relationships(self, session, cls_):
#        obj = cls_()
#
#        with persist2(session, obj) as obj_id:
#            stored_obj = get_stored_obj(session, cls_, obj_id)


def test_WorkerProcess(model, session):
    cls = model.WorkerProcess
    assert cls.__tablename__ == 'worker_process'
    assert has_unique_constraint(cls.__table__, ('server_name', 'hostname'))
    with dbcleanup(session, cls):
        server_name, hostname = get_random_string(), 'a'
        obj = cls(server_name, hostname)
        update_time = datetime.now()
        obj.update_time = update_time
        obj_id = persist(session, obj)

        stored_obj = get_stored_obj(session, cls, obj_id)
        # test mapped columns
        assert stored_obj.id == obj_id
        assert stored_obj.server_name == server_name
        assert stored_obj.hostname == hostname
        assert stored_obj.pid is None
        assert stored_obj.update_time == update_time


#class Test(BaseTest):
#
#    def test_table(self, cls_):
#        assert cls_.__tablename__ == ''
#
#    def test_columns(self, session, cls_):
#        obj = cls_()
#
#        with persist2(session, obj) as obj_id:
#            stored_obj = get_stored_obj(session, cls_, obj_id)
#            assert stored_obj.id == obj_id
#
#    def test_relationships(self, session, cls_):
#        obj = cls_()
#
#        with persist2(session, obj) as obj_id:
#            stored_obj = get_stored_obj(session, cls_, obj_id)


def test_WorkflowStepAnnotationAssociation(model, session, workflow_step, user):
    cls = model.WorkflowStepAnnotationAssociation
    assert cls.__tablename__ == 'workflow_step_annotation_association'
    assert has_index(cls.__table__, ('annotation',))
    with dbcleanup(session, cls):
        annotation = 'a'
        obj = cls()
        obj.user = user
        obj.workflow_step = workflow_step
        obj.annotation = annotation
        obj_id = persist(session, obj)

        stored_obj = get_stored_obj(session, cls, obj_id)
        # test mapped columns
        assert stored_obj.id == obj_id
        assert stored_obj.workflow_step_id == workflow_step.id
        assert stored_obj.user_id == user.id
        assert stored_obj.annotation == annotation
        # test mapped relationships
        assert stored_obj.workflow_step.id == workflow_step.id
        assert stored_obj.user.id == user.id


#class Test(BaseTest):
#
#    def test_table(self, cls_):
#        assert cls_.__tablename__ == ''
#
#    def test_columns(self, session, cls_):
#        obj = cls_()
#
#        with persist2(session, obj) as obj_id:
#            stored_obj = get_stored_obj(session, cls_, obj_id)
#            assert stored_obj.id == obj_id
#
#    def test_relationships(self, session, cls_):
#        obj = cls_()
#
#        with persist2(session, obj) as obj_id:
#            stored_obj = get_stored_obj(session, cls_, obj_id)


def test_WorkflowStepTagAssociation(model, session, workflow_step, tag, user):
    cls = model.WorkflowStepTagAssociation
    assert cls.__tablename__ == 'workflow_step_tag_association'
    with dbcleanup(session, cls):
        user_tname, value, user_value = 'a', 'b', 'c'
        obj = cls(user=user, tag_id=tag.id, user_tname=user_tname, value=value)
        obj.user_value = user_value
        obj.workflow_step = workflow_step
        obj_id = persist(session, obj)

        stored_obj = get_stored_obj(session, cls, obj_id)
        # test mapped columns
        assert stored_obj.id == obj_id
        assert stored_obj.workflow_step_id == workflow_step.id
        assert stored_obj.tag_id == tag.id
        assert stored_obj.user_id == user.id
        assert stored_obj.user_tname == user_tname
        assert stored_obj.value == value
        assert stored_obj.user_value == user_value
        # test mapped relationships
        assert stored_obj.workflow_step.id == workflow_step.id
        assert stored_obj.tag.id == tag.id
        assert stored_obj.user.id == user.id


#class Test(BaseTest):
#
#    def test_table(self, cls_):
#        assert cls_.__tablename__ == ''
#
#    def test_columns(self, session, cls_):
#        obj = cls_()
#
#        with persist2(session, obj) as obj_id:
#            stored_obj = get_stored_obj(session, cls_, obj_id)
#            assert stored_obj.id == obj_id
#
#    def test_relationships(self, session, cls_):
#        obj = cls_()
#
#        with persist2(session, obj) as obj_id:
#            stored_obj = get_stored_obj(session, cls_, obj_id)


def test_VisualizationTagAssociation(model, session, visualization, tag, user):
    cls = model.VisualizationTagAssociation
    assert cls.__tablename__ == 'visualization_tag_association'
    with dbcleanup(session, cls):
        user_tname, value, user_value = 'a', 'b', 'c'
        obj = cls(user=user, tag_id=tag.id, user_tname=user_tname, value=value)
        obj.user_value = user_value
        obj.visualization = visualization
        obj_id = persist(session, obj)

        stored_obj = get_stored_obj(session, cls, obj_id)
        # test mapped columns
        assert stored_obj.id == obj_id
        assert stored_obj.visualization_id == visualization.id
        assert stored_obj.tag_id == tag.id
        assert stored_obj.user_id == user.id
        assert stored_obj.user_tname == user_tname
        assert stored_obj.value == value
        assert stored_obj.user_value == user_value
        # test mapped relationships
        assert stored_obj.visualization.id == visualization.id
        assert stored_obj.tag.id == tag.id
        assert stored_obj.user.id == user.id


#class Test(BaseTest):
#
#    def test_table(self, cls_):
#        assert cls_.__tablename__ == ''
#
#    def test_columns(self, session, cls_):
#        obj = cls_()
#
#        with persist2(session, obj) as obj_id:
#            stored_obj = get_stored_obj(session, cls_, obj_id)
#            assert stored_obj.id == obj_id
#
#    def test_relationships(self, session, cls_):
#        obj = cls_()
#
#        with persist2(session, obj) as obj_id:
#            stored_obj = get_stored_obj(session, cls_, obj_id)


def test_WorkflowRequestInputParameter(model, session, workflow_invocation):
    cls = model.WorkflowRequestInputParameter
    assert cls.__tablename__ == 'workflow_request_input_parameters'
    with dbcleanup(session, cls):
        name, value, type = 'a', 'b', 'c'
        obj = cls(name, value, type)
        obj.workflow_invocation = workflow_invocation
        obj_id = persist(session, obj)

        stored_obj = get_stored_obj(session, cls, obj_id)
        # test mapped columns
        assert stored_obj.id == obj_id
        assert stored_obj.workflow_invocation_id == workflow_invocation.id
        assert stored_obj.name == name
        assert stored_obj.value == value
        assert stored_obj.type == type
        # test mapped relationships
        assert stored_obj.workflow_invocation.id == workflow_invocation.id


@pytest.fixture(scope='module')
def model():
    db_uri = 'sqlite:///:memory:'
    return mapping.init('/tmp', db_uri, create_tables=True)


@pytest.fixture
def session(model):
    Session = model.session
    yield Session()
    Session.remove()  # Ensures we get a new session for each test


@pytest.fixture
def cloud_authz(model, session, user, user_authnz_token):
    ca = model.CloudAuthz(user.id, 'a', 'b', user_authnz_token.id, 'c')
    yield from dbcleanup_wrapper(session, ca)


@pytest.fixture
def dataset(model, session):
    d = model.Dataset()
    yield from dbcleanup_wrapper(session, d)


@pytest.fixture
def dataset_collection(model, session):
    dc = model.DatasetCollection(collection_type='a')
    yield from dbcleanup_wrapper(session, dc)


@pytest.fixture
def dataset_collection_element(
        model, session, dataset_collection, history_dataset_association):
    dce = model.DatasetCollectionElement(
        collection=dataset_collection, element=history_dataset_association)
    yield from dbcleanup_wrapper(session, dce)


@pytest.fixture
def dataset_permission(model, session, dataset):
    d = model.DatasetPermissions('a', dataset)
    yield from dbcleanup_wrapper(session, d)


@pytest.fixture
def dataset_source(model, session):
    d = model.DatasetSource()
    yield from dbcleanup_wrapper(session, d)


@pytest.fixture
def dataset_source_hash(model, session):
    d = model.DatasetSourceHash()
    yield from dbcleanup_wrapper(session, d)


@pytest.fixture
def default_quota_association(model, session, quota):
    type_ = model.DefaultQuotaAssociation.types.REGISTERED
    dqa = model.DefaultQuotaAssociation(type_, quota)
    yield from dbcleanup_wrapper(session, dqa)


@pytest.fixture
def form_definition(model, session, form_definition_current):
    fd = model.FormDefinition(name='a', form_definition_current=form_definition_current)
    yield from dbcleanup_wrapper(session, fd)


@pytest.fixture
def form_definition_current(model, session):
    fdc = model.FormDefinitionCurrent()
    yield from dbcleanup_wrapper(session, fdc)


@pytest.fixture
def galaxy_session(model, session, user):
    s = model.GalaxySession()
    yield from dbcleanup_wrapper(session, s)


@pytest.fixture
def group(model, session):
    g = model.Group()
    yield from dbcleanup_wrapper(session, g)


@pytest.fixture
def group_quota_association(model, session):
    gqa = model.GroupQuotaAssociation(None, None)
    yield from dbcleanup_wrapper(session, gqa)


@pytest.fixture
def group_role_association(model, session):
    gra = model.GroupRoleAssociation(None, None)
    yield from dbcleanup_wrapper(session, gra)


@pytest.fixture
def history(model, session):
    h = model.History()
    yield from dbcleanup_wrapper(session, h)


@pytest.fixture
def history_dataset_association(model, session, dataset):
    hda = model.HistoryDatasetAssociation(dataset=dataset)
    yield from dbcleanup_wrapper(session, hda)


@pytest.fixture
def history_dataset_association_tag_association(model, session):
    hdata = model.HistoryDatasetAssociationTagAssociation()
    yield from dbcleanup_wrapper(session, hdata)


@pytest.fixture
def history_dataset_collection_association(model, session):
    hdca = model.HistoryDatasetCollectionAssociation()
    yield from dbcleanup_wrapper(session, hdca)


@pytest.fixture
def history_dataset_collection_tag_association(model, session):
    hdcta = model.HistoryDatasetCollectionTagAssociation()
    yield from dbcleanup_wrapper(session, hdcta)


@pytest.fixture
def history_tag_association(model, session):
    hta = model.HistoryTagAssociation()
    yield from dbcleanup_wrapper(session, hta)


@pytest.fixture
def job(model, session):
    j = model.Job()
    yield from dbcleanup_wrapper(session, j)


@pytest.fixture
def library(model, session):
    lb = model.Library()
    yield from dbcleanup_wrapper(session, lb)


@pytest.fixture
def library_folder(model, session):
    lf = model.LibraryFolder()
    yield from dbcleanup_wrapper(session, lf)


@pytest.fixture
def library_dataset(model, session):
    ld = model.LibraryDataset()
    yield from dbcleanup_wrapper(session, ld)


@pytest.fixture
def library_dataset_collection_association(model, session):
    ldca = model.LibraryDatasetCollectionAssociation()
    yield from dbcleanup_wrapper(session, ldca)


@pytest.fixture
def library_dataset_collection_tag_association(model, session):
    ldcta = model.LibraryDatasetCollectionTagAssociation()
    yield from dbcleanup_wrapper(session, ldcta)


@pytest.fixture
def library_dataset_dataset_association(model, session):
    ldda = model.LibraryDatasetDatasetAssociation()
    yield from dbcleanup_wrapper(session, ldda)


@pytest.fixture
def library_dataset_dataset_association_tag_association(model, session):
    lddata = model.LibraryDatasetDatasetAssociationTagAssociation()
    yield from dbcleanup_wrapper(session, lddata)


@pytest.fixture
def library_dataset_permission(model, session, library_dataset, role):
    ldp = model.LibraryDatasetPermissions('a', library_dataset, role)
    yield from dbcleanup_wrapper(session, ldp)


@pytest.fixture
def library_dataset_dataset_association_permission(model, session, library_dataset_dataset_association, role):
    lddp = model.LibraryDatasetDatasetAssociationPermissions('a', library_dataset_dataset_association, role)
    yield from dbcleanup_wrapper(session, lddp)


@pytest.fixture
def library_folder_permission(model, session, library_folder, role):
    lfp = model.LibraryFolderPermissions('a', library_folder, role)
    yield from dbcleanup_wrapper(session, lfp)


@pytest.fixture
def library_permission(model, session, library, role):
    lp = model.LibraryPermissions('a', library, role)
    yield from dbcleanup_wrapper(session, lp)


@pytest.fixture
def page(model, session, user):
    p = model.Page()
    p.user = user
    yield from dbcleanup_wrapper(session, p)


@pytest.fixture
def page_revision(model, session, page):
    pr = model.PageRevision()
    pr.page = page
    yield from dbcleanup_wrapper(session, pr)


@pytest.fixture
def page_annotation_association(model, session):
    paa = model.PageAnnotationAssociation()
    yield from dbcleanup_wrapper(session, paa)


@pytest.fixture
def page_rating_association(model, session):
    pra = model.PageRatingAssociation(None, None)
    yield from dbcleanup_wrapper(session, pra)


@pytest.fixture
def page_tag_association(model, session):
    pta = model.PageTagAssociation()
    yield from dbcleanup_wrapper(session, pta)


@pytest.fixture
def page_user_share_association(model, session):
    pra = model.PageUserShareAssociation()
    yield from dbcleanup_wrapper(session, pra)


@pytest.fixture
def quota(model, session):
    q = model.Quota(get_random_string(), 'b')
    yield from dbcleanup_wrapper(session, q)


@pytest.fixture
def role(model, session):
    r = model.Role()
    yield from dbcleanup_wrapper(session, r)


@pytest.fixture
def stored_workflow(model, session, user):
    w = model.StoredWorkflow()
    w.user = user
    yield from dbcleanup_wrapper(session, w)


@pytest.fixture
def stored_workflow_tag_association(model, session):
    swta = model.StoredWorkflowTagAssociation()
    yield from dbcleanup_wrapper(session, swta)


@pytest.fixture
def tag(model, session):
    t = model.Tag()
    yield from dbcleanup_wrapper(session, t)


@pytest.fixture
def task(model, session, job):
    t = model.Task(job, 'a', 'b')
    yield from dbcleanup_wrapper(session, t)


@pytest.fixture
def task_metric_numeric(model, session):
    tmn = model. TaskMetricNumeric('a', 'b', 9)
    yield from dbcleanup_wrapper(session, tmn)


@pytest.fixture
def task_metric_text(model, session):
    tmt = model. TaskMetricText('a', 'b', 'c')
    yield from dbcleanup_wrapper(session, tmt)


@pytest.fixture
def tool_tag_association(model, session):
    tta = model.ToolTagAssociation()
    yield from dbcleanup_wrapper(session, tta)


@pytest.fixture
def user(model, session):
    u = model.User(email='test@example.com', password='password')
    yield from dbcleanup_wrapper(session, u)


@pytest.fixture
def user_authnz_token(model, session, user):
    t = model.UserAuthnzToken('a', 'b', 'c', 1, 'd', user)
    yield from dbcleanup_wrapper(session, t)


@pytest.fixture
def user_quota_association(model, session):
    uqa = model.UserQuotaAssociation(None, None)
    yield from dbcleanup_wrapper(session, uqa)


@pytest.fixture
def visualization(model, session, user):
    v = model.Visualization()
    v.user = user
    yield from dbcleanup_wrapper(session, v)


@pytest.fixture
def visualization_tag_association(model, session):
    vta = model.VisualizationTagAssociation()
    yield from dbcleanup_wrapper(session, vta)


@pytest.fixture
def workflow(model, session):
    w = model.Workflow()
    yield from dbcleanup_wrapper(session, w)


@pytest.fixture
def workflow_invocation(model, session, workflow):
    wi = model.WorkflowInvocation()
    wi.workflow = workflow
    yield from dbcleanup_wrapper(session, wi)


@pytest.fixture
def workflow_step(model, session, workflow):
    s = model.WorkflowStep()
    s.workflow = workflow
    yield from dbcleanup_wrapper(session, s)


@pytest.fixture
def workflow_step_tag_association(model, session):
    wsta = model.WorkflowStepTagAssociation()
    yield from dbcleanup_wrapper(session, wsta)


@contextmanager
def dbcleanup(session, cls):
    """
    Ensure all records of cls are deleted from the database on exit.
    """
    try:
        yield
    finally:
        session.execute(delete(cls))


def dbcleanup_wrapper(session, obj):
    persist(session, obj)
    with dbcleanup(session, type(obj)):
        yield obj


@contextmanager
def persist2(session, obj):
    """Store obj in database, delete on exit."""
    try:
        session.add(obj)
        session.flush()
        obj_id = obj.id
        # Remove from session, so that on a subsequent load from the database we get a *new* obj.
        session.expunge(obj)
        yield obj_id
    finally:
        # Cannot do `session.delete(obj)` because obj has been replaced in the session with another
        # instance of the same class when calling `get_stored_obj()` in the test function.
        stored_obj = get_stored_obj(session, type(obj), obj_id)
        session.delete(stored_obj)  
        session.flush()


# TODO can we do better?
@contextmanager
def persist_no_id(session, obj, select_statement):
    """Store obj in database, delete on exit."""
    try:
        session.add(obj)
        session.flush()
        # Remove from session, so that on a subsequent load from the database we get a *new* obj.
        session.expunge(obj)
        yield
    finally:
        # Cannot do `session.delete(obj)` because obj has been replaced in the session with another
        # instance of the same class when calling `get_stored_obj()` in the test function.
        stored_obj = get_stored_obj(session, type(obj), stmt=select_statement)
        session.delete(stored_obj)  
        session.flush()


def persist(session, obj, return_id=True):
    session.add(obj)
    session.flush()
    obj_id = obj.id if return_id else None  # save this before obj is expunged
    # Remove from session, so that on a subsequent load we get a *new* obj from the db
    session.expunge(obj)
    return obj_id



def has_unique_constraint(table, fields):
    for constraint in table.constraints:
        if isinstance(constraint, UniqueConstraint):
            col_names = {c.name for c in constraint.columns}
            if set(fields) == col_names:
                return True


def has_index(table, fields):
    for index in table.indexes:
        col_names = {c.name for c in index.columns}
        if set(fields) == col_names:
            return True


def get_stored_obj(session, cls, obj_id=None, stmt=None):
    # Either obj_id or stmt must be provided, but not both
    assert bool(obj_id) ^ (stmt is not None)
    if stmt is None:
        stmt = select(cls).where(cls.id == obj_id)
    return session.execute(stmt).scalar_one()


def get_random_string():
    """Generate unique values to accommodate unique constraints."""
    return str(random.random())
