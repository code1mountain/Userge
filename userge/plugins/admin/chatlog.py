from userge import userge, Message, Config

@userge.on_cmd("logchat", about={
    'header': "Read the given Text in English",
    'usage': ".logchat @username"}, del_pre=True)
async def gts(message: Message):
    n = 0
    text = message.filtered_input_str
    chat = await userge.get_chat(text)
    for member in message._client.iter_chat_members(chat):
        n += 1
    await message.edit(str(member) + " " + str(n))
