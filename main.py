import asyncio
from pyrogram import Client, filters, types, enums


# how to get api_id/hash - https://core.telegram.org/api/obtaining_api_id
# how to get bot token - https://core.telegram.org/bots/tutorial#obtain-your-bot-token
# in bot_name type bot username without @
# in allowed_users type users username (also without @) or ids who will have access for /addprefix and /delprefix

#note/ there is no handlers to adding/deleting prefixes who wasn't promoted by bot, so it'll error eventually
api_id = int
api_hash = str
token = str
bot_name = str
allowed_users = []
bot = Client('bot', api_id, api_hash, bot_token=token)


@bot.on_message(filters.command('prefix', '/') & filters.group)
async def prefix(_, msg: types.Message): #custom title change
	await msg.delete()
	username = msg.from_user.username
	chat_id = msg.chat.id
	user = await bot.get_chat_member(chat_id, username)
	prefix = msg.text.split(maxsplit=1)

	if len(prefix) >= 1: #check if there is anything after /prefix
		prefix = prefix[1] #changes to whatever user typed if present
	else:
		prefix = '' #changes to blank, will delete custom title

	if not user.status == enums.ChatMemberStatus.ADMINISTRATOR: #check if user have any admin rights
		print(user.status)
		await bot.send_message(chat_id, 'У вас нет префикса (ну, или вы владелец или вы бот).')
		print(f'@{user.user.username} has no prefix')
		return
	if not user.promoted_by.username == bot_name: #check if user was promoted by other user
		await bot.send_message(chat_id, f'Ваш префикс выдан другим [человеком](https://t.me/{user.promoted_by.username}). Извините, я не могу его поменять.', disable_web_page_preview=True)
		print(f'@{user.user.username} prefix is given by other person @{user.promoted_by.username}')
		return
	if len(prefix) > 16: #check if custom title lenght is less than 16 characters
		await bot.send_message(chat_id, 'Длина префикса больше 16 символов.')
		print(f'prefix is {len(prefix)} long')
		return
	
	await bot.set_administrator_title(chat_id, username, prefix)
	await bot.send_message(chat_id, f'Префикс сменен с "{user.custom_title}" на "{prefix}"')
	print(f'changed @{username} from {user.custom_title} to {prefix}')
	
@bot.on_message(filters.command('addprefix', '/') &  filters.group & filters.user(allowed_users))
async def add_prefix(_, msg: types.Message): #adds admin rights to user and custom title if present
	await msg.delete()
	chat_id = msg.chat.id
	arg = msg.text.split(maxsplit=2)
	users = []
	async for x in bot.get_chat_members(chat_id): #gets every user in chat
		users.append(f"@{x.user.username}") #i have no clue how to make it easier

	if len(arg) > 1 and arg[1].startswith("@"):
		user = arg[1] #changes to @tag if user typed [/addprefix @tag prefix]
	elif msg.reply_to_message:
		user = f'@{msg.reply_to_message.from_user.username}' #changes to @tag if user used command with reply like [reply /addprefix prefix]
	else:
		user = None #changes to none in case user isn't present in command
	
	if len(arg) > 2:
		prefix = arg[2] #changes to prefix if user typed [/addprefix @tag prefix]
	elif len(arg) > 1 and not arg[1].startswith("@"):
		prefix = arg[1] #changes to prefix if user used command with reply like [reply /addprefix prefix]
	else:
		prefix = '' #changes to blank just to give user very basic rights

	if not user in users: #check if user is present in chat
		await bot.send_message(chat_id, f'Этого пользователя нет в беседе.')
		print(f'{user} user not found')
		return
	if user is None: #check if user wasn't present in command
		await bot.send_message(chat_id, f'Пожалуйста, укажите пользователя при ответе или укажите его тег.')
		print('no user specified')
		return
	if len(prefix) > 16: #check if custom title lenght is less than 16 characters
		await bot.send_message(chat_id, 'Длина префикса больше 16 символов.')
		print(f'prefix is {len(prefix)} long')
		return
	
	await bot.promote_chat_member(chat_id, user)
	await bot.set_administrator_title(chat_id, user, prefix)
	await bot.send_message(chat_id, 'Префикс выдан.')
	print(f'added {prefix} to {user}')

@bot.on_message(filters.command('delprefix', '/') & filters.group & filters.user(allowed_users))
async def delete_prefix(_, msg: types.Message): #deletes admin rights from user
	await msg.delete()
	chat_id = msg.chat.id
	user = msg.text.split(maxsplit=1)

	if len(user) > 1 and user[1].startswith("@"):
		user = user[1] #changes to @tag if user typed [/delprefix @tag]
	elif msg.reply_to_message:
		user = f"@{msg.reply_to_message.from_user.username}" #changes to @tag if user used command with reply like [reply /delprefix]
	else:
		user = None #changes to none in case user isn't present in command

	if user is None: #check if user wasn't present in command
		await bot.send_message(chat_id, 'Пожалуйста, укажите пользователя при ответе или укажите его тег.')
		print('no user specified')
		return
	
	await bot.promote_chat_member(chat_id, user, types.ChatPrivileges(can_manage_chat=False))
	await bot.send_message(chat_id, 'Префикс удален.')
	print(f'deleted {user} prefix')

if __name__ == '__main__':
	bot.run()
