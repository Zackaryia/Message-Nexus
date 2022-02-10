from json import load
import os
from parser.helper import *
from parser._variables import *
import json_stream
from json import dumps
from database.message import messageClass
import json_stream
import time
from ._base_service import *

	



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
			timestamp_date=epoch_to_datetime(epoch),
			contents=message_data['text'],
			source_program=SOURCE_PROGRAM.GROUP_ME_DIRECT_DOWNLOAD,
			other=dumps({"group_me_source_guid": message_data['source_guid']})
		)


		return message_return