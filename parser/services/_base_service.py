import json_stream
from json import dumps
import time
from parser.helper import *
from parser._variables import *
from database import *
from shutil import copyfile



class base_service:
	def __init__(self, streaming_func, file_location, database_class, message_index=[]):
		self.streaming_func = streaming_func
		self.file_location = file_location
		self.database_class = database_class
		self.message_index = message_index

	def return_message_index(self, streaming_obj, message_index):
		if message_index == None or len(message_index) == 0:
			return streaming_obj
		else:
			index_value = message_index.pop(0)
			return self.return_message_index(streaming_obj[index_value], message_index)

	def get_streaming_func(self):
		pass

	def parse_message(self, message_raw, chatroom_data, current_cursor):
		pass 

	def save_chatroom_data(self, data, current_cursor):
		pass

	def get_chatroom_data(self, streaming_obj, current_cursor):
		pass

	def save_avatar(self):
		pass

	def save_attachments(self):
		pass

	def verify_file(self):
		"""Verifies that the file is in the correct format"""
		pass

	def stream_file(self, yield_message=True):
		with open(self.file_location, 'r') as raw_file:
			streaming_obj = self.streaming_func(raw_file)


			with self.database_class.get_conn() as conn:
				cursor = conn.cursor()
				chatroom_data = self.get_chatroom_data(streaming_obj, cursor)

				for message_raw in self.return_message_index(streaming_obj, self.message_index):
					message_instance = self.parse_message(message_raw, chatroom_data, current_cursor=cursor)

					message_instance.insert_to_db(cursor)


					if yield_message:
						yield message_instance

