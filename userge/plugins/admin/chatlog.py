from userge import userge, Message, Config

@userge.on_cmd("logchat", about={
    'header': "Read the given Text in English",
    'usage': ".logchat @username"}, del_pre=True)
async def gts(message: Message):
    text = message.filtered_input_str
    chat = await userge.get_chat(text)
    await message.edit(chat.username)
