import os
import sqlite3
import uuid


def create_or_reset_table(local_files_dir, copy_source_files_to_local_dir):
	if os.path.exists('messages.db'):
		os.remove('messages.db')
	with open('database_format.sql', 'r') as database_format_file:
		database_format = database_format_file.read()

	con = sqlite3.connect('messages.db')
	cur = con.cursor()
	cur.execute(database_format)
	cur.executemany("INSERT INTO messages VALUES (?, ?);", [
		('local_files_dir', local_files_dir),
		('copy_source_files_to_local_dir', copy_source_files_to_local_dir)
	])




if __name__ == "__main__":
	create_or_reset_table()