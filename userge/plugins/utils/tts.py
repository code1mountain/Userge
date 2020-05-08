import re
import urllib.parse
import requests
from userge import userge, Message, Config
from pydub import AudioSegment
import os.path

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

pattern2 = r"\n *\n"

def split_string(text, maxlength=4700):
  while text:
    if len(text) < 4700:
      yield text
      return
    sub = text[:4700]
    index = [(m.start(0), m.end(0)) for m in re.finditer(pattern2, sub)][-1]
    if index[0] <= 0:
      index=(4700, 4700)
    yield sub[:index[0]]
    text = text[index[1]:]


def getAudioUrl(text, voice):
    matches = re.findall("^IBM-Watson .* \((.+)\)$", voice["voiceName"])
    voiceName = voice["lang"] + "_" + matches[0] + "Voice"
    return "https://text-to-speech-demo.ng.bluemix.net/api/v2/synthesize?text=" + encodeURIComponent(text) + "&voice=" + encodeURIComponent(voiceName) + "&download=true&accept=" + encodeURIComponent("audio/mp3")


def generate_voice(text, file_out, voice=voices[5]):
    playlist = AudioSegment.silent(duration=100)
    for t in split_string(text):
        
        url = getAudioUrl(t, voice)
        r = requests.get(url)
        with open(file_out, "wb") as f:
            f.write(r.content)
        while os.path.getsize(file_out) < 2000:
            url = getAudioUrl(text, voice)
            r = requests.get(url)
            with open(file_out, "wb") as f:
                f.write(r.content)
        playlist = playlist.append(AudioSegment.from_mp3(file_out))
    playlist.export(file_out, format='mp3').close()


@userge.on_cmd("tts", about={
    'header': "Read the given Text in English",
    'usage': ".tts Text to read"
             ".tts [reply to message]"}, del_pre=True)
async def tts(message: Message):
    text = message.filtered_input_str
    replied = message.reply_to_message
    if not text and replied:
        text = replied.text
    if text:
        await message.delete()
        generate_voice(text, "talking.mp3")
        await message._client.send_voice(chat_id=message.chat.id,
                                         voice="talking.mp3",
                                         disable_notification=True)
    else:
        await message.edit("Please specify the text!")
        
@userge.on_cmd("gts", about={
    'header': "Read the given Text in English",
    'usage': ".tts Text to read"
             ".tts [reply to message]"}, del_pre=True)
async def gts(message: Message):
    text = message.filtered_input_str
    replied = message.reply_to_message
    if not text and replied:
        text = replied.text
    if text:
        await message.delete()
        generate_voice(text, "talking.mp3", voice=voices[17])
        await message._client.send_voice(chat_id=message.chat.id,
                                         voice="talking.mp3",
                                         disable_notification=True)
    else:
        await message.edit("Please specify the text!")
