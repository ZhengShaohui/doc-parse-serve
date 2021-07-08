import sqlite3
from uuid import uuid4


class SQL:
    __con = sqlite3.connect('database.db', check_same_thread=False)
    __cursor = __con.cursor()

    @classmethod
    def insert_class(cls, name):
        id = uuid4().hex
        cls.__cursor.execute(
            "insert into class (id, name) values ('%s','%s')" % (id, name)
        )
        cls.__con.commit()
        return id

    @classmethod
    def insert_formulation(cls, class_id):
        id = uuid4().hex
        cls.__cursor.execute(
            "insert into formulation (id, class_id) values ('%s', '%s')" % (id, class_id)
        )
        cls.__con.commit()
        return id

    @classmethod
    def insert_item(cls, formulation_id, t, content, picture=''):
        id = uuid4().hex
        cls.__cursor.execute(
            "insert into item (id, formulation_id, type , content, picture) values ('%s', '%s', '%s', '%s', '%s')" % (
            id, formulation_id, t, content, picture)
        )
        cls.__con.commit()
        return id

    @classmethod
    def is_existed(cls, name):
        cls.__cursor.execute('select name from class')
        names = list(map(lambda x:x[0], cls.__cursor.fetchall()))
        if name in names:
            return True
        return False


if __name__ == '__main__':
    SQL.is_existed(123)
