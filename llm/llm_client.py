import ollama

class LLMClient:
    def __init__(self):
        self.model = "llama3.2"
        self.counter = 1

    def query(self, system_prompt, user_prompt):
        with open(f'llm/prueba{self.counter}.txt', 'r') as f:
            content = f.read()
        if self.counter == 3:
            self.counter = 1
        else:
            self.counter += 1
        return content