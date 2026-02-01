import google.generativeai as genai
genai.configure(api_key="AIzaSyD7uJ321FcGWmAj7zEiwniSHqNw6f8y7hs")
model=genai.GenerativeModel('gemini-2.5-flash')

topic="Life of a lazy software engineer"
prompt=f"Give me 5 viral instagram reel ideas about {topic}. Make them funny and relatable."

print("--=Asking for ideas---")
response= model.generate_content(prompt)

print(response.text)






#




