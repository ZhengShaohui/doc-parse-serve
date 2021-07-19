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
    def insert_formulation(cls, class_id, result=''):
        id = uuid4().hex
        cls.__cursor.execute(
            "insert into formulation (id, class_id, result ) values ('%s', '%s', '%s')" % (id, class_id, result)
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
        names = list(map(lambda x: x[0], cls.__cursor.fetchall()))
        if name in names:
            return True
        return False

    @classmethod
    def get_all_class(cls):
        cls.__cursor.execute('select * from class')
        res = cls.__cursor.fetchall()
        return res

    @classmethod
    def get_all_forms(cls, class_id):
        cls.__cursor.execute("select * from formulation where class_id='%s'" % class_id)
        res = cls.__cursor.fetchall()
        return res

    @classmethod
    def get_items(cls, formulation_id):
        cls.__cursor.execute("select id, type, content, picture from item where formulation_id='%s'" % formulation_id)
        res = cls.__cursor.fetchall()
        return res

    @classmethod
    def update_item(cls, item_id, content):
        cls.__cursor.execute("update item set content=? where id=?", (content, item_id))
        cls.__con.commit()

    @classmethod
    def save_result(cls, formulation_id, result):
        cls.__cursor.execute("update formulation set result=? where id=?", (result, formulation_id))
        cls.__con.commit()

    @classmethod
    def get_result(cls, formulation_id):
        cls.__cursor.execute("select result from formulation where id=?", (formulation_id,))
        res = cls.__cursor.fetchone()
        return res[0]


if __name__ == '__main__':
    # res = SQL.get_all_forms('d794517d8a734e0a95df80a21913ed34')
    # print(SQL.get_items(res[0][0]))
    pass