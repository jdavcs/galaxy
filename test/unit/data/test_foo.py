import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.orm import registry
from galaxy import model as m

from galaxy.util.hash_util import md5_hash_str


mapper_registry = registry()


def initialize_model(mapper_registry, engine):
    mapper_registry.metadata.create_all(engine)

@pytest.fixture(scope="module")
def engine():
    db_uri = "sqlite:///:memory:"
    return create_engine(db_uri)

@pytest.fixture(scope="module")
def init_model(engine):
    """Create model objects in the engine's database."""
    # Must use the same engine as the session fixture used by this module.
    initialize_model(mapper_registry, engine)

@pytest.fixture
def session(init_model, engine):
    with Session(engine) as s:
        yield s


def make_Foo(**kwd):
    if "a" not in kwd:
        kwd["a"] = make_A()
    if "b" not in kwd:
        kwd["b"] = random_str()
    if "c" not in kwd:
        kwd["c"] = random_int()
    foo = model.Foo(**kwd)
    session.add(foo)  # session is a fixture available on the class
    session.flush()   # we don't need to persist, so flush should be fine
    return foo  # return fully constructed instance of Foo

def test_bar():
    myfoo = make_Foo()
    bar = Bar(foo=myfoo)
    session.add(bar)   # session is a fixture available on the class 
    session.flush()
    assert bar.x == "value of x"






def make_User(**kwd):
    # TODO ensure required args are passed or generated
    if "email" not in kwd:
        kwd["email"] = "a"
    if "username" not in kwd:
        kwd["username"] = "a"
    u = m.User(**kwd)
    return u

def make_History():
    h = m.History()
    return h


def make_Dataset():
    #h = make_History()
    #hda = m.HistoryDatasetAssociation(history=h, create_dataset=True)
#    hda = m.HistoryDatasetAssociation()
#    return hda.dataset
    return m.Dataset()

def make_DatasetPermissions():
    a = "action"
    d = make_Dataset()
    dp = m.DatasetPermissions(action=a, dataset=d)
    return dp


def make_Role():
    return m.Role()

def make_Page():
    u = make_User()
    return m.Page(user=u)


class TestPage:

    def test_constructor(self):
        p = m.Page(user=make_User())
        assert p.user is not None

    def test_properties(self):
        u = make_User()
        p = m.Page(user=u)
        assert p.username is not None and p.username == u.username
        assert p.email_hash is not None and p.email_hash == md5_hash_str(u.email)

    def test_to_dict(self):
        p = m.Page(user=make_User())
        r1 = m.PageRevision(p)
        r2 = m.PageRevision(p)
        # commit
        # verify to_dict

    def test_db(self, session):
        p = m.Page(user=make_User())
        #session = get_session()
        #session.add(p)
        #session.commit()




# use a module-scoped fixture to create and init a db. Then reuse it.
def get_session():
    connection_url = "sqlite:///"
    engine = create_engine(connection_url, isolation_level="AUTOCOMMIT")

    return session

class TestPageRevision:
    def test_constructor(self):
        r = m.PageRevision(page=make_Page())
        assert r.page is not None

    def test_to_dict(self):
        r = m.PageRevision(page=make_Page())
        # must commit
        foo = r.to_dict()
        # test added vals


class TestUser:
    def test_constructor(self):
        u = m.User(email='foo', username='foo')
        assert u.email is not None
        assert u.password is not None
        assert u.active is not None
        assert u.username is not None  # because must be unique




def ____test_dataset_action_tuples(self):
    # but do you even need a clean database????
#    with clean_database():
    r = make_Role()
    c = make_DatasetCollection()
    hda1 = make_HistoryDatasetAssociaiont()
    hda2 = make_HistoryDatasetAssociaiont()
    d = hda1.dataset

    make_DatasetPermissions(action="action1", dataset=d, role=r)
    make_DatasetPermissions(action="action2", dataset=d, role=r)

    make_DatasetCollectionElement(collection=c1, element=hda1)
    make_DatasetCollectionElement(collection=c1, element=hda2)
    
    assert len(c.dataset_action_tuples) == 2
    assert ("action1", r.id) in c.dataset_action_tuples
    assert ("action2", r.id) in c.dataset_action_tuples

    #c.dataset_action_tuples
