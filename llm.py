import json
from groq_use import MainModelLLM
from groq import Groq
from groq.types.chat import ChatCompletionMessage
# ai = Groq()
# r = ChatCompletionMessage()
# r.dict()

#Clase para utilizar cualquier LLM para procesar un texto
#Y regresar una funcion a llamar con sus parametros
#Uso el modelo 0613, pero puedes usar un poco de
#prompt engineering si quieres usar otro modelo
class LLM(MainModelLLM):    
    def __init__(self,llm_object):
        super().__init__(llm_object)
        self.__model = 'llama3-groq-70b-8192-tool-use-preview'
        self.__content_system = (
            "Eres un asistente el cual esta atento a todo lo que dice el usuario ya que le ayudaras a investigar temas sin que te lo pida directamente."
            "Si el usuario menciona un tema y subtemas debes investigar sobre ello. Si el usuario solo menciona el tema antes de investigar debes de razonar cuales serian los posibles sub temas."
        )
    
    def process_functions(self, text):
        
        response = self._ai.chat.completions.create(
            model=self.__model,
            messages=[
                    #Si no te gusta que te hable feo, cambia aqui su descripcion
                    {"role": "system", "content": self.__content_system},
                    {"role": "user", "content": text},
            ], functions=[
                {
                    "name": "investigate",
                    "description": "Investigar un tema del cual se este hablando o se haya mencionado",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "tema_principal":{
                                "type":"string",
                                "description":"El tema principal del cual se quiere investigar"
                            },
                            "sub_temas":{
                                "type":"array",
                                "description":"Los subtemas que divergen del tema principal",
                                "items":{
                                    "type":"string"
                                }
                            
                            }
                        },
                        "required": [
                            "tema_principal",
                            "sub_temas"
                        ]
                    }
                },

            ],
            temperature=0,
            function_call="auto",
        )
        message = response.choices[0].message.dict()
        
        #Nuestro amigo GPT quiere llamar a alguna funcion?
        if message.get("function_call"):
            #Sip
            function_name = message["function_call"]["name"] #Que funcion?
            args = message['function_call']['arguments'] #Con que datos?
            print("Funcion a llamar: " + function_name)
            args = json.loads(args)
            return function_name, args, message
        
        return None, None, message
    
    #Una vez que llamamos a la funcion (e.g. obtener clima, encender luz, etc)
    #Podemos llamar a esta funcion con el msj original, la funcion llamada y su
    #respuesta, para obtener una respuesta en lenguaje natural (en caso que la
    #respuesta haya sido JSON por ejemplo
    def process_response(self, text, message, function_name, function_response):
        response = self._ai.chat.completions.create(
            model=self.__model,
            messages=[
                #Aqui tambien puedes cambiar como se comporta
                {"role": "system", "content": self.__content_system},
                {"role": "user", "content": text},
                message,
                {
                    "role": "function",
                    "name": function_name,
                    "content": function_response,
                },
            ],
        )
        return response.choices[0].message

