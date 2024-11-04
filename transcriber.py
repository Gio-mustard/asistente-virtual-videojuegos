from groq_use import MainModelLLM

#Convertir audio en texto
class Transcriber(MainModelLLM):
    def __init__(self,llm_object):
        super().__init__(llm_object)
        self.__filename = "audio.mp3"
        pass
        
    #Siempre guarda y lee del archivo audio.mp3
    #Utiliza whisper en la nube :) puedes cambiarlo por una impl local
    def transcribe(self, audio):
        audio.save(self.__filename)
        audio_file= open(self.__filename, "rb")

        transcript = self._ai.audio.transcriptions.create(
            file=(self.__filename, audio_file.read()), # Required audio file
            model="whisper-large-v3-turbo", # Required model to use for transcription
            response_format="json",  # Optional
            language="es",  # Optional
            temperature=0.0  # Optional
        )
        return transcript.text