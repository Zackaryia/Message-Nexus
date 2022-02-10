from uuid import uuid4
from json import dumps, loads
from parser.helper import *
from parser._variables import *
import requests, os
from random import randint
import shutil
import hashlib
from pathlib import Path


class fileClass:
	def __init__(self, 	service,
	local_location=None, raw_source_file_location_local=None, full_source_file_location_local=None,
	source_file_location_remote=None, source_file_name=None, source_file_ext=None, file_type=None,
	output_file_name=None, author_id=None, chatroom_id=None, reference_id=None, reference_name=None, 
	url_hash=None, file_hash=None, file_size=None, source_program=None, timestamp=None, timestamp_date=None, 
	timestamp_pulled=None, timestamp_imported=None, timestamp_recived=None, other=None, file_uuid=None
):
		if file_uuid == None:
			file_uuid = uuid4().hex

		args = locals()
		args.pop('self')

		for x in args: # Removes a weird glitch with unicode json
			args[x] = loads(dumps(args[x]))

		self.values = args

		self.table_name = "files"

		

		# Will add the source_file_hash(16chars) if the file gets downloaded and if the 



		self.values = args

	def create(self, search_crieteria, cursor):
		search_filter = ','.join([f"{key}=:{key}" for value in search_crieteria.keys()])

		cursor.execute(f"SELECT FROM {self.table_name} WHERE "+search_filter, search_crieteria)
		cursor.fetchone()

	def insert_file(self, database_class, cursor):
		if 'raw_source_file_location_local' not in self.values:
			self.values['raw_source_file_location_local'] = None
		if 'source_file_location_remote' not in self.values:
			self.values['source_file_location_remote'] = None

		cursor.execute(
			f"SELECT EXISTS(SELECT 1 FROM {self.table_name} WHERE raw_source_file_location_local=? OR source_file_location_remote=? LIMIT 1)", 
			(self.values['raw_source_file_location_local'], self.values['source_file_location_remote'])
		)

		x = cursor.fetchone()[0]

		print(x)
		if x == 1: # If file exists
			return
		

		keys = ','.join(self.values.keys())
		values = ':'+',:'.join(self.values.keys())
		print(self.values)
		cursor.execute(f"INSERT INTO {self.table_name} ("+keys+") VALUES ("+values+")", self.values)


	def get_file_or_insert(self, database_class, cursor):
		if 'raw_source_file_location_local' not in self.values:
			self.values['raw_source_file_location_local'] = None
		if 'source_file_location_remote' not in self.values:
			self.values['source_file_location_remote'] = None

		cursor.execute(
			f"SELECT * FROM {self.table_name} WHERE raw_source_file_location_local=? OR source_file_location_remote=? LIMIT 1", 
			(self.values['raw_source_file_location_local'], self.values['source_file_location_remote'])
		)

		file_instance = cursor.fetchall()

		print(file_instance)
		if file_instance == None or file_instance == []: # If file exists
			self.insert_file(database_class, cursor)
			return
		else:
			file_instance = file_instance[0]
			file_instance = [file_instance[i] for i in range(len(file_instance))]
			print(file_instance)
			cursor.execute(f"PRAGMA table_info({self.table_name})")

			headers = [i[1] for i in cursor.fetchall()]

			print(headers)
			x = {headers[i]: file_instance[i] for i in range(len(headers))}
			print("______________#$@$@#$$")
			print(x)
			self.values = x
			print(self.values)
			return

		


if __name__ == "__main__":
	a = message(1, 1, 1, 1, 1)