from sqlalchemy import create_engine, MetaData
from BabyMonitor.model_baby_monitor import create_table_baby_monitor, insert_baby_monitor
from Smartphone.model_smartphone import create_table_smartphone, insert_smartphone
from SmartTv.model_smart_tv import create_table_smart_tv, insert_smart_tv


engine = create_engine('sqlite:///app.db')
meta = MetaData()

bm = create_table_baby_monitor(engine, meta)
smt = create_table_smartphone(engine, meta)
tv = create_table_smart_tv(engine, meta)

for i in range(10):
    insert_baby_monitor(bm, engine)

for i in range(10):
    insert_smartphone(smt, engine)

for i in range(10):
    insert_smart_tv(tv, engine)