from datetime import datetime
import hashlib
import uuid
from json_stream.base import TransientStreamingJSONList, TransientStreamingJSONObject

from sqlalchemy.orm import declarative_base

Base = declarative_base()


class CONFIG:
	TEMP_DOWNLOAD_FILE_FOR_INFO = True
	DOWNLOAD_FILE_PERM = True
	data_dir = '/home/ze/Desktop/messages-centralizer/'

	BUF_SIZE = 65536

def gen_uuid():
	return uuid.uuid4().hex


def generate_reference_string(service, reference_type, reference_identifyer):
	"""Ment for mentions in a chatroom or to reference other objects in the SQL table.
	
	Can not contain <>:"/\\|?*"""

	return f"<{service}:{reference_type}:{reference_identifyer}>"

def epoch_to_datetime(epoch): # Add timezone TODO
	return datetime.fromtimestamp(epoch).strftime('%Y-%m-%dT%H:%M:%S.%f+00:00')

def hash_obj(hash_obj):
	""""This function returns the SHA-256 hash
	of the file passed into it"""

	# make a hash object
	h = hashlib.sha256()

	# loop till the end of the file
	chunk = 0

	while chunk != b'':
		# read only BUF_SIZE bytes at a time
		if isinstance(hash_obj, type(b'')) or isinstance(hash_obj, type('')):
			if len(hash_obj) > CONFIG.BUF_SIZE:
				chunk, hash_obj = hash_obj[0:CONFIG.BUF_SIZE], hash_obj[CONFIG.BUF_SIZE:]
			else:
				chunk, hash_obj = hash_obj, b''
				
		else:
			chunk = hash_obj.read(CONFIG.BUF_SIZE)

		h.update(chunk)

	# return the hex representation of digest
	return h.hexdigest().upper()

def combine_items(input):
	if isinstance(input, TransientStreamingJSONList):
		return [combine_items(x) for x in input]

	if isinstance(input, TransientStreamingJSONObject):
		return_dict = {}
		for x in input.items():
				
			if isinstance(x[1], TransientStreamingJSONObject):
				return_dict[x[0]] = combine_items(x[1])

			elif isinstance(x[1], TransientStreamingJSONList):
				return_dict[x[0]] = combine_items(x[1])

			else:
				return_dict[x[0]] = x[1]
		
		return return_dict
	
	return input

def discord_datetime_to_epoch(datetime_str):
	if '.' in datetime_str:
		utc_time = datetime.strptime(datetime_str, f'%Y-%m-%dT%H:%M:%S.%f+00:00')
		return (utc_time - datetime(1970, 1, 1)).total_seconds()
	else:
		utc_time = datetime.strptime(datetime_str, f'%Y-%m-%dT%H:%M:%S+00:00')
		return (utc_time - datetime(1970, 1, 1)).total_seconds()


def groupme_id_to_epoch(groupme_id):
	return int(groupme_id)/100000000

def group_me_sender_type_to_type(group_me_sender_type):
	if group_me_sender_type == "user":
		return SENDER_TYPE.HUMAN_USER
	elif group_me_sender_type == "service":
		return SENDER_TYPE.OTHER
	elif group_me_sender_type == "system":
		return SENDER_TYPE.SYSTEM
	else:
		return SENDER_TYPE.OTHER
