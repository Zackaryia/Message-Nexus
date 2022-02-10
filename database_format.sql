CREATE TABLE messages (
	reference_id		TEXT	NOT NULL,
	message_id			TEXT	NOT NULL, 
	service				INT		NOT NULL, -- Determined by helper.py in parser
	message_type		TEXT, -- Determined by helper.py in parser
	message_type_raw	TEXT, -- Directly from the service
	contents			TEXT, 
	chatroom_id			TEXT	NOT NULL, 
	chatroom_reference_id TEXT  NOT NULL,
	chatroom_type		TEXT	NOT NULL, -- The type of chat room (group dm, dm, channel, etc) Determined by helper.py in parser
	chatroom_type_raw	TEXT, -- If availible the raw format of the chat's type
	author_name			TEXT,
	author_id			TEXT	NOT NULL,

	avatar_uuid			TEXT,
	attachments_ids		TEXT,

	sender_type			TEXT, -- The type of sender (user, bot, system, etc) Determined by helper.py in parser
	sender_type_raw		TEXT, -- If availible the raw format of the sender's type

	favorited_or_pinned	BOOLEAN, -- If a message was pinned or favorited (like discord not like group me)
	reactions_str		TEXT, -- Simple plain text format of the reactions
	reactions_id		TEXT, -- Links to the ID of an reactioms table entry
	embed_id			TEXT, -- Links to the ID of an embed table entry
	replied_to			TEXT, -- ID of the message the current message replies to
	edited				BOOLEAN, -- If message was edited
	edited_timestamp	FLOAT,    -- Timestamp message was edited
	edited_timestamp_date TEXT, 
	
	export_ids			TEXT,
	source_program		INT,  -- Program that retrived the message

	timestamp			FLOAT	NOT NULL, -- Time message was sent
	timestamp_date		TEXT,

	timestamp_pulled	FLOAT, -- Time that the message was downloaded from the server / exported
	timestamp_imported	FLOAT, -- Time that the message was inserted into the database 
	timestamp_recived	FLOAT, -- Time that the message was recived (mainly for SMS type things)

	other				TEXT -- Dict of any other data
);

CREATE TABLE chatrooms (
	reference_id		TEXT	NOT NULL,
	chatroom_id     	TEXT	NOT NULL, 
	service         	INT		NOT NULL, -- Determined by helper.py in parser
	chatroom_type   	TEXT, -- Determined by helper.py in parser
	chatroom_type_raw	TEXT, -- Directly from the service
	description        	TEXT, 
	
	avatar_uuid			TEXT,
	chatroom_name   	TEXT	NOT NULL,
	attachments_uuid	TEXT,

	source_file     	TEXT,	-- File that the message was retrieved from
	source_program  	INT,  -- Program that retrived the message

	timestamp			FLOAT, -- Time message was sent
	timestamp_date  	TEXT,

	timestamp_pulled	FLOAT, -- Time that the message was downloaded from the server / exported
	timestamp_imported	FLOAT, -- Time that the message was inserted into the database 
	timestamp_recived	FLOAT, -- Time that the message was recived (mainly for SMS type things)

	other           	TEXT -- Dict of any other data
);



CREATE TABLE files (
	file_uuid			TEXT	NOT NULL,

	service				INT	NOT NULL,
	local_location		TEXT,

	raw_source_file_location_local TEXT,
	full_source_file_location_local TEXT,

	source_file_location_remote TEXT,
	source_file_name	TEXT,
	source_file_ext 	TEXT,
	output_file_name	TEXT, -- Currently making the file hash to make it so I dont duplicate outputs.

	file_type			INT,
	
	author_id			TEXT,
	chatroom_id			TEXT,
	--author_id			TEXT, other things I can add
	--author_id			TEXT,
	--author_id			TEXT,

	reference_id		TEXT, -- From source program Avatar id, or message_id, or something like that in the reference form
	reference_name		TEXT, -- Like user name if this is an avatar, or a channel's name if this is a channel icon
	url_hash			TEXT,
	file_hash			TEXT,
	file_size			TEXT,

	source_program		INT,
	timestamp			FLOAT,
	timestamp_date		TEXT,
	
	timestamp_pulled	FLOAT,
	timestamp_imported	FLOAT, 
	timestamp_recived	FLOAT,

	other				TEXT -- Dict of any other data
);

CREATE TABLE meta_data (
	key_field TEXT NOT NULL,
	value_field TEXT
);