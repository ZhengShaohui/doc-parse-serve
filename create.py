import sqlite3

db = sqlite3.connect('database.db')
cursor = db.cursor()
cursor.execute(
    '''
    create table class
    (
    id text,
    name text,
    primary key (id)
    )
    '''
)
db.commit()

cursor.execute(
    '''
    create table formulation
    (
    id text,
    class_id text,
    result text,
    primary key (id),
    foreign key (class_id) references class (id)
    )
    '''
)
db.commit()

cursor.execute(
    '''
    create table item
    (
    id text,
    formulation_id text,
    type text not null,
    content text,
    picture text,
    primary key (id),
    foreign key (formulation_id) references formulation (id),
    check (type='text' or type='table')
    )
    '''
)
db.commit()
db.close()
print('数据库建好了')
