function discord_template(message_dict) {
	return `<div class="message row discord-message" data-message-id="${message_dict['message_id']}" id="${message_dict['message_id']}">
	<div class="col-auto">
		<div class="avatar">
			<img src="/api/get-avatar-url/${message_dict['avatar_id']}/"" width="48px" height="48px">
		</div>

	</div>
	<div class="col float-end">
		
		<span class="author-name" data-author-id="${message_dict['author_id']}">${message_dict['author_name']}</span>
		<span class="date" data-date-epoch=${message_dict['timestamp']}>${message_dict['timestamp']}</span>	
		<div class="content">${message_dict['contents']}</div>

	</div>
</div>`
}
