function discord_template(message_dict) {
	let avatar_url = JSON.parse($.ajax({
		url: "/api/get-avatar-url/"+message_dict['avatar_uuid']+"/",
		async: false
	}).responseText)

	return `<div class="message row discord-message" data-message-id="${message_dict['message_id']}">
	<div class="col-auto">
		<div class="avatar">
			<img src="${avatar_url}" width="48px" height="48px">
		</div>
	</div>
	<div class="col float-end">
		
		<span class="author-name" data-author-id="${message_dict['author_id']}">${message_dict['author_name']}</span>
		<span class="date" data-date-epoch=${message_dict['timestamp']}>${message_dict['timestamp_date']}</span>	
		<div class="content">${message_dict['contents']}</div>

	</div>
</div>`
}
