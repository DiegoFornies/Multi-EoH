import ollama
import google.generativeai as genai
import time

class LLMClient:
    def __init__(self):
        genai.configure(api_key='AIzaSyDwCd7UCMxYe7zQKlho91CHBRZLc8SHdQ0')
        self.model = genai.GenerativeModel('gemini-2.0-flash')
        self.counter = 1

    def query(self, system_prompt, user_prompt):
        content = self.model.generate_content(system_prompt + '\n' + user_prompt).text
        self.counter += 1
        if(self.counter % 15 == 0):
            print('Esperando...')
            time.sleep(15)
        return content