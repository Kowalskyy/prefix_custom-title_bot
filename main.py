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
async def prfx_hndl(client, msg: types.Message):
	await msg.delete()
	un = msg.from_user.username
	cid = msg.chat.id
	user = await bot.get_chat_member(cid, un)
	arg = msg.text.split(maxsplit=1)
	prfx = arg[1] if not len(arg) <= 1 else ''
	
	if not user.status == enums.ChatMemberStatus.ADMINISTRATOR:
		print(user.status)
		await bot.send_message(cid, 'У вас нет префикса (ну, или вы владелец или вы бот).')
		print(f'@{user.user.username} has no prefix')
		return
	if not user.promoted_by.username == bot_name:
		await bot.send_message(cid, f'Ваш префикс выдан другим [человеком](https://t.me/{user.promoted_by.username}). Извините, я не могу его поменять.', disable_web_page_preview=True)
		print(f'@{user.user.username} prefix is given by other person @{user.promoted_by.username}')
		return
	if len(prfx) > 16:
		await bot.send_message(cid, 'Длина префикса больше 16 символов.')
		print(f'prefix is {len(prfx)} long')
		return
	
	await bot.set_administrator_title(cid, un, prfx)
	await bot.send_message(cid, f'Префикс сменен с "{user.custom_title}" на "{prfx}"')
	print(f'changed @{un} from {user.custom_title} to {prfx}')
	
@bot.on_message(filters.command('addprefix', '/') &  filters.group & filters.user(allowed_users))
async def aprf_hndl(client, msg: types.Message):
	await msg.delete()
	cid = msg.chat.id
	arg = msg.text.split(maxsplit=2)
	users = []
	async for x in bot.get_chat_members(cid): #have no clue how to make it easier
		users.append(f"@{x.user.username}")
	user = arg[1] if len(arg) > 1 and arg[1].startswith("@") else f"@{msg.reply_to_message.from_user.username}" if msg.reply_to_message else None
	prfx = arg[2] if len(arg) > 2 else arg[1] if len(arg) > 1 and not arg[1].startswith("@") else ''
	
	if not user in users:
		await bot.send_message(cid, f'Этого пользователя нет в беседе.')
		print(f'{user} user not found')
		return
	if user is None:
		await bot.send_message(cid, f'Пожалуйста, укажите пользователя при ответе или укажите его тег.')
		print('no user specified')
		return
	if len(prfx) > 16:
		await bot.send_message(cid, 'Длина префикса больше 16 символов.')
		print(f'prefix is {len(prfx)} long')
		return
	
	await bot.promote_chat_member(cid, user)
	await bot.set_administrator_title(cid, user, prfx)
	await bot.send_message(cid, 'Префикс выдан.')
	print(f'added {prfx} to {user}')

@bot.on_message(filters.command('delprefix', '/') & filters.group & filters.user(allowed_users))
async def dprf_hndl(client, msg: types.Message):
	await msg.delete()
	cid = msg.chat.id
	arg = msg.text.split(maxsplit=1)
	user = arg[1] if len(arg) > 1 and arg[1].startswith("@") else f"@{msg.reply_to_message.from_user.username}" if msg.reply_to_message else None

	if user is None:
		await bot.send_message(cid, 'Пожалуйста, укажите пользователя при ответе или укажите его тег.')
		print('no user specified')
		return
	
	await bot.promote_chat_member(cid, user, types.ChatPrivileges(can_manage_chat=False))
	await bot.send_message(cid, 'Префикс удален.')
	print(f'deleted {user} prefix')

if __name__ == '__main__':
	bot.run()