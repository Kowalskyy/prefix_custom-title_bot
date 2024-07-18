# prefix_custom-title_bot
some goofy doofy ahh bot made on pyrogram so do
```pip install pyrogram tgcrypto```

everything written in main file, but i'll copy it here

- how to get api_id/hash - https://core.telegram.org/api/obtaining_api_id
- how to get bot token - https://core.telegram.org/bots/tutorial#obtain-your-bot-token
- in bot_name type bot username without @
- in allowed_users type users username (also without @) or ids who will have access for /addprefix and /delprefix

# commands
/addprefix @user/reply_to_user prefix - adds prefix for specified user, also forceful change of prefix [admin only]  
/delprefix @user/reply_to_user - deletes prefix for specified user [admin only]  
/prefix prefix - changes prefix  
# note: there is no handlers to adding/deleting prefixes who wasn't promoted by bot, so it'll error eventually
