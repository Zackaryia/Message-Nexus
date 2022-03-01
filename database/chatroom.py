from sqlalchemy import Column
import uuid
from database._utility import gen_uuid, Base
from database._enum import *

from sqlalchemy.types import Integer, String, Float, Boolean, DateTime, Enum, Text, JSON

class Chatroom(Base):
	__tablename__ = 'chatroom'

	id = Column(String, primary_key=True, default=gen_uuid, unique=True, nullable=False)

	parrent_id = Column(String) # Like the guild id (Discord) or the space id (Matrix)

	chatroom_id = Column(String, unique=True, nullable=False)
	chatroom_name = Column(String, nullable=False)
	chatroom_type = Column(Enum(CHATROOM_TYPE), nullable=False)
	chatroom_type_raw = Column(String)

	description = Column(String)

	service = Column(Enum(SERVICES), nullable=False) # Determined by helper.py in parser
	source_program = Column(Enum(SOURCE_PROGRAM)) # Program that retrived the message (_variables.py)

	avatar_id = Column(String)

	timestamp = Column(DateTime) # Time file was sent
	timestamp_recived = Column(DateTime) # Time that the file was sent (mainly for SMS type things)
	timestamp_pulled = Column(DateTime) # Time that the file was downloaded from the server / exported
	timestamp_imported = Column(DateTime) # Time that the message was inserted into the database

	other = Column(JSON) 


