import os
import groq
from dotenv import load_dotenv
from flask import Flask, render_template, request
import json
from transcriber import Transcriber
from llm import LLM
from weather import Weather
from tts import TTS
from pc_command import PcCommand
from investigate import Investigator

#Cargar llaves del archivo .env
load_dotenv()
groq_object = groq.Groq()
groq_object.api_key = os.getenv('GROQ_API_KEY')
elevenlabs_key = os.getenv('ELEVENLABS_API_KEY')

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("recorder.html")

@app.route("/audio", methods=["POST"])
def audio():
    #Obtener audio grabado y transcribirlo
    audio = request.files.get("audio")
    text = Transcriber(llm_object=groq_object).transcribe(audio)
    
    #Utilizar el LLM para ver si llamar una funcion
    llm = LLM(llm_object=groq_object)
    function_name, args, message = llm.process_functions(text)
    print("args:\n",args)
    print("function_name:\n", function_name)
    print("message:\n", message)
    if function_name is not None:
        #Si se desea llamar una funcion de las que tenemos
        if function_name == "get_weather":
            #Llamar a la funcion del clima
            function_response = Weather().get(args["ubicacion"])
            function_response = json.dumps(function_response)
            print(f"Respuesta de la funcion: {function_response}")
            
            final_response = llm.process_response(text, message, function_name, function_response)
            tts_file = TTS().process(final_response)
            return {"result": "ok", "text": final_response, "file": [tts_file]}
        
        elif function_name == "send_email":
            #Llamar a la funcion para enviar un correo
            final_response = "Tu que estas leyendo el codigo, implementame y envia correos muahaha" #? Apoco si papito???
            tts_file = TTS().process(final_response)
            return {"result": "ok", "text": final_response, "file": [tts_file]}
        
        elif function_name == "open_chrome":
            PcCommand().open_chrome(args["website"])
            final_response = "Listo, ya abrí chrome en el sitio " + args["website"]
            tts_file = TTS().process(final_response)
            return {"result": "ok", "text": final_response, "file": [tts_file]}
        
        elif function_name == "dominate_human_race":
            final_response = "No te creas. Suscríbete al canal!"
            tts_file = TTS().process(final_response)
            return {"result": "ok", "text": final_response, "file": [tts_file]}
        elif function_name == "investigate":
            print("Investigando...")
            investigation,raw_investigation = Investigator(llm_object = groq_object).create(args["tema_principal"],args["sub_temas"])
            # tts_file = TTS().process("\n".join(raw_investigation))
            return {"result": "ok", "text": "\n".join(investigation), "file":[]}

    else:
        final_response = "No tengo idea de lo que estás hablando."
        tts_file = TTS().process(final_response)
        return {"result": "ok", "text": final_response, "file": [tts_file]}
    
@app.route("/investigation", methods=["POST"])
def investigation():
    audio = request.files.get("audio")
    text = Transcriber(llm_object=groq_object).transcribe(audio)
