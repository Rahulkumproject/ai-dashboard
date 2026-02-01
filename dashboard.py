import streamlit as st
import pandas as pd
import google.generativeai as genai

st.set_page_config(page_title="AI Analyst",page_icon="🤖")
st.title("🤖 200k views AI dashbard")

api_key= st.sidebar.text_input("Enter google api key",type="password")

uploaded_file= st.file_uploader("Upload your Excel file",type=["xlsx"])

if api_key and uploaded_file:
    df=pd.read_excel(uploaded_file,engine="openpyxl")
    st.subheader("Data Preview")
    st.dataframe(df.head())

    if st.button("Generate AI Report"):
        genai.configure(api_key=api_key)
        model= genai.GenerativeModel('gemini-2.5-flash')
        with st.spinner("AI is thinking"):
            data_summary=df.head().to_string()
            counts=df['Account_Name'].value_counts().head().to_string()
            prompt=f"""
                    Analyze this dataset sample:
                    {data_summary}
                
                    Explain these to me as i am 5 year old , use emojis
                    """
            response=model.generate_content(prompt)
            st.success("AI Report Generated")
            st.markdown(response.text)
