from userge import userge, Message, Config
import json

@userge.on_cmd("logchat", about={
    'header': "Read the given Text in English",
    'usage': ".logchat @username"})
async def gts(message: Message):
    obj = []
    text = message.filtered_input_str
    async for member in message._client.iter_chat_members(text):
        obj.append({
            "user_id": member.user.id,
            "is_bot": member.user.is_bot,
            "is_deleted": member.user.is_deleted,
            "first_name": member.user.first_name,
            "last_name": member.user.last_name,
            "last_online_date": member.user.last_online_date,
            "username": member.user.username,
            "dc_id": member.user.dc_id,
            "phone_number": member.user.phone_number,
            "status": member.status
        })
    #await message.edit(str(member) + " " + str(n))
    await message.edit(f"Got {len(obj)} users")
    await message.send_as_file(json.dumps(obj, indent=4), filename="members_log.json")
