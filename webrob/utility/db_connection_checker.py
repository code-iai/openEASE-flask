def got_db_connection(app, db):
    try:
        db.session.query("1").from_statement("SELECT 1").all()
        return True
    except Exception:
        app.logger.info('Unable to connect to database.')
        return False
