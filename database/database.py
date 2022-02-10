import os
from datetime import datetime
import sqlite3
import json


class CONFIG:
	TEMP_DOWNLOAD_FILE_FOR_INFO = True

class database:
	def __init__(self, local_files_dir, copy_source_files_to_local_dir, db_file_name="messages.db"):
		self.local_files_dir = local_files_dir
		self.db_loc = os.path.join(local_files_dir, db_file_name)

		if not os.path.isdir(os.path.join(local_files_dir, 'files')):
			os.mkdir(os.path.join(local_files_dir, 'files'))
			
		if not os.path.isdir(os.path.join(local_files_dir, 'temp')):
			os.mkdir(os.path.join(local_files_dir, 'temp'))
			
		
		if os.path.isfile(self.db_loc):
			return
		
		with self.get_conn() as conn:
			c = conn.cursor()
			with open("database_format.sql") as database_format_raw:
				c.executescript(database_format_raw.read())

			conn.commit()

		with self.get_conn() as conn:
			c = conn.cursor()

			c.executemany("INSERT INTO meta_data VALUES (?, ?)", [
				('local_files_dir', self.local_files_dir),
				('db_file_name', db_file_name),
				('db_loc', self.db_loc),
				('timezone', 'utc'), # NOT IMPLIMENTED YET TODO
			])

			conn.commit()



	def get_conn(self):
		conn = sqlite3.connect(self.db_loc)
		conn.row_factory = sqlite3.Row
		return conn




	def insert_into(
		self, cursor, message_id, service, chatroom_type, author_id, timestamp, contents=None, 
		attachments_id=None, favorited_or_pinned=False, reactions_str=None, reactions_id=None, 
		embed_id=None, replied_to=None, edited=False, edited_timestamp=None, edited_timestamp_date=None,
		source_file=None, source_program=None, timestamp_date=None
	):
	
		args = locals()
		args.pop('self')
		args.pop('cursor')

		keys = ','.join(args.keys())
		values = ':'+',:'.join(args.keys())

		new_args = {}
		for (x, y) in args.items():
			new_args[x] = json.loads(json.dumps(y))
		
		args = new_args

		cursor.execute("INSERT INTO \"main\".\"messages\" ("+keys+") VALUES ("+values+")", args)
