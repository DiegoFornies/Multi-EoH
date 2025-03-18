import pathlib
import textwrap

import google.generativeai as genai

from IPython.display import display
from IPython.display import Markdown


genai.configure(api_key='AIzaSyDwCd7UCMxYe7zQKlho91CHBRZLc8SHdQ0')
model = genai.GenerativeModel('gemini-1.5-flash')
conversation = model.start_chat(history=[
    {"role": "system", "parts": ["Eres un experto en inteligencia artificial y debes explicar conceptos de forma clara y concisa."]}
])

response = conversation.send_message("Explica cómo funciona la inteligencia artificial.")