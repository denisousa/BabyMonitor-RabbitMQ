from sqlalchemy import create_engine, MetaData, Table, Column, Integer, Boolean
import sqlalchemy as db


def create_table_baby_monitor(engine, meta):
    baby_monitor_table = Table(
        "baby_monitor",
        meta,
        Column("id", Integer, primary_key=True, autoincrement=True),
        Column("breathing", Boolean),
        Column("time_no_breathing", Integer),
        Column("crying", Boolean),
        Column("sleeping", Boolean),
    )
    meta.create_all(engine)

    return baby_monitor_table


def insert_baby_monitor(bm, engine, data):
    conn = engine.connect()
    query = bm.insert()
    conn.execute(query, data)

def get_data_baby_monitor(bm, engine):
    conn = engine.connect()
    query = db.select([bm])
    return conn.execute(query).fetchall()[-1]