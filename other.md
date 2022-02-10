NOTE: All ids are structured as seen below

  Descriminator to determine between the type of id, message vs emote vs service vs user etc
 / Service id, int for the specific service
| / A underscore for seperation
|| /       The id of the message according to the service
|||       /
|||      |
@0_3209402394924023





# Messages table
@message_id (Plus service descirminator) 
@service 

@chatroom_id
chatroom_type // int Group dm or private dm or sub chatroom or server
@contents 
author_uuid
@author_name (with descriminator for discord)
@author_avatar 
author_type (bot, user, webhook etc)
attachments_id // List of ids
favorited_or_pinned 
reactions_str // <emote_id>:count;<emote_id>:count;<emote_id>:count etc
reactions_id
embed_id
@replies_to // the id of the previous message
edited // Bool
edited_id
source_file - the file in /files/ that this message came from.
source_program - the program (& version) that the data was downloaded
timestamp_pulled - the timestamp the data was downloaded / pulled from the service
timestamp_imported - the timestamp the data was imported to Message Centralizer
@timestamp - epoch of message sent date
@timestamp_date - 2021/10/13 5:05pm 
@timestamp_recived - epoch of message sent date // Nullable
@timestamp_recived_date - 2021/10/13 5:05pm  // Nullable
@other - A json object for what ever garbage you want

# User table
user_id
user_name
nickname
avatar
all_nicknames // list of all KNOWN nicknames
all_avatars // list of all KNOWN avatars
user_type // bot/user/admin/system
account_creation - epoch
account_creation_date - 2021/10/13 5:05pm
other - A json object thats basically a blob

# chatroom table 
chatroom_id
chatroom_name
chatroom_avatar
server_id
all_chatroom_names // list of all KNOWN chat room names
all_avatars // list of all KNOWN avatars
other - A json object thats basically a blob

# server table // basically any group of chat rooms
server_id
server_name
server_avatar
all_chatrooms // list of all sub chat rooms
all_server_names // list of all KNOWN chat room names
all_avatars // list of all KNOWN avatars
other - A json object thats basically a blob

# File
file_id
foreign_location
local_location
file_size
file_ext
file_name

# Emote
emote_id
emote_name
file_id

# Reactions
message_id
emote_id
user_id

# History 
also have past history of all reactions, edits, and more