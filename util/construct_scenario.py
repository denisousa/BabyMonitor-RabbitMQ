from sqlalchemy import create_engine, MetaData

engine = create_engine("sqlite:///app.db")
meta = MetaData()

routing_key_baby_monitor = "baby_monitor_route"
routing_key_smart_tv = "smart_tv_route"
routing_key_smartphone = "smartphone_route"
queue_baby_monitor = "queue_baby_monitor"
queue_smart_tv = "queue_smart_tv"
queue_smartphone = "queue_smartphone"
exchange = "exchange_baby_monitor"