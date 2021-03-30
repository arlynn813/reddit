import sqlite3


# SQL connection decorator to open/close connection and maintain cursor.
def connection_required(commit=False):
    def connection(func):
        def wrapper(*args, **kwargs):
            con = sqlite3.connect('data/database.db')
            cur = con.cursor()
            instruction = func(*args, **kwargs)
            if instruction:
                cur.execute(instruction)
            val = cur.fetchall()
            if commit:
                con.commit()
            con.close()
            return val
        return wrapper
    return connection
