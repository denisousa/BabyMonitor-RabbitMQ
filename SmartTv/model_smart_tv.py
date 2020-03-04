from sqlalchemy import Table, Column, String, Integer


def create_table_smart_tv(engine, meta):
    smart_tv_table = Table(
        "smart_tv",
        meta,
        Column("id", Integer, primary_key=True, autoincrement=True),
        Column("command", String),
    )
    meta.create_all(engine)

    return smart_tv_table


def insert_smart_tv(smart_tv, engine):
    conn = engine.connect()
    new_data = smart_tv.insert().values(command="Receive command from Smartphone")
    conn.execute(new_data)
