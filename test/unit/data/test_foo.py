from galaxy import model as m

from galaxy.util.hash_util import md5_hash_str

def make_User(**kwd):
    # TODO ensure required args are passed or generated
    if "username" not in kwd:
        kwd["username"] = "abc"
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

def test_Page():
    u = make_User()
    p = m.Page(user=u)
    assert p.username is not None and p.username == u.username
    assert p.email_hash is not None and p.email_hash == md5_hash_str(u.email)

def test_User():
    email, password = 'a', 'b'
    u = m.User(email=email, password=password)
    # email, password, active




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
