

from datetime import datetime
from database._enum import *
import hashlib
from database.file import File, get_url_file_hash_and_size, get_url_hash, get_file_hash_and_size
from sqlalchemy.orm import Query
from database._utility import hash_obj, CONFIG
import uuid
import logging
import os
from pathlib import Path
import json




def find_file(session, file_url_hash=None, file_hash=None):	
	print(session.commit)
	if file_url_hash != None:
		return Query(File, session=session).filter(
			File.url_hash == file_url_hash
		).first()
	elif file_hash != None:
		return Query(File, session=session).filter(
			File.file_hash == file_hash
		).first()
	else: # File hash and url are none. 
		logging.error("File url and hash are both None")
		return None



def create_find_update_file(session, file_name, ext, service, file_type, reference_id, source_program, file_url=None, full_file_location=None, source_file_path=None):
	if full_file_location == None and file_url == None and reference_id == None:
		raise ValueError("Did not input a full_file_location or file_url")

	file_inst = Query(File, session=session).filter(
		File.reference_id == reference_id,
		File.source_program == source_program
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
			reference_id = reference_id,
			service = service,
			file_type = file_type,
			source_program = source_program,
			timestamp_imported = datetime.now()
		)
		
	# Update file with new information
	if file_url != None:
		file_inst.insert_url(file_url, file_name, ext, reference_id)
	if full_file_location != None:
		file_inst.insert_file_path(full_file_location, source_file_path, reference_id, file_name, ext)

	return file_inst
