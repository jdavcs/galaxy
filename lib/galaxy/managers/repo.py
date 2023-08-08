#def get_user_by_username(app, username):
#    """Get a user from the database by username."""
#    sa_session = app.model.session
#    try:
#        user = sa_session.query(app.model.User).filter(app.model.User.table.c.username == username).one()
#        return user
#    except Exception:
#        return None
