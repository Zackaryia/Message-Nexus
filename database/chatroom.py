

from json import dumps, loads
from parser.helper import *
from parser._variables import *
from .file import fileClass

class chatroomClass:
	def __init__(
		self, current_cursor, chatroom_id, service, chatroom_type, 
		chatroom_type_raw=None, description=None, avatar_uuid=None, chatroom_name=None, attachments_uuid=None, 
		source_file=None, source_program=False,  timestamp=False,
		timestamp_date=None, timestamp_pulled=None, timestamp_imported=None, 
		timestamp_recived=None, other=None, other_parsing_data=None
	):
		self.table_name = "chatrooms"

		args = locals()
		args.pop('self')
		args.pop('other_parsing_data')
		
		self.other_parsing_data = other_parsing_data
					
		args.pop('current_cursor')

		self.current_cursor = current_cursor
		for x in args:
			if x == None:
				del args[x]
				continue
			
			args[x] = loads(dumps(args[x])) # Removes a weird glitch with unicode json trash

		self.values = args
		
		self.values['reference_id'] = generate_reference_string(self.values['service'], self.values['chatroom_type'], self.values['chatroom_id'])
	
	def check_exists(self, current_cursor):
		current_cursor.execute(f"""
			SELECT EXISTS(
				SELECT 1 
				FROM {self.table_name} 
				WHERE service=:service AND chatroom_type=:chatroom_type AND chatroom_id=:chatroom_id
			)
			""", {
			"service": self.values['service'],
			"chatroom_type": self.values['chatroom_type'],
			"chatroom_id": self.values['chatroom_id']
		})

		if current_cursor.fetchone()[0]:
			return True
		else:
			return False




	def insert_to_db(self, cursor):
		if not self.check_exists(cursor):
			keys = ','.join(self.values.keys())
			values = ':'+',:'.join(self.values.keys())
			
			cursor.execute("INSERT INTO "+self.table_name+" ("+keys+") VALUES ("+values+")", self.values)


if __name__ == "__main__":
	a = message(1, 1, 1, 1, 1)