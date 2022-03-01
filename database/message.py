from sqlalchemy import Column
import uuid
from database.file import File
from database._enum import *
from database._utility import gen_uuid, Base
from sqlalchemy.types import Integer, String, Float, Boolean, DateTime, Enum, Text, JSON


class Message(Base):
	__tablename__ = 'message'

	id = Column(String, primary_key=True, default=gen_uuid, unique=True, nullable=False)

	message_id = Column(String, unique=True, nullable=False)
	chatroom_id = Column(String, nullable=False)
	author_id = Column(String)
	embed_id = Column(String)
	reactions_id = Column(String)
	avatar_id = Column(String, nullable=False)

	attachments_ids = Column(String)

	author_name = Column(String, nullable=False)
	contents = Column(Text, nullable=False)

	service = Column(Enum(SERVICES), nullable=False) # Determined by helper.py in parser
	source_program = Column(Enum(SOURCE_PROGRAM)) # Program that retrived the message (_variables.py)
	replied_to = Column(String)

	chatroom_type = Column(Enum(CHATROOM_TYPE)) # The type of chat room (group dm, dm, channel, etc) Determined by helper.py in parser
	chatroom_type_raw = Column(String) # If availible the raw format of the sender's type

	#message_type = Column(Enum(message_type)) # Determined by helper.py in parser
	message_type_raw = Column(String) # Directly from the service

	sender_type = Column(Enum(SENDER_TYPE))
	sender_type_raw = Column(String)
	favorited_or_pinned = Column(Boolean)
	reactions_str = Column(String) # 

	edited_timestamp = Column(DateTime)

	timestamp = Column(DateTime, nullable=False) # Time message was sent
	timestamp_recived = Column(DateTime) # Time that the message was recived (mainly for SMS type things)
	timestamp_pulled = Column(DateTime) # Time that the message was downloaded from the server / exported
	timestamp_imported = Column(DateTime) # Time that the message was inserted into the database

	other = Column(JSON) # Dict of any other data


