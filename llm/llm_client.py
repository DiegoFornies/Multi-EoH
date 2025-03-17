class LLMClient:
    def __init__(self):
        self.llm = ''
        self.counter = 1

    def query(self, system_prompt, user_prompt):
        if(self.counter == 3):
            self.counter = 1
        else:
            self.counter += 1
        with open(f'llm/prueba{self.counter}.txt', 'r') as f:
            content = f.read()
        return content