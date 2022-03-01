from ._base_service import *
import json_stream
from json import dumps, loads
import time
from database._helper import *
from database._enum import *
from database._utility import *
from database import *
import requests
import random
import logging
from pathlib import Path
import os
import shutil

from database.file import *
from datetime import datetime
from enum import Enum 

logging.basicConfig(format='%(asctime)s:%(levelname)s - %(message)s', level=logging.INFO)

logging.warn("test")



class discord_dce_json(base_service):
	def __init__(self, file_location):
		super().__init__(json_stream.load, file_location, ['messages'])
		# streaming_func

	def get_streaming_func(self, raw_file):
		return json_stream.load(raw_file)

	def file_handler(self, file_url_loc, file_type, session):
		name, ext = file_url_loc.split('/')[-1].split('.')
		ext = ext.split('?')[0]
		file_url, full_file_local, source_file_path = None, None, None

		if file_url_loc.startswith("https://") or file_url_loc.startswith("http://"):
			file_url = file_url_loc 
		else:
			
			file_name, ext = name, ext
			source_file_path = file_url_loc
			full_file_local = os.path.join(Path(self.file_location).parent.resolve(), file_url_loc)

		
		
		return create_find_update_file(session, name, ext, SERVICES.DISCORD, file_type, name, SOURCE_PROGRAM.DISCORD_CHAT_EXPORTER, file_url=file_url, full_file_location=full_file_local, source_file_path=source_file_path)

	def get_chatroom_instance(self, chatroom_data, session):
		chatroom = Query(Chatroom, session=session).filter(Chatroom.chatroom_id == chatroom_data['channel']['id'], Chatroom.service == SERVICES.GROUPE_ME).first()

		if chatroom == None:
			chatroom_avatar = self.file_handler(chatroom_data["guild"]["iconUrl"], OBJECT_TYPE.ICON, session)
			chatroom_avatar.timestamp_imported = datetime.now()
			chatroom_avatar.parrent_type = OBJECT_TYPE.CHATROOM
			chatroom_avatar.parrent_id = chatroom_data['guild']['id']

			chatroom = Chatroom(
				avatar_id=chatroom_avatar.reference_id,
				chatroom_id=chatroom_data['channel']['id'], 
				service=SERVICES.DISCORD, 
				source_program=SOURCE_PROGRAM.DISCORD_CHAT_EXPORTER,
				chatroom_type=chatroom_data['type'],
				chatroom_type_raw=chatroom_data['raw_type'],
				chatroom_name=chatroom_data['channel']['name'],
				description=chatroom_data['channel']['topic'],
				timestamp_imported=datetime.now()
			)

			session.add(chatroom)
		else:
			pass # Update chatroom to add more data

		return chatroom





	def get_chatroom_data(self, streaming_obj):
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

		return chatroom_data


	def parse_message(self, message_data, chatroom_data, session):
		message_data = loads(dumps((combine_items(message_data))))
		print(dumps(message_data, indent=4))

		#print(message_data)
		epoch_time = discord_datetime_to_epoch(message_data['timestamp'])
		
		epoch_edited_time = None
		if message_data['timestampEdited'] != None:
			epoch_edited_time = discord_datetime_to_epoch(message_data['timestampEdited'])

		author_name = message_data['author']['name']+"#"+message_data['author']['discriminator']

		
		avatar_inst = self.file_handler(message_data['author']['avatarUrl'], OBJECT_TYPE.AVATAR, session)
		
		avatar_inst.parrent_type = OBJECT_TYPE.USER
		avatar_inst.parrent_id = message_data['author']['id']
		avatar_inst.timestamp_imported = datetime.now()

		session.add(avatar_inst)
		session.flush()
		session.refresh(avatar_inst) # Adds the avatar id to the avatar object avatar id

		if epoch_edited_time != None:
			epoch_edited_time = datetime.fromtimestamp(epoch_edited_time)

		message = Message(
			message_id=message_data['id'], 
			chatroom_id=chatroom_data["channel"]["id"],
			service=SERVICES.DISCORD, 
			chatroom_type=chatroom_data['type'], 
			author_id=message_data['author']['id'],
			author_name=author_name,
			# author pfp
			# attachments
			avatar_id=avatar_inst.reference_id,
			timestamp=datetime.fromtimestamp(epoch_time),
			contents=message_data['content'],
			favorited_or_pinned=message_data['isPinned'],
			edited_timestamp=epoch_edited_time,
			source_program=SOURCE_PROGRAM.DISCORD_CHAT_EXPORTER,
			timestamp_imported=datetime.now()
		)



		if Query(Message, session=session).filter(
			Message.message_id == message.message_id
		).first() == None:
			session.add(message)
		else:
			pass # Update message to be better based on data that only DCE Json exports
		
		return message
