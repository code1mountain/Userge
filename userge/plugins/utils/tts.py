import re
import urllib.parse
import requests
from userge import userge, Message, Config
import pydub

encodeURIComponent = urllib.parse.quote_plus

voices = [
    {"voiceName": "IBM-Watson American English (Allison)", "lang": "en-US", "gender": "female"},
    {"voiceName": "IBM-Watson American English (AllisonV3)", "lang": "en-US", "gender": "female"},
    {"voiceName": "IBM-Watson American English (Lisa)", "lang": "en-US", "gender": "female"},
    {"voiceName": "IBM-Watson American English (LisaV3)", "lang": "en-US", "gender": "female"},
    {"voiceName": "IBM-Watson American English (Michael)", "lang": "en-US", "gender": "male"},
    {"voiceName": "IBM-Watson American English (MichaelV3)", "lang": "en-US", "gender": "male"},
    {"voiceName": "IBM-Watson British English (Kate)", "lang": "en-GB", "gender": "female"},
    {"voiceName": "IBM-Watson British English (KateV3)", "lang": "en-GB", "gender": "female"},
    {"voiceName": "IBM-Watson Castilian Spanish (Enrique)", "lang": "es-ES", "gender": "male"},
    {"voiceName": "IBM-Watson Castilian Spanish (EnriqueV3)", "lang": "es-ES", "gender": "male"},
    {"voiceName": "IBM-Watson Castilian Spanish (Laura)", "lang": "es-ES", "gender": "female"},
    {"voiceName": "IBM-Watson Castilian Spanish (LauraV3)", "lang": "es-ES", "gender": "female"},
    {"voiceName": "IBM-Watson Latin American Spanish (Sofia)", "lang": "es-LA", "gender": "female"},
    {"voiceName": "IBM-Watson Latin American Spanish (SofiaV3)", "lang": "es-LA", "gender": "female"},
    {"voiceName": "IBM-Watson North American Spanish (Sofia)", "lang": "es-US", "gender": "female"},
    {"voiceName": "IBM-Watson North American Spanish (SofiaV3)", "lang": "es-US", "gender": "female"},
    {"voiceName": "IBM-Watson German (Dieter)", "lang": "de-DE", "gender": "male"},
    {"voiceName": "IBM-Watson German (DieterV3)", "lang": "de-DE", "gender": "male"},
    {"voiceName": "IBM-Watson German (Birgit)", "lang": "de-DE", "gender": "female"},
    {"voiceName": "IBM-Watson German (BirgitV3)", "lang": "de-DE", "gender": "female"},
    {"voiceName": "IBM-Watson French (Renee)", "lang": "fr-FR", "gender": "female"},
    {"voiceName": "IBM-Watson French (ReneeV3)", "lang": "fr-FR", "gender": "female"},
    {"voiceName": "IBM-Watson Italian (Francesca)", "lang": "it-IT", "gender": "female"},
    {"voiceName": "IBM-Watson Italian (FrancescaV3)", "lang": "it-IT", "gender": "female"},
    {"voiceName": "IBM-Watson Japanese (Emi)", "lang": "ja-JP", "gender": "female"},
    {"voiceName": "IBM-Watson Japanese (EmiV3)", "lang": "ja-JP", "gender": "female"},
    {"voiceName": "IBM-Watson Brazilian Portuguese (Isabela)", "lang": "pt-BR", "gender": "female"},
    {"voiceName": "IBM-Watson Brazilian Portuguese (IsabelaV3)", "lang": "pt-BR", "gender": "female"}
  ]

def getAudioUrl(text, voice):
    matches = re.findall("^IBM-Watson .* \((.+)\)$", voice["voiceName"])
    voiceName = voice["lang"] + "_" + matches[0] + "Voice"
    return "https://text-to-speech-demo.ng.bluemix.net/api/v1/synthesize?text=" + encodeURIComponent(text) + "&voice=" + encodeURIComponent(voiceName) + "&download=true&accept=" + encodeURIComponent("audio/mp3")


def generate_voice(text, file_out, voice=voices[5]):
    url = getAudioUrl(text, voice)
    r = requests.get(url)
    with open(file_out, "wb") as f:
        f.write(r.content)


@userge.on_cmd("tts", about={
    'header': "Read the given Text in English",
    'usage': ".tts Text to read"
             ".tts [reply to message]"}, del_pre=True)
async def tts(message: Message):
    text = message.filtered_input_str
    replied = message.reply_to_message
    if not text and replid:
        text = replied.message
    if text:
        generate_voice(text, "talking.mp3")
        await message._client.send_voice(chat_id=message.chat.id,
                                         voice="talking.mp3",
                                         disable_notification=True)
    else:
        await message.edit("Please specify the text!")
