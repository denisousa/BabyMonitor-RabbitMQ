import pika
import random
import sys
import time
sys.path.append('../')
from construct_scenario import *
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, Boolean
import sqlalchemy as db
import threading


class Smartphone(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		self.engine = engine
		self.meta = meta
		self.connection = pika.BlockingConnection(
			pika.ConnectionParameters(host='localhost'))
		self.channel = self.connection.channel()
		self.is_producer = False
		self.is_consumer = False

		self.button_is_pressed = False
		self.is_notification = False
		declare_exchanges_queues(self.channel)

	def run(self):
		if self.is_consumer:
			while self.button_is_pressed:
				print(' [*] Smartphone waiting for messages. To exit press CTRL+C')

				def callback_smartphone(ch, method, properties, body):
					if method.routing_key == routing_key_smartphone:
						print(" [x] Receive Topic: %r | Message: %r" % (method.routing_key, body))
						self.read_message(body)

				self.channel.queue_bind(
					exchange=exchange_baby_monitor, queue=queue_smartphone, routing_key=routing_key_smartphone)
				
				self.channel.basic_consume(
							queue=queue_smartphone, on_message_callback=callback_smartphone, auto_ack=True)

				self.channel.start_consuming()
			
			self.connection.close()

		if self.is_producer and self.button_is_pressed:
			message = 'CONFIRMATION: Notification received!'
			self.channel.basic_publish(exchange=exchange_baby_monitor, routing_key=routing_key_baby_monitor, body=message)
			self.is_notification = False
			print(" [x] Sent Topic: %r | Message: %r" % (routing_key_baby_monitor, message))
			self.button_is_pressed = False

	def read_message(self, message):
		message = str(message)
		if 'NOTIFICATION' in message: 
			data = message.replace('b"NOTIFICATION: ', '')
			data = data.replace('"', '')
			data = eval(data)
			self.is_notification = True

			if not data['breathing']: 
				print(f"Alert: Baby Emma hasn't been breathing for {data['time_no_breathing']} seconds!")
			
			elif not data['crying']:
				print('Alert: Baby Emma is crying.')
		
		else: 
			print("Everything's fine. :)")
	
	def get_data_baby_monitor(self):
		bm = db.Table('baby_monitor', self.meta, autoload=True, autoload_with=self.engine)
		conn = self.engine.connect()
		query = db.select([bm])
		result = conn.execute(query).fetchall()
		if result: 
			return result[-1]
		else: 
			return 0 