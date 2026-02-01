import pandas as pd
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("API_KEY"))
model = genai.GenerativeModel('gemini-2.5-flash')

df=pd.read_excel("api_fetched.xlsx",engine="openpyxl")
data_sample=df.head(3).to_string()
top_account=df['Account_Name'].value_counts().head(4).to_string()

prompt = f"""
You are a Senior Data Analyst. I am providing you with data from our system.

Here is a sample of the raw data (First 20 rows):
{data_sample}

Here are the top accounts by frequency:
{top_account}

Please analyze this data and provide a professional report:
1. Identify the most active account.
2. Are there any potential duplicates or issues in the account names?
3. Suggest 3 actionable next steps for the engineering team to clean this data.
"""

print("--=Sending AI analyst ---")
response= model.generate_content(prompt)
print("-- AI Report --")
print(response.text)