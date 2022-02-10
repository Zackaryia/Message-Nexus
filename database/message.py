from json import dumps, loads
from parser.helper import *
from parser._variables import *
from .file import fileClass

class messageClass:
	def __init__(
		self, current_cursor, message_id, chatroom_id, service, chatroom_type, author_id, 
		timestamp, contents=None, 
		chatroom_type_raw=None, author_name=None, avatar_uuid=None, sender_type=None, sender_type_raw=None, 
		attachments_ids=None, favorited_or_pinned=False,  reactions_str=None, reactions_id=None, 
		embed_id=None, replied_to=None, edited=False, edited_timestamp=None, 
		edited_timestamp_date=None, source_program=None, 
		timestamp_date=None, timestamp_pulled=None, timestamp_imported=None, 
		timestamp_recived=None, other=None, other_parsing_data=None
	):
		self.table_name = "messages"
	
		args = locals()

		args.pop('self')
		args.pop('other_parsing_data')
		
		self.other_parsing_data = other_parsing_data
					
		args.pop('current_cursor')

		self.current_cursor = current_cursor
		for x in args: # Removes a weird glitch with unicode json
			if x == None:
				del args[x]
				continue
			
			args[x] = loads(dumps(args[x]))

		self.values = args
		
		self.values['reference_id'] = generate_reference_string(self.values['service'], reference_TYPE.MESSAGE, self.values['message_id'])
		self.values['chatroom_reference_id'] = generate_reference_string(self.values['service'], self.values['chatroom_type'], self.values['chatroom_id'])
	
	def check_exists(self, cursor):
		cursor.execute(f"""
			SELECT EXISTS(
				SELECT 1 
				FROM {self.table_name} 
				WHERE service=:service AND chatroom_type=:chatroom_type AND chatroom_id=:chatroom_id AND message_id=:message_id
			)
			""", {
			"service": self.values['service'],
			"chatroom_type": self.values['chatroom_type'],
			"chatroom_id": self.values['chatroom_id'],
			"message_id": self.values['message_id']
		})


		if cursor.fetchone()[0]:
			return True
		else:
			return False

	def insert_to_db(self, cursor):
		# Maybe do some smarter version of checking if a message exists in the exact same form to allow for saving edits of a message and other things
		if not self.check_exists(cursor):
			keys = ','.join(self.values.keys())
			values = ':'+',:'.join(self.values.keys())
			
			cursor.execute("INSERT INTO messages ("+keys+") VALUES ("+values+")", self.values)


if __name__ == "__main__":
	a = message(1, 1, 1, 1, 1)