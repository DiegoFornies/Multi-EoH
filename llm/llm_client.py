import google.generativeai as genai
import time

class LLMClient:
    def __init__(self):
        genai.configure(api_key='AIzaSyDwCd7UCMxYe7zQKlho91CHBRZLc8SHdQ0')
        self.model = genai.GenerativeModel('gemini-2.0-flash')
        self.total_petitions = 0
        self.counter = 0
        self.time = time.time()
        self.total_input_tokens = 0
        self.total_output_tokens = 0

    def query(self, system_prompt, user_prompt):
        elapsed_time = time.time() - self.time

        if self.counter >= 12:
            if elapsed_time < 60:
                time_to_wait = 60 - elapsed_time + 5
                print(f"Esperando {time_to_wait:.2f} segundos para cumplir el límite de 15 peticiones por minuto.")
                time.sleep(time_to_wait)
            self.total_petitions += self.counter
            self.counter = 0
            self.time = time.time()

        prompt = system_prompt + '\n' + user_prompt
        response = self.model.generate_content(prompt)

        input_tokens = self.model.count_tokens(prompt).total_tokens
        self.total_input_tokens += input_tokens

        output_tokens = self.model.count_tokens(response.text).total_tokens
        self.total_output_tokens += output_tokens
        self.counter += 1

        return response.text
