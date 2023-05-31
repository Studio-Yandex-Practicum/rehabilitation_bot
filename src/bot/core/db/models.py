from sqlalchemy import Column, Integer, MetaData, String, Table, create_engine


engine = create_engine('sqlite:///sqlite3.db')
engine.connect()

meta = MetaData()

obscene_language = Table(
    'Obscene_language', meta,
    Column('id', Integer, primary_key=True),
    Column('The_forbidden_word', String(50), unique=True)
)
