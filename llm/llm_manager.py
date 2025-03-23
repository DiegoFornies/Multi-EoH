import re

class LLMManager:
    def __init__(self):
        from llm import LLMClient
        self.LLMClient = LLMClient()
    
    def get_heuristic(self, system_prompt, user_prompt):
        response = self.LLMClient.query(system_prompt, user_prompt)
        return self.decode_heuristic(response)

    def decode_heuristic(self, encoded_ind):
        code_pattern = r'```python(.*?)```'
                
        code_matches = re.findall(code_pattern, encoded_ind, re.DOTALL)
        code_matches = code_matches[0] if code_matches else ''
        
        return code_matches
    
    def get_reflection(self, system_prompt, user_prompt):
        response = self.LLMClient.query(system_prompt, user_prompt)
        return response