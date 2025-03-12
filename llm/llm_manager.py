from llm import LLMClient
import re

class LLMManager:
    def __init__(self):
        self.LLMClient = LLMClient()
    
    def get_heuristic(self, system_prompt, user_prompt):
        response = self.LLMClient(system_prompt, user_prompt)
        return self.decode_heuristic(response)

    def decode_heuristic(self, encoded_ind):
        code_pattern = r'```python(.*?)```'
        code_matches = re.findall(code_pattern, encoded_ind, re.DOTALL)
        description = re.sub(code_pattern, '', encoded_ind).strip()
        
        return description, code_matches