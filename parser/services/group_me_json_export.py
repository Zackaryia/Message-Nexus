from json import load
import os
from database._enum import *
import json_stream
from json import dumps
import json_stream
import time
from ._base_service import *
from pathlib import Path
	

class GROUP_ME_FILE_TYPE(Enum):
	IMAGE = 0
	VIDEO = 1
	FILE = 2
	AVATAR = 3

class group_me_json_export(base_service):
	def __init__(self, file_location):
		if os.path.isdir(os.path.join(Path(self.file_location).parent.resolve(), 'gallery')):
			manifest_data_file_path = os.path.join(Path(self.file_location).parent.resolve(), 'gallery', 'manifest.json')
			with open(manifest_data_file_path, "r") as manifest_data_file:
				self.manifest_data = load(manifest_data_file)
				self.files = os.listdir(os.path.join(self.file_location).parent.resolve(), 'gallery')

		else:
			self.manifest_data = None
			self.files = None


		super().__init__(json_stream.load, file_location, ['messages'])
		# streaming_func

	def file_handler(self, file_url_loc, group_me_file_type, file_type, session, group_id=None):
		referance_id = None
		ext = None
		if group_me_file_type == GROUP_ME_FILE_TYPE.IMAGE:
			referance_id = file_url_loc.split['.'][-1]
			ext = file_url_loc.split['.'][-2]
		elif group_me_file_type == GROUP_ME_FILE_TYPE.VIDEO:
			referance_id = file_url_loc.split("/")[-1].split('.')[0]
			ext = file_url_loc.split("/")[-1].split('.')[-1]
		elif group_me_file_type == GROUP_ME_FILE_TYPE.FILE:
			referance_id = file_url_loc
		elif group_me_file_type == GROUP_ME_FILE_TYPE.AVATAR:
			referance_id = file_url_loc.split('.')[-2]
			ext = file_url_loc.split('.')[-3]

			#######################################################
			# GO TO `group_me_file_dwld.py` FOR HOW TO DWLD FILES #
			#######################################################

		else:
			pass


		if file_url_loc in self.manifest_data:
		#	for file in self.files:
		#		if 
			
			file_name, ext = name, ext
			source_file_path = file_url_loc
			full_file_local = os.path.join(Path(self.file_location).parent.resolve(), file_url_loc)

		
		
		return create_find_update_file(session, name, ext, SERVICES.DISCORD, file_type, name, SOURCE_PROGRAM.DISCORD_DCE_JSON, file_url=file_url, full_file_location=full_file_local, source_file_path=source_file_path)

	def get_chatroom_instance(self, chatroom_data, session):
		if "chat" in chatroom_data:
			chatroom = Query(Chatroom, session=session).filter(Chatroom.chatroom_id == chatroom_data['chat']['last_message']['chat_id'], Chatroom.service == SERVICES.GROUPE_ME).first()

			if chatroom == None:
				chatroom_avatar = self.file_handler(chatroom_data['chat']['other_user']["avatar_url"], OBJECT_TYPE.ICON, session)
				chatroom_avatar.timestamp_imported = datetime.now()

				chatroom = Chatroom(
					avatar_id=chatroom_avatar.reference_id,
					chatroom_id=chatroom_data['chat']['last_message']['chat_id'], 
					service=SERVICES.GROUPE_ME, 
					source_program=SOURCE_PROGRAM.GROUP_ME_DIRECT_DOWNLOAD,
					chatroom_type=CHATROOM_TYPE.DIRECT,
					chatroom_name=chatroom_data['chat']['other_user']['name'],
					timestamp=datetime.fromtimestamp(chatroom_data['chat']['created_at']),
					timestamp_imported=datetime.now()
				)

				session.add(chatroom)
			else:
				pass # Update chatroom to add more data
		
		else:
			chatroom = Query(Chatroom, session=session).filter(Chatroom.chatroom_id == chatroom_data['group_id'], Chatroom.service == SERVICES.GROUPE_ME).first()

			if chatroom == None:
				chatroom_avatar = self.file_handler(chatroom_data["image_url"], OBJECT_TYPE.ICON, session)
				chatroom_avatar.timestamp_imported = datetime.now()

				chatroom = Chatroom(
					avatar_id=chatroom_avatar.reference_id,
					chatroom_id=chatroom_data['group_id'], 
					service=SERVICES.GROUPE_ME, 
					source_program=SOURCE_PROGRAM.GROUP_ME_DIRECT_DOWNLOAD,
					chatroom_type=CHATROOM_TYPE.GROUP_DM,
					chatroom_name=chatroom_data['name'],
					description=chatroom_data['description'],
					timestamp=datetime.fromtimestamp(chatroom_data['chat']['created_at']),
					timestamp_imported=datetime.now()
				)

				session.add(chatroom)
			else:
				pass # Update chatroom to add more data
		

		return chatroom


	def get_chatroom_data(self, streaming_obj):
		chatroom_data_file_path = os.path.join(Path(self.file_location).parent.resolve(), 'conversation.json')
		with open(chatroom_data_file_path, "r") as chatroom_data_file:
			chatroom_data = load(chatroom_data_file)

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
			source_program=SOURCE_PROGRAM.DISCORD_DCE_JSON,
			timestamp_imported=datetime.now()
		)



		if Query(Message, session=session).filter(
			Message.message_id == message.message_id
		).first() == None:
			session.add(message)
		else:
			pass # Update message to be better based on data that only DCE Json exports
		
		return message



class group_me_json_export(base_service):
	def __init__(self, file_location, database_class):
		super().__init__(json_stream.load, file_location, database_class)
		# streaming_func
	

	def get_streaming_func(self, raw_file):
		return json_stream.load(raw_file)
				


	def parse_message(self, message_data, chatroom_data, current_cursor):
		message_data = combine_items(message_data)
		print(dumps(message_data, indent=4))


		if "conversation_id" in message_data.keys():
			chatroom_type = CHATROOM_TYPE.DIRECT # DM
			chatroom_id = message_data['conversation_id']
		else:
			chatroom_type = CHATROOM_TYPE.GROUP_DM # GM
			chatroom_id = message_data['group_id']

		if "platform" in message_data:
			message_platform = message_data['platform']
		else:
			message_platform = None

		"""The message ID converted to epoch has a value after the decimal place so it can be more accurate."""
		if int(groupme_id_to_epoch(message_data['id'])) == message_data['created_at']:
			epoch = groupme_id_to_epoch(message_data['id'])
		else:
			epoch = message_data['created_at']


		return messageClass(
			current_cursor,
			message_id=message_data['id'], 
			chatroom_id=chatroom_id,
			service=SERVICES.GROUPE_ME, 
			chatroom_type=chatroom_type, 
			chatroom_type_raw=message_platform, 
			author_id=message_data['sender_id'],
			sender_type=group_me_sender_type_to_type(message_data['sender_type']),
			sender_type_raw=message_data['sender_type'],
			# avatar url 
			# attachments
			
			author_name=message_data['name'],
			timestamp=epoch,
			contents=message_data['text'],
			source_program=SOURCE_PROGRAM.GROUP_ME_DIRECT_DOWNLOAD,
			other=dumps({"group_me_source_guid": message_data['source_guid']})
		)


		return message_return