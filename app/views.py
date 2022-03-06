from app import app
from flask import render_template, request, redirect, url_for, flash, make_response, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, Query
from database import *
from datetime import datetime
from database._enum import *



engine = create_engine("sqlite:///"+"home/ze/Desktop/Message-Nexus", echo=True)

def row2dict(row):
    d = {}
    for column in row.__table__.columns:
        d[column.name] = str(getattr(row, column.name))

    return d

def get_chatrooms():
	session = Session(engine)

	return Query(Chatroom, session).all()

print(get_chatrooms())

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

@app.route('/api/get-avatar-url/<file_id>/')
def return_avatar_url(file_id):
	session = Session(engine)

	avatar = Query(File, session).filter(
		File.id == file_id
	).first()
	print(avatar)
	print(row2dict(avatar))
	print(avatar.local_location)

	if avatar.file_url != None:
		return redirect(avatar.file_url)

# self.values['service'], self.values['chatroom_type'], self.values['chatroom_id']
@app.route('/api/messages/<int:service>/<chatroom_id>/')
def chatroom_messages(service, chatroom_id):
	if "limit" in request.args:
		limit = int(request.args['limit'])
	else:
		limit = 500
		
	session = Session(engine)

	x = Query(Message, session).filter(
		Message.service == SERVICES(service).name,
		Message.chatroom_id == chatroom_id
	).order_by(Message.timestamp.desc())
	
	if "before_timestamp" in request.args:
		x = x.filter(Message.timestamp < datetime.fromtimestamp(request.args['before_timestamp']))
	elif "before_message_id" in request.args: 
		x = x.filter(Message.message_id < request.args['before_message_id'])

	x = x.limit(100)

	return_dict = []
	for y in x:
		return_dict.append(row2dict(y))

	return jsonify(return_dict)



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

