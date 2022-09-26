import psycopg2


def get_connection():
    return psycopg2.connect(
        user='postgres',
        password='3597',
        database='postgres'
    )