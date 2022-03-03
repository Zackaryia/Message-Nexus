from sqlalchemy import Column
from database._utility import hash_obj, gen_uuid, CONFIG, Base
from database._enum import *
from sqlalchemy.types import Integer, String, Float, Boolean, DateTime, Enum, Text, JSON

import os, json
import shutil
import requests
from pathlib import Path


class File(Base):
	__tablename__ = 'file'

	id = Column(String, primary_key=True, default=gen_uuid, unique=True, nullable=False)

	parrent_type = Column(Enum(OBJECT_TYPE))
	parrent_id = Column(String) # Like chatroom id if this is a chatroom avatar
	name = Column(String) # Sticker name, emoji name, anything other than file name that is relevant

	file_type = Column(Enum(OBJECT_TYPE), nullable=False)

	reference_id = Column(String, nullable=False) # From source program attachment id, or avatar id, emoji id, sticker id, or something like that in the reference form

	service = Column(Enum(SERVICES), nullable=False)
 
	source_file_path = Column(String) # The file location that was defined in the origin program
	relative_file_path = Column(String) # The file location relative to the exported file
	full_source_file_path = Column(String) # The full file location from root

	file_url = Column(String)
	url_hash = Column(String)

	file_name = Column(String)
	file_ext = Column(String)
	
	file_hash = Column(String)
	file_size = Column(Integer)

	source_program = Column(Enum(SOURCE_PROGRAM), nullable=False)

	timestamp = Column(DateTime) # Time file was sent
	timestamp_recived = Column(DateTime) # Time that the file was sent (mainly for SMS type things)
	timestamp_pulled = Column(DateTime) # Time that the file was downloaded from the server / exported
	timestamp_imported = Column(DateTime) # Time that the message was inserted into the database


	other = Column(JSON) 


	def insert_url(self, url, file_name, ext, ref_id):
		# Sets data that can be easily generated
		ext = ext.split('?')[0] # Removing any extra parts on the ext left by say a ?size=128 in the url for the file
		self.file_url = url
		self.url_hash = hash_obj(url.encode('utf-8'))
		self.source_file_location_remote = url
		self.file_name = file_name
		self.file_ext = ext
		
		self.reference_id = ref_id
	

		if self.file_hash == None and CONFIG.TEMP_DOWNLOAD_FILE_FOR_INFO:
			self.file_hash, self.file_size = get_url_file_hash_and_size(url)

	
	def insert_file_path(self, full_file_location, source_file_path, ref_id, file_name, ext):
		self.file_name, self.file_ext = file_name, ext
		self.reference_id = ref_id
		self.full_file_location = full_file_location
		self.source_file_path = source_file_path

		with open(self.full_file_location, 'rb') as file_obj:
			self.file_hash = hash_obj(file_obj)

		self.local_location = os.path.join(CONFIG.data_dir, "files", self.file_hash) + self.file_ext

		print(full_file_location)
		self.file_size = Path(full_file_location).stat().st_size

		shutil.copy(self.full_file_location, self.local_location)

		
		self.reference_id = ref_id




url_cache = dict()
def get_url_hash(url):
	if url not in url_cache:
		url_cache[url] = hash_obj(url.encode('utf-8'))

	return url_cache[url]


url_file_cache = dict()
def get_url_file_hash_and_size(url, set_none_cache=True, save_file=False, save_file_location=None):
	if url not in url_file_cache:
		response = requests.get(url)

		file_hash, file_size = None, 0
		if response.ok: # Makes sure that there is something to actually hash or get 
			file_hash = hash_obj(response.content)
			file_size = len(response.content)

			if save_file:
				with open(save_file_location, "wb") as f:
					f.write(response.content)

		else:
			if set_none_cache: # You may not want to set the value of this location to none but in that case, it will.
				print(f"URL: {url} could not be retrieved and data was set to None, 0.")

		url_file_cache[url] = (file_hash, file_size)

	return url_file_cache[url]


file_hash_cache = dict()
def get_file_hash_and_size(file_full_location):
	if file_full_location not in file_hash_cache:
		print("a")
		with open(file_full_location, 'rb') as raw_file:
			print("b")

			file_hash = hash_obj(raw_file)
			print(file_hash)


		file_size = os.path.getsize(file_full_location)

		file_hash_cache[file_full_location] = (file_hash, file_size)
	
	print(file_hash_cache[file_full_location])
	return file_hash_cache[file_full_location]
