from sqlalchemy import Table, Column, String, Integer

def create_table_smartphone(engine, meta):
    smartphone = Table(
    'smartphone', meta, 
    Column('id', Integer, primary_key = True, autoincrement=True), 
    Column('notification', String), 
    )
    meta.create_all(engine)
    
    return smartphone

def insert_smartphone(smartphone, engine):
    conn = engine.connect()
    new_data = smartphone.insert().values(notification="Sou uma notificacao")
    conn.execute(new_data)