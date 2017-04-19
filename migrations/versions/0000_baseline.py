#!/usr/bin/env python


def create_table_changelog(conn):
    cursor = conn.cursor()

    query = """
        CREATE TABLE IF NOT EXISTS changelog (
            id serial PRIMARY KEY,
            version VARCHAR(4),
            name VARCHAR(100) UNIQUE,
            applied TIMESTAMP
        );
    """
    params = {}

    cursor.execute(query, params)
    conn.commit()
# _____________________________


def create_table_roles(conn):
    cursor = conn.cursor()

    query = """
        CREATE TABLE IF NOT EXISTS roles (
            id serial PRIMARY KEY,
            name VARCHAR(64) UNIQUE,
            isdefault BOOLEAN DEFAULT FALSE,
            permissions INTEGER
        );
    """
    params = {}

    cursor.execute(query, params)
    conn.commit()
# _____________________________


def create_table_users(conn):

    cursor = conn.cursor()

    query = """
        CREATE TABLE IF NOT EXISTS users (
            id serial PRIMARY KEY,
            social_id VARCHAR(64) NOT NULL UNIQUE,
            nickname VARCHAR(64) NOT NULL,
            email VARCHAR(64) UNIQUE,
            username VARCHAR(64) UNIQUE,
            password_hash VARCHAR(128),
            role_id INTEGER REFERENCES roles(id)
        );
    """
    params = {}

    cursor.execute(query, params)
    conn.commit()
# _____________________________


def drop_table_changelog(conn):
    cursor = conn.cursor()

    query = """
        DROP TABLE IF EXISTS changelog;
    """
    params = {}

    cursor.execute(query, params)
    conn.commit()
# _____________________________


def drop_table_roles(conn):
    cursor = conn.cursor()

    query = """
        DROP TABLE IF EXISTS roles;
    """
    params = {}

    cursor.execute(query, params)
    conn.commit()
# _____________________________


def drop_table_users(conn):
    cursor = conn.cursor()

    query = """
        DROP TABLE IF EXISTS users;
    """
    params = {}

    cursor.execute(query, params)
    conn.commit()
# _____________________________


def upgrade(conn, **kwargs):
    create_table_changelog(conn)
    create_table_roles(conn)
    create_table_users(conn)
# _______________________________


def downgrade(conn):
    drop_table_changelog(conn)
    drop_table_users(conn)
    drop_table_roles(conn)
