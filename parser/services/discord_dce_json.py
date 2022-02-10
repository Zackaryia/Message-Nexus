from ._base_service import *
import json_stream
from json import dumps, loads
import time
from parser.helper import *
from parser._variables import *
from database import *
import requests
import random
import logging
from pathlib import Path
import os
import shutil

logging.basicConfig(format='%(asctime)s:%(levelname)s - %(message)s', level=logging.INFO)

logging.warn("test")

class discord_dce_json(base_service):
	def __init__(self, file_location, database_class):
		super().__init__(json_stream.load, file_location, database_class, ['messages'])
		# streaming_func

	def get_streaming_func(self, raw_file):
		return json_stream.load(raw_file)

	def save_chatroom_data(self, data, current_cursor):
		chatroomClass(
			current_cursor, 
			data['channel']['id'], 
			SERVICES.DISCORD, 
			data['type'],
			chatroom_type_raw=data['raw_type'],
			chatroom_name=data['channel']['name'],
			description=data['channel']['topic'],

		).insert_to_db(current_cursor)

	def get_chatroom_data(self, streaming_obj, current_cursor):
		print(streaming_obj)

		chatroom_data = {
					"guild": combine_items(streaming_obj['guild']),
					"channel": combine_items(streaming_obj['channel']),
					"dateRange": combine_items(streaming_obj['dateRange'])
				}

		# Gets discord chat type
		test_chatroom_type = str(chatroom_data['channel']['type'])
		chatroom_data['raw_type'] = test_chatroom_type

		if test_chatroom_type in DISCORD_DCE_CHAT_TO_DISCORD_CHATROOM_TYPE.keys():
			chatroom_type = DISCORD_CHATROOM_TYPE_TO_CHATROOM_TYPE[DISCORD_DCE_CHAT_TO_DISCORD_CHATROOM_TYPE[test_chatroom_type]]
		elif test_chatroom_type in [str(x) for x in DISCORD_CHATROOM_TYPE_TO_CHATROOM_TYPE.keys()]:
			chatroom_type = DISCORD_CHATROOM_TYPE_TO_CHATROOM_TYPE[int(test_chatroom_type)]    
		elif test_chatroom_type in CHATROOM_TYPE.CHATROOM_TYPE_LIST:
			chatroom_type = test_chatroom_type
		else:
			chatroom_type = CHATROOM_TYPE.OTHER

		chatroom_data['type'] = chatroom_type

		self.save_chatroom_data(chatroom_data, current_cursor)

		return chatroom_data


	def parse_message(self, message_data, chatroom_data, current_cursor):
		message_data = loads(dumps((combine_items(message_data))))
		print(dumps(message_data, indent=4))

		#print(message_data)
		epoch_time = discord_datetime_to_epoch(message_data['timestamp'])
		
		epoch_edited_time = None
		edited = False
		if message_data['timestampEdited'] != None:
			edited = True
			epoch_edited_time = discord_datetime_to_epoch(message_data['timestampEdited'])

		author_name = message_data['author']['name']+"#"+message_data['author']['discriminator']

		print('aasas')
		# TODO if avatar exists only fill in details that may be inacurate when first downloaded. IE replace url hash with the full url hash
		if message_data['author']['avatarUrl'].startswith("https://") or message_data['author']['avatarUrl'].startswith("http://"):

			url_hash = hash_obj(message_data['author']['avatarUrl'].encode('utf-8'))
			
			file_hash = None
			file_size = None

			if CONFIG.TEMP_DOWNLOAD_FILE_FOR_INFO:
				myfile = requests.get(message_data['author']['avatarUrl'])
			
				file_hash = hash_obj(myfile.content)
				file_size = print(len(myfile.content))

			print(message_data['author']['avatarUrl'])
			avatar_data = {
				"raw_source_file_location_local": None,
				"full_source_file_location_local": None,
				"source_file_location_remote": message_data['author']['avatarUrl'],
				"reference_id": message_data['author']['avatarUrl'].split('/')[-1].split('.')[0].rpartition('-')[0],
				"file_name": message_data['author']['avatarUrl'].split('/')[-1].split('.')[0].rpartition('-')[0],
				"file_ext": message_data['author']['avatarUrl'].split('/')[-1].split('.')[1],
				"url_hash": url_hash,

				"local_location": None,
				"file_hash": file_hash,
				"file_size": file_size,
				"other": None,
			}
		
		else:

			file_name, file_ext = Path(message_data['author']['avatarUrl']).stem.split('.')[0], Path(message_data['author']['avatarUrl']).suffix

			with open(os.path.join(Path(self.file_location).parent.resolve(), message_data['author']['avatarUrl']), 'rb') as file_obj:
				file_hash = hash_obj(file_obj)

			full_source_file_location_local = os.path.join(Path(self.file_location).parent.resolve(), message_data['author']['avatarUrl'])
			local_location = os.path.join(self.database_class.local_files_dir, "files", file_hash)

			file_size = Path(os.path.join(Path(self.file_location).parent.resolve(), message_data['author']['avatarUrl'])).stat().st_size

			shutil.copy(full_source_file_location_local, local_location)

			avatar_data = {
				"raw_source_file_location_local": message_data['author']['avatarUrl'],
				"full_source_file_location_local": full_source_file_location_local,
				"source_file_location_remote": None,
				"reference_id": file_name.rpartition('-')[0],
				"file_name": file_name.rpartition('-')[0],
				"file_ext": file_ext,
				"url_hash": None,
				"other": {"first_6_url_hash_discord": file_name.rpartition('-')[2]},
				"local_location": local_location,
				"file_hash": file_hash,
				"file_size": file_size
			}

		avatar = fileClass(
			service=SERVICES.DISCORD,
			local_location=avatar_data['local_location'],
					
			raw_source_file_location_local=avatar_data['raw_source_file_location_local'],
			full_source_file_location_local=avatar_data['full_source_file_location_local'],
			source_file_location_remote=avatar_data['source_file_location_remote'],
			source_file_name=message_data['author']['avatarUrl'].split('/')[-1].split('.')[0],
			source_file_ext=message_data['author']['avatarUrl'].split('.')[1],
			
			author_id=message_data['author']['id'],
			reference_id=message_data['author']['avatarUrl'].split('/')[-1].split('.')[0],
			file_type=FILE_TYPE.AVATAR,
			#original_file_name(48charmax)-source_url_hash(5char).extension
			output_file_name=avatar_data['file_hash'],
			url_hash=avatar_data['url_hash'],
			file_hash=avatar_data['file_hash'],
			file_size=avatar_data['file_size'],
			source_program=SOURCE_PROGRAM.DISCORD_CHAT_EXPORTER,
			timestamp=None,
			timestamp_date=None,
			timestamp_pulled=None,
			timestamp_imported=None,
			timestamp_recived=None,
			other=avatar_data['other']
		)
		
		avatar.get_file_or_insert(self.database_class, current_cursor)
		



		message_return = messageClass(
			current_cursor=current_cursor,
			message_id=message_data['id'], 
			chatroom_id=chatroom_data["channel"]["id"],
			service=SERVICES.DISCORD, 
			chatroom_type=chatroom_data['type'], 
			author_id=message_data['author']['id'],
			author_name=author_name,
			# author pfp
			# attachments
			avatar_uuid=avatar.values['file_uuid'],
			timestamp=epoch_time,
			timestamp_date=message_data['timestamp'],
			contents=message_data['content'],
			favorited_or_pinned=message_data['isPinned'],
			edited=edited,
			edited_timestamp=epoch_edited_time,
			edited_timestamp_date=message_data['timestampEdited'],
			source_program=SOURCE_PROGRAM.DISCORD_CHAT_EXPORTER
		)
		
		return message_return