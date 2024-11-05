from groq_use import MainModelLLM
from tts import TTS
from threading import Thread
class Investigator(MainModelLLM):
    def __init__(self, llm_object) -> None:
        super().__init__(llm_object)

    def __search_topic(self, text,index=0):
        response = self._ai.chat.completions.create(
            model="llama3-groq-70b-8192-tool-use-preview",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Eres un investigador de temas, tu tarea es investigar sobre un tema que te pida el usuario."
                        "Debes de investigar y dar una respuesta concisa y clara al usuario."
                        "Debes de investigar usando internet"
                    )
                },
                {
                    "role": "user",
                    "content": text
                }],
                max_tokens=1024,
        )
        content = response.choices[0].message.content
        
        return self.__to_markdown(content),content
    
    def __to_markdown(self,text):
        response = self._ai.chat.completions.create(
            model="llama3-groq-70b-8192-tool-use-preview",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Tu unica tarea es tomar un texto y esquematizarlo."
                        "Dame los resultados en formato markdown."
                    )
                },
                {
                    "role": "user",
                    "content": text
                }],
        )
        return response.choices[0].message.content
        

    from threading import Thread

    def create(self, topic:str, sub_topics:tuple):
        messages = [None for i in sub_topics]
        raw_messages = [None for i in sub_topics]
        threads = []

        def search_and_append(sub_topic,index):
            message,raw_message= self.__search_topic(f"{topic}:{sub_topic}",index)
            messages[index] = message
            raw_messages[index] = raw_message

        for index,sub_topic in enumerate(sub_topics):
            thread = Thread(target=search_and_append, args=(sub_topic,index))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        return messages,raw_messages