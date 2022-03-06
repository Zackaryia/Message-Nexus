import json_stream
from json import dumps
import time
from database._enum import *
from database import *
from shutil import copyfile
from sqlalchemy.orm import Session, Query
from database._utility import combine_items


class base_service:
	def __init__(self, file_location, keys):
		self.file_location = file_location
		self.keys = keys

	def get_streaming_iterable(self, streaming_obj):
		pass

	def parse_message(self, message_raw, chatroom_data, session):
		pass 

	def get_chatroom_instance(self, chatroom_data, session):
		pass

	def get_chatroom_data(self, streaming_obj):
		pass


	def verify_file(self):
		"""Verifies that the file is in the correct format"""
		pass

	def stream_file(self, engine, yield_message=True):
		with open(self.file_location, 'r') as raw_file:
			with Session(engine) as session, session.begin():
				streaming_obj = self.streaming_func(raw_file)

				chatroom_data = self.get_chatroom_data(streaming_obj)
				chatroom_instance = self.get_chatroom_instance(chatroom_data, session)

				for message_raw in self.get_streaming_iterable(streaming_obj):
					message = self.parse_message(message_raw, chatroom_data, session=session)

					if yield_message:
						yield message
			

