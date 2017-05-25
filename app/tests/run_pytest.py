from app.dbmodels.query_admin import DBAdmin


def resetdb(conf):
    dba = DBAdmin(conf=conf)
    conn = dba.connectdb(conf.DB_CONN_URI_ADMIN)

    try:
        dba.dbdrop()
        dba.createdb()
    finally:
        conn.close()
