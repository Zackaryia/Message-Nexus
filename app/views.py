from app import app
from flask import render_template, request, redirect, url_for, flash, make_response, jsonify, request
import sqlite3

con = sqlite3.connect('messages.db', check_same_thread=False)
cur = con.cursor()



def run_sql(statment, variables={}, limit=-1):
	cur.execute(statment, variables)

	if limit > 0:
		return cur.fetchmany(limit)

	return cur.fetchall()

messages_headder = [i[1] for i in run_sql("PRAGMA table_info(messages)")]
files_headder = [i[1] for i in run_sql("PRAGMA table_info(files)")]


def run_sql_prittify(*argv, **kwargs):
	headers = kwargs.pop('headers')
	statment_resolved_values = run_sql(*argv, **kwargs)
	return_list = []
	for value in statment_resolved_values:
		return_list.append({headers[i]: value[i] for i in range(0, len(headers), 1)})

	return return_list

def get_avatar_url(file_uuid):
	x = run_sql_prittify("SELECT * FROM files WHERE file_uuid=:file_uuid", {"file_uuid": file_uuid}, limit=1, headers=files_headder)[0]
	print(x)
	return x


def get_chatrooms():
	messages_headder = [i[1] for i in run_sql("PRAGMA table_info(chatrooms)")]

	chatrooms = run_sql_prittify("SELECT * FROM chatrooms", {}, limit=-1, headers=messages_headder)
	print(chatrooms)
	return chatrooms

@app.route('/')
def home():

	return render_template('index.html', chatrooms=get_chatrooms(), service=0, chatroom_id="913919178287747114")

@app.route('/import-messages/')
def import_messages():
	return render_template('import.html', chatrooms=get_chatrooms())


@app.route('/chatroom/<int:service>/<chatroom_id>/')
def chatrooms(service, chatroom_id):
	# Get chatrooms
	
	return render_template('index.html', chatrooms=get_chatrooms(), service=service, chatroom_id=chatroom_id)

@app.route('/api/get-avatar-url/<file_uuid>/')
def return_avatar_url(file_uuid):
	avatar_data = get_avatar_url(file_uuid)
	if avatar_data["full_source_file_location_local"] != None:
		return jsonify(avatar_data['full_source_file_location_local'])
	else:
		return jsonify(avatar_data['source_file_location_remote'])


# self.values['service'], self.values['chatroom_type'], self.values['chatroom_id']
@app.route('/api/messages/<int:service>/<chatroom_id>/')
def chatroom_messages(service, chatroom_id):
	# Get messages
	print(request.args)
	
	if "limit" in request.args:
		limit = int(request.args['limit'])
	else:
		limit = 500
		
	args = {
		"service": service, 
		"chatroom_id": chatroom_id,
		**request.args # Can be dangerous
	}

	sql_statment = "SELECT * FROM messages WHERE service=:service AND chatroom_id=:chatroom_id "
	
	### Conditions ###
	if "before_timestamp" in args:
		sql_statment += " AND timestamp < :before_timestamp " 
	elif "before_message_id" in args: 
		# Make sure message id is an integer and it allways incriments up as time goes forward
		sql_statment += " AND CAST(message_id AS int) < :before_message_id "

	sql_statment += " ORDER BY timestamp DESC "
	### Conditions ### 

	print(sql_statment, args)
	messages = run_sql_prittify(sql_statment, args, limit=int(limit), headers=messages_headder)

	#print(messages)

	return jsonify(messages)

@app.route('/api/submit-import/', methods = ['POST'])
def submit_import():
	
	print(request.data)
	
	data = request.form
	for key, value in data.items():
		print("received", key, "with value", value)

	return jsonify(dict(data.items()))

@app.route('/api/headers/')
def get_message_headers():
	return jsonify(messages_headder)

@app.route('/static/<path:path>/')
def send_js(path):
	return send_from_directory('static', path)
