import pathlib
import textwrap

import google.generativeai as genai

from IPython.display import display
from IPython.display import Markdown


genai.configure(api_key='AIzaSyDwCd7UCMxYe7zQKlho91CHBRZLc8SHdQ0')
model = genai.GenerativeModel('gemini-1.5-flash')
conversation = model.generate_content('Hola').text
print(conversation)