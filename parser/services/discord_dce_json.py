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
		self.SERVICE = SERVICES.DISCORD
		self.SOURCE_PROGRAM = SOURCE_PROGRAM.DISCORD_DCE_JSON
		# streaming_func

	def get_streaming_func(self, raw_file):
		return json_stream.load(raw_file)

	def file_handler(self, file_url_loc, file_type, session):
		FIVE_CHAR_HASH = None
		name, ext = file_url_loc.split('/')[-1].split('.')
		ext = ext.split('?')[0]
		file_url, full_file_location, source_file_path = None, None, None

		if file_url_loc.startswith("https://") or file_url_loc.startswith("http://"):
			file_url = file_url_loc 
			referance_id = name
		else:
			referance_id, FIVE_CHAR_HASH = name.replace("a_", '').split('-')
			source_file_path = file_url_loc
			full_file_location = os.path.join(Path(self.file_location).parent.resolve(), file_url_loc)


		file_inst = Query(File, session=session).filter(
			File.reference_id == referance_id,
			File.file_type == file_type,
			File.source_program == self.SOURCE_PROGRAM
		).first()

		if file_url != None and file_inst == None:
			url_file_hash, _ = get_url_file_hash_and_size(file_url, save_file=CONFIG.BUF_SIZE)

			file_inst = find_file(session, get_url_hash(file_url), url_file_hash)
		else:
			file_hash, _ = get_file_hash_and_size(full_file_location)
			file_inst = find_file(session, None, file_hash)

		# Make avatar if it was not found
		if file_inst == None: 
			file_inst = File(
				reference_id = referance_id,
				service = self.SERVICE,
				file_type = file_type,
				source_program = self.SOURCE_PROGRAM,
				timestamp_imported = datetime.now(),
			)
			
		# Update file with new information
		if file_url != None:
			file_inst.insert_url(file_url, file_name, ext, referance_id)
		if full_file_location != None:
			file_inst.insert_file_path(full_file_location, source_file_path, referance_id, name, ext)
			
		file_inst.other[self.SOURCE_PROGRAM.name+"_5_CHAR_HASH"] = FIVE_CHAR_HASH

		return file_inst

	def get_chatroom_instance(self, chatroom_data, session):
		chatroom = Query(Chatroom, session=session).filter(Chatroom.chatroom_id == chatroom_data['channel']['id'], Chatroom.service == self.SERVICE).first()
		
		if chatroom == None:
			chatroom_avatar = self.file_handler(chatroom_data["guild"]["iconUrl"], OBJECT_TYPE.ICON, session)
			chatroom_avatar.timestamp_imported = datetime.now()
			chatroom_avatar.parrent_type = OBJECT_TYPE.CHATROOM
			chatroom_avatar.parrent_id = chatroom_data['guild']['id']

			chatroom = Chatroom(
				avatar_id=chatroom_avatar.reference_id,
				chatroom_id=chatroom_data['channel']['id'], 
				service=self.SERVICE, 
				source_program=self.SOURCE_PROGRAM,
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

		session.add(avatar_inst)
		session.flush()
		session.refresh(avatar_inst) # Adds the avatar id to the avatar object avatar id

		if epoch_edited_time != None:
			epoch_edited_time = datetime.fromtimestamp(epoch_edited_time)

		message = Message(
			message_id=message_data['id'], 
			chatroom_id=chatroom_data["channel"]["id"],
			service=self.SERVICE, 
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
			source_program=self.SOURCE_PROGRAM,
			timestamp_imported=datetime.now()
		)



		if Query(Message, session=session).filter(
			Message.message_id == message.message_id
		).first() == None:
			session.add(message)
		else:
			pass # Update message to be better based on data that only DCE Json exports
		
		return message
