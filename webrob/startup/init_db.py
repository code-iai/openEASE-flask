import psycopg2


def init_db(app, db):
    # Automatically create all DB tables in app/app.sqlite file
    # TODO: find better check for postgre-sql connection
    try:
        db.create_all()
        db.session.commit()
    except:
        app.logger.info('Unable to connect to database.')
