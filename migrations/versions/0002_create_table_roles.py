
def upgrade(self):
    """
    """

    query = """
        CREATE TABLE IF NOT EXISTS roles (
            id serial PRIMARY KEY,
            name VARCHAR(64) UNIQUE,
            isdefault BOOLEAN DEFAULT FALSE,
            permissions INTEGER
        );
    """
    params = {}

    self.cur.execute(query, params)
    self.conn.commit()
# _____________________________
