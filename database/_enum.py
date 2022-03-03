from enum import Enum

class OBJECT_TYPE(Enum):
	MESSAGE = 0
	USER = 1
	CHATROOM = 2
	EMOJI = 3
	FILE = 4
	AVATAR = 5
	ATTACHMENT = 6
	STICKER = 7
	ICON = 8


class FILE_STREAMING_TYPE(Enum):
	OTHER = -1 # Will error out
	JSON = 0
	HTML = 1
	CSV = 2

class SOURCE_PROGRAM(Enum):
	DISCORD_DCE_JSON = 0 # https://github.com/Tyrrrz/DiscordChatExporter
	DISCORD_DCE_HTML = 1 # https://github.com/Tyrrrz/DiscordChatExporter
	GROUP_ME_DIRECT_DOWNLOAD = 2 # https://web.groupme.com/profile/export

class SENDER_TYPE(Enum):
	OTHER = -1
	HUMAN_USER = 0
	BOT = 1
	WEBHOOK = 2
	SYSTEM = 3

class SERVICES(Enum):
	DISCORD = 0
	GROUPE_ME = 1

class CHATROOM_TYPE(Enum):
	OTHER = -1
	TEXT_CHANNEL = 0 # Text channel within a server
	GROUP_DM = 1 # A text chatroom within itself
	DIRECT = 2 # A 1-1 messaging chatroom
	VOICE = 3 # A voice chatroom
	THREAD = 4 # A sub chatroom for a text chatroom

	CHATROOM_TYPE_LIST = [
		OTHER, TEXT_CHANNEL, GROUP_DM, DIRECT, VOICE, THREAD
	]

# https://discord.com/developers/docs/resources/channel#channel-object-channel-types
class DISCORD_CHATROOM_TYPES(Enum):
	GUILD_TEXT = 0 # a text channel within a server
	DM = 1 # a direct message between users
	GUILD_VOICE = 2 # a voice channel within a server
	GROUP_DM = 3 # a direct message between multiple users
	GUILD_CATEGORY = 4 # an organizational category that contains up to 50 channels
	GUILD_NEWS = 5 # a channel that users can follow and crosspost into their own server
	GUILD_STORE = 6 # a channel in which game developers can sell their game on Discord
	GUILD_NEWS_THREAD = 10 # a temporary sub-channel within a GUILD_NEWS channel
	GUILD_PUBLIC_THREAD = 11 # a temporary sub-channel within a GUILD_TEXT channel
	GUILD_PRIVATE_THREAD = 12 # a temporary sub-channel within a GUILD_TEXT channel that is only viewable by those invited and those with the MANAGE_THREADS permission
	GUILD_STAGE_VOICE = 13 # a voice channel for hosting events with an audience

DISCORD_CHATROOM_TYPE_TO_CHATROOM_TYPE = {
	DISCORD_CHATROOM_TYPES.GUILD_TEXT: CHATROOM_TYPE.TEXT_CHANNEL,
	DISCORD_CHATROOM_TYPES.DM: CHATROOM_TYPE.DIRECT,
	DISCORD_CHATROOM_TYPES.GUILD_VOICE: CHATROOM_TYPE.VOICE,
	DISCORD_CHATROOM_TYPES.GROUP_DM: CHATROOM_TYPE.GROUP_DM,
	DISCORD_CHATROOM_TYPES.GUILD_CATEGORY: CHATROOM_TYPE.OTHER,
	DISCORD_CHATROOM_TYPES.GUILD_NEWS: CHATROOM_TYPE.TEXT_CHANNEL,
	DISCORD_CHATROOM_TYPES.GUILD_STORE: CHATROOM_TYPE.OTHER,
	DISCORD_CHATROOM_TYPES.GUILD_NEWS_THREAD: CHATROOM_TYPE.THREAD,
	DISCORD_CHATROOM_TYPES.GUILD_PUBLIC_THREAD: CHATROOM_TYPE.THREAD,
	DISCORD_CHATROOM_TYPES.GUILD_PRIVATE_THREAD: CHATROOM_TYPE.THREAD,
	DISCORD_CHATROOM_TYPES.GUILD_STAGE_VOICE: CHATROOM_TYPE.VOICE,
}

# Discord DCE Exporter
# https://github.com/Tyrrrz/DiscordChatExporter/blob/master/DiscordChatExporter.Core/Discord/Data/ChannelKind.cs
DISCORD_DCE_CHAT_TO_DISCORD_CHATROOM_TYPE = {
	"GuildTextChat": DISCORD_CHATROOM_TYPES.GUILD_TEXT,
	"DirectTextChat": DISCORD_CHATROOM_TYPES.DM,
	"GuildVoiceChat": DISCORD_CHATROOM_TYPES.GUILD_VOICE,
	"DirectGroupTextChat": DISCORD_CHATROOM_TYPES.GROUP_DM,
	"GuildCategory": DISCORD_CHATROOM_TYPES.GUILD_CATEGORY,
	"GuildNews": DISCORD_CHATROOM_TYPES.GUILD_NEWS,
	"GuildStore": DISCORD_CHATROOM_TYPES.GUILD_STORE
}

# https://discord.com/developers/docs/resources/channel#message-object-message-types
class DISCORD_MESSAGE_KIND(Enum):
	DEFAULT = 0
	RECIPIENT_ADD = 1
	RECIPIENT_REMOVE = 2
	CALL = 3
	CHANNEL_NAME_CHANGE = 4
	CHANNEL_ICON_CHANGE = 5
	CHANNEL_PINNED_MESSAGE = 6
	GUILD_MEMBER_JOIN = 7
	USER_PREMIUM_GUILD_SUBSCRIPTION = 8
	USER_PREMIUM_GUILD_SUBSCRIPTION_TIER_1 = 9
	USER_PREMIUM_GUILD_SUBSCRIPTION_TIER_2 = 10
	USER_PREMIUM_GUILD_SUBSCRIPTION_TIER_3 = 11
	CHANNEL_FOLLOW_ADD = 12
	GUILD_DISCOVERY_DISQUALIFIED = 14
	GUILD_DISCOVERY_REQUALIFIED = 15
	GUILD_DISCOVERY_GRACE_PERIOD_INITIAL_WARNING = 16
	GUILD_DISCOVERY_GRACE_PERIOD_FINAL_WARNING = 17
	THREAD_CREATED = 18
	REPLY = 19
	CHAT_INPUT_COMMAND = 20
	THREAD_STARTER_MESSAGE = 21
	GUILD_INVITE_REMINDER = 22
	CONTEXT_MENU_COMMAND = 23