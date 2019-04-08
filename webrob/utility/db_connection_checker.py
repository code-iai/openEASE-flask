def got_db_connection(app, db):

    try:
        # TODO: Not sure how secure this is, so maybe check this in the future or change this
        db.engine.execute('SELECT 1')
        return True
    except Exception, e:
        app.logger.info(e.message)
        app.logger.info('Unable to connect to database.')
        return False
