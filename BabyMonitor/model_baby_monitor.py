import pika
from time import sleep
import sys
from generate_data import *
sys.path.append('../')
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, Boolean, String
from construct_scenario import *
import sqlalchemy as db
import threading

semaphore = threading.Semaphore()
notif_confirm = [False, False]

class BabyMonitorConsumer(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		self.connection = pika.BlockingConnection(
			pika.ConnectionParameters(host='localhost'))
		self.channel = self.connection.channel()
		
		self.channel.exchange_declare(exchange=exchange_baby_monitor, exchange_type="direct")
		
		self.queue = self.channel.queue_declare(queue_baby_monitor)
		
		self.channel.queue_bind(
			exchange=exchange_baby_monitor, queue=queue_baby_monitor, routing_key=routing_key_baby_monitor)
		
		self.button_is_pressed = False

	def run(self):
		global semaphore, notif_confirm

		#print("thread que recebeu: ", threading.get_ident())
		while self.button_is_pressed:
			print(' [*] BabyMonitor waiting for messages. To exit press CTRL+C')

			def callback_baby_monitor(ch, method, properties, body):
				
				if notif_confirm[0]:
					print(" [BabyMonitor] Receive Topic: %r | Message: %r \n" % (method.routing_key, body))
					semaphore.acquire()
					notif_confirm[1] = True
					semaphore.release()

			self.channel.basic_consume(
				queue=queue_baby_monitor, on_message_callback=callback_baby_monitor, auto_ack=True)
			self.channel.start_consuming()
		
		self.connection.close()
			
class BabyMonitorProducer(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		self.engine = engine
		self.meta = meta
		self.connection = pika.BlockingConnection(
			pika.ConnectionParameters(host='localhost'))
		self.channel = self.connection.channel()
		
		self.channel.exchange_declare(exchange=exchange_baby_monitor, exchange_type="direct")

		self.data = None
		self.bm = self.create_table_baby_monitor()
		self.button_is_pressed = False

		self.message = None

	def run(self):
		global semaphore, notif_confirm

		while self.button_is_pressed:
			if notif_confirm[0]:
				if notif_confirm[1]:
					data_from_baby(self, -1)
					semaphore.acquire()
					notif_confirm[0] = False
					notif_confirm[1] = False
					semaphore.release()
				else: 
					data_from_baby(self, 1)
			else: 
				data_from_baby(self, 0)

			self.data = self.get_data_baby_monitor()
			keys = ('id', 'breathing', 'time_no_breathing', 'crying', 'sleeping')
			data = dict(zip(keys, self.data))
			message = str(data)
			
			if data['crying']:
				message = 'NOTIFICATION: Baby Emma is crying.' 
				semaphore.acquire()
				notif_confirm[0] = True
				semaphore.release()

			elif data['time_no_breathing'] >= 3:
				message = f"NOTIFICATION: Baby Emma hasn't been breathing for {data['time_no_breathing']} seconds."
				semaphore.acquire()
				notif_confirm[0] = True
				semaphore.release()

			else: 
				message = 'STATUS: ' + message 

			self.channel.basic_publish(exchange=exchange_baby_monitor, routing_key=routing_key_smartphone, body=message)

			print(" [BabyMonitor] Sent Topic: %r | Message: %r \n" % (routing_key_smartphone, message))
			
			self.message = message
			#sleep(1)

	def create_table_baby_monitor(self):
		try:
			baby_monitor_table = Table(
				"baby_monitor",
				self.meta,
				Column("id", Integer, primary_key=True, autoincrement=True),
				Column("breathing", Boolean),
				Column("time_no_breathing", Integer),
				Column("crying", Boolean),
				Column("sleeping", Boolean),
			)
			self.meta.create_all(self.engine)

			return baby_monitor_table
		except:
			connection = self.engine.connect()
			bm = db.Table('baby_monitor', self.meta, autoload=True, autoload_with=self.engine)
			return bm

	def insert_baby_monitor(self, data):
		try:
			conn = self.engine.connect()
			query = self.bm.insert()
			conn.execute(query, data)
		except:
			conn = self.engine.connect()
			#conn.rollback()

	def get_data_baby_monitor(self):
		conn = self.engine.connect()
		query = db.select([self.bm])
		result = conn.execute(query).fetchall()

		if result: 
			return result[-1]
		else: 
			return 0 
