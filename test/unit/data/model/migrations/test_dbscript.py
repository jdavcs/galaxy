
class TestDbScript:

    def test_revision(self):

        # call command, make sure it does what? creates a new blank revision for gxy model
        # maybe assert stdout?

        # maybe test exit code and output?
        env = TestEnv()
        env.db = make_db(state1)
        env.dir = tempdir.mkdir()
        env.invoke('db.sh', 'upgrade')
        # assert that db is upgraded?


        pass

        
