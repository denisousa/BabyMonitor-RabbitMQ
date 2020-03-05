from sqlalchemy import create_engine, MetaData, Table, Column, Integer, Boolean
import generate_data as gd

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


def insert_baby_monitor(baby_monitor, engine):
    conn = engine.connect()
    '''new_data = baby_monitor.insert().values(
        breathing=True, time_no_breathing=0, crying=True, sleeping=False
    )'''
    query = baby_monitor.insert()
    new_data = [gd.data_from_baby(0)]
    conn.execute(query, new_data)
