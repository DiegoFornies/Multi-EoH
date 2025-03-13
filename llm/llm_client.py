class LLMClient:
    def __init__(self):
        self.llm = ''

    def query(self, system_prompt, user_prompt):
        with open('llm/prueba.txt', 'r') as f:
            content = f.read()
        return content