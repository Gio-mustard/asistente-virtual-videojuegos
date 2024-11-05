import os
from dotenv import load_dotenv
import requests
from gtts import gTTS

#Texto a voz. Esta impl utiliza ElevenLabs
class TTS():
    def __init__(self):
        load_dotenv()
        self.key = os.getenv('ELEVENLABS_API_KEY')
    
    def process(self, text):
        tts = gTTS(text=text, lang='es')
        tts.save("static/response.mp3")
        return "response.mp3"
    
    def _process(self, text,index=0):
        CHUNK_SIZE = 1024
        #Utiliza la voz especifica de Bella
        #Me robe este codigo de su pagina hoh
        url = "https://api.elevenlabs.io/v1/text-to-speech/15bJsujCI3tcDWeoZsQP"

        headers = {
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
            "xi-api-key": self.key
        }

        data = {
            "text": text,
            "model_id": "eleven_multilingual_v2",
            "voice_settings": {
                "stability": 0.55,
                "similarity_boost": 0.55
            }
        }

        #Lo guarda en static/response.mp3 para que el sitio web
        #pueda leerlo y reproducirlo en el explorador
        file_name = f"response{index}.mp3"
        response = requests.post(url, json=data, headers=headers)
        print(F"{response=}")
        print(response.text)
        with open("static/" + file_name, 'wb') as f:
            for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
                if chunk:
                    f.write(chunk)
                    
        return file_name