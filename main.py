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
async def prefix(_, msg: types.Message):
	await msg.delete()
	username = msg.from_user.username
	chat_id = msg.chat.id
	user = await bot.get_chat_member(chat_id, username)
	prefix = msg.text.split(maxsplit=1)

	if len(prefix) >= 1:
		prefix = prefix[1]
	else:
		prefix = ''

	if not user.status == enums.ChatMemberStatus.ADMINISTRATOR:
		print(user.status)
		await bot.send_message(chat_id, 'У вас нет префикса (ну, или вы владелец или вы бот).')
		print(f'@{user.user.username} has no prefix')
		return
	if not user.promoted_by.username == bot_name:
		await bot.send_message(chat_id, f'Ваш префикс выдан другим [человеком](https://t.me/{user.promoted_by.username}). Извините, я не могу его поменять.', disable_web_page_preview=True)
		print(f'@{user.user.username} prefix is given by other person @{user.promoted_by.username}')
		return
	if len(prefix) > 16:
		await bot.send_message(chat_id, 'Длина префикса больше 16 символов.')
		print(f'prefix is {len(prefix)} long')
		return
	
	await bot.set_administrator_title(chat_id, username, prefix)
	await bot.send_message(chat_id, f'Префикс сменен с "{user.custom_title}" на "{prefix}"')
	print(f'changed @{username} from {user.custom_title} to {prefix}')
	
@bot.on_message(filters.command('addprefix', '/') &  filters.group & filters.user(allowed_users))
async def add_prefix(_, msg: types.Message):
	await msg.delete()
	chat_id = msg.chat.id
	arg = msg.text.split(maxsplit=2)
	users = []
	async for x in bot.get_chat_members(chat_id): #have no clue how to make it easier
		users.append(f"@{x.user.username}")

	if len(arg) > 1 and arg[1].startswith("@"):
		user = arg[1]
	elif msg.reply_to_message:
		user = f'@{msg.reply_to_message.from_user.username}'
	else:
		user = None
	
	if len(arg) > 2:
		prefix = arg[2]
	elif len(arg) > 1 and not arg[1].startswith("@"):
		prefix = arg[1]
	else:
		prefix = ''

	if not user in users:
		await bot.send_message(chat_id, f'Этого пользователя нет в беседе.')
		print(f'{user} user not found')
		return
	if user is None:
		await bot.send_message(chat_id, f'Пожалуйста, укажите пользователя при ответе или укажите его тег.')
		print('no user specified')
		return
	if len(prefix) > 16:
		await bot.send_message(chat_id, 'Длина префикса больше 16 символов.')
		print(f'prefix is {len(prefix)} long')
		return
	
	await bot.promote_chat_member(chat_id, user)
	await bot.set_administrator_title(chat_id, user, prefix)
	await bot.send_message(chat_id, 'Префикс выдан.')
	print(f'added {prefix} to {user}')

@bot.on_message(filters.command('delprefix', '/') & filters.group & filters.user(allowed_users))
async def delete_prefix(_, msg: types.Message):
	await msg.delete()
	chat_id = msg.chat.id
	user = msg.text.split(maxsplit=1)

	if len(user) > 1 and user[1].startswith("@"):
		user = user[1]
	elif msg.reply_to_message:
		user = f"@{msg.reply_to_message.from_user.username}"
	else:
		user = None

	if user is None:
		await bot.send_message(chat_id, 'Пожалуйста, укажите пользователя при ответе или укажите его тег.')
		print('no user specified')
		return
	
	await bot.promote_chat_member(chat_id, user, types.ChatPrivileges(can_manage_chat=False))
	await bot.send_message(chat_id, 'Префикс удален.')
	print(f'deleted {user} prefix')

if __name__ == '__main__':
	bot.run()
