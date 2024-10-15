from pyrogram import Client, types, filters, enums
from pyrogram.errors import bad_request_400 as err

# how to get api_id/hash - https://core.telegram.org/api/obtaining_api_id
# how to get bot token - https://core.telegram.org/bots/tutorial#obtain-your-bot-token
# in bot_name type bot username without @
# in allowed_users type users username (also without @) or ids who will have access for /addprefix and /delprefix

bot_token = ''
api_id = ''
api_hash = ''

bot = Client('bot', api_id, api_hash, bot_token=bot_token)
users = ['@durov'] #users that will have access to /addprefix and /delprefix

@bot.on_message(filters.command('prefix') & filters.group)
async def prefix_handler(_, msg:types.Message):
    await msg.delete()

    chat = msg.chat.id
    user = await bot.get_chat_member(chat, msg.from_user.id)
    bot_id = await bot.get_me() #using it just to get bot id to check if member was promoted by bot
    prefix = msg.text.removeprefix('/prefix').removeprefix(' ') #second .removeprefix to make it "title" and not " title"

    if user.status == enums.ChatMemberStatus.MEMBER:
        await bot.send_message(chat, 'У вас нет префикса.')
        print(f'{user.user.first_name} does not have prefix')
        return
    
    if user.promoted_by.id != bot_id.id:
        await bot.send_message(chat, 'Префикс нельзя сменить, потому что он выдан другим пользователем.')
        print(f'can not change {user.user.first_name} prefix because he was promoted by {user.promoted_by.id}')
        return

    if len(prefix) > 16:
        await bot.send_message(chat, 'Ваш префикс более 16 символов в длину.')
        print(f'can not change {user.user.first_name} prefix because its lenght more than 16 ({len(prefix)})')
        return

    await bot.set_administrator_title(chat, user.user.id, prefix)
    await bot.send_message(chat, f'Префикс успешно сменен с "{user.custom_title}" на "{prefix}"')
    print(f'successfully changed {user.user.first_name} prefix from {user.custom_title} to {prefix}')

@bot.on_message(filters.command('addprefix') & filters.group & filters.user(users))
async def addprefix_handler(_, msg:types.Message):
    await msg.delete()

    prefix = msg.text.removeprefix('/addprefix').removeprefix(' ')
    chat = msg.chat.id

    if not msg.reply_to_message is None: #in case if command used like reply /addprefix title
        username = msg.reply_to_message.from_user.id
    if prefix.startswith('@'): #in case if command used like /addprefix @username title
        if len(prefix.split(maxsplit=1)) > 1: #sometimes people just wanna add right to user
            username, prefix = prefix.split(maxsplit=1)
        else:
            username = prefix
            prefix = ''

    try:
        user = await bot.get_chat_member(chat, username)
    except err.UserNotParticipant:
        await bot.send_message(chat, 'Этого пользователя нет в беседе.')
        print('user is not presented in chat')
        return
    except err.UsernameNotOccupied:
        await bot.send_message(chat, 'Этого пользователя не существует.')
        print('user does not exist')
        return

    if user.status != enums.ChatMemberStatus.MEMBER: #this checks should be upper, ikr?
        await bot.send_message(chat, 'У этого человека уже есть префикс.')
        print(f'can not add prefix to {user.user.username} because he is not member (admin, owner, etc)')
        return
    if len(prefix) > 16:
        await bot.send_message(chat, 'Выдаваемый префикс более 16 символов в длину.')
        print(f'can not add prefix to {user.user.username} because its lenght more than 16 ({len(prefix)})')
        return

    await bot.promote_chat_member(chat, user.user.id)
    await bot.set_administrator_title(chat, user.user.id, prefix)
    await bot.send_message(chat, f'Префикс "{prefix}" выдан пользователю {user.user.first_name}.')
    print(f'successfully added "{prefix} to a {user.user.first_name}')

@bot.on_message(filters.command('delprefix') & filters.group & filters.user(users))
async def delprefix_handler(_, msg:types.Message):
    await msg.delete()

    prefix = msg.text.removeprefix('/delprefix').removeprefix(' ')
    bot_id = await bot.get_me()
    chat = msg.chat.id

    if not msg.reply_to_message is None:
        username = msg.reply_to_message.from_user.id
    if prefix.startswith('@'):
        username = prefix

    try:
        user = await bot.get_chat_member(chat, username)
    except err.UserNotParticipant:
        await bot.send_message(chat, 'Этого пользователя нет в беседе.')
        print('user is not presented in chat')
        return
    except err.UsernameNotOccupied:
        await bot.send_message(chat, 'Этого пользователя не существует.')
        print('user does not exist')
        return

    if user.status == enums.ChatMemberStatus.MEMBER:
        await bot.send_message(chat, 'У этого человека нет префикса.')
        print(f'can not delete prefix from {user.user.username} because he is member already')
        return
    if user.promoted_by.id != bot_id.id:
        await bot.send_message(chat, 'Префикс нельзя удалить, потому что он выдан другим пользователем.')
        print(f'can not delete prefox from {user.user.username} because he was promoted by {user.promoted_by.id}')
        return

    await bot.promote_chat_member(chat, user.user.id, types.ChatPrivileges(can_manage_chat=False))
    await bot.send_message(chat, f'Префикс пользователя {user.user.first_name} удален.')
    print(f'successfully deleted prefix from {user.user.first_name}')

if __name__ == '__main__':
    bot.run()
