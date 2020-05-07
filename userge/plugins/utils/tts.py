import re
import urllib.parse
import requests
import pydubs



encodeURIComponent = urllib.parse.quote_plus

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
    await message.edit("Working!")
