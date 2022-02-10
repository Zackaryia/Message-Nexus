from parser.group_me import parser
from database_handler import insert_messages_to_db

insert_messages_to_db(next(parser("message.json", 0)))


